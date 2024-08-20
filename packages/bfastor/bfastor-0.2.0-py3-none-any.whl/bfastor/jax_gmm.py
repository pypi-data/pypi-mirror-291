import functools
import os
import inspect
import pathlib
import typing
import tqdm

os.environ[
    "XLA_PYTHON_CLIENT_PREALLOCATE"
] = "false"  # this stops jax automatically allocating ~90% of GPU memory
import jax  # noqa: E402
from bfastor import loss, models, maps, blur, spatial  # noqa: E402
from bfastor.core import (  # noqa: E402
    Parameters,
    State,
    Data,
    ExtraParams,
    Functions,
)
import jax.numpy as jnp  # noqa: E402
import optax  # noqa: E402
import numpy as np  # noqa: E402


def normalise(data):
    normalised_data = (data - data.min()) / (data.max() - data.min())
    return normalised_data


def get_coordinates_from_model(model, origin):
    uncorrected_coordinates = model.get_columns(["z", "y", "x"])
    return jnp.asarray(uncorrected_coordinates) - jnp.flip(jnp.asarray(origin))


def step_progress_bar(pbar, state, n, patience):
    _ = jax.lax.cond(
        state.i % 10 == 0,
        pbar,
        lambda x: x,
        10,
    )
    _ = jax.lax.cond(
        n > patience,
        pbar,
        lambda x: x,
        1e12,
    )


@functools.partial(jax.jit, static_argnums=(1,), inline=True)
def step(state, functions):
    (
        random_vectors,
        indexed_densities,
        key,
    ) = spatial.prepare_data_from_state(state)
    random_vectors = (random_vectors / state.params.apix).round(0) * state.params.apix
    if inspect.getmodule(functions.blurrer) is not blur.isp:
        random_vectors = random_vectors + (state.params.apix / 2)
    loss, grads = functions.loss_and_grads(
        state.params,
        random_vectors,
        indexed_densities,
        state.extra_params.neighbours_ij,
        state.extra_params.neighbour_distances,
    )
    new_params, opt_state = update_params_from_state(state, grads, functions.optimiser)
    return State(
        params=new_params,
        data=state.data,
        extra_params=state.extra_params,
        opt_state=opt_state,
        key=key,
        loss=jnp.nan_to_num(loss),
        i=state.i + 1,
    )


def scan_compliant_step(args, _):
    n, min_loss, patience, state, functions = args
    updated_state = jax.lax.cond(
        n >= patience,
        lambda x, y: x,
        step,
        state,
        functions,
    )
    if functions.progress_bar is not None:
        jax.jit(step_progress_bar, static_argnums=0)(
            functions.progress_bar, state, n, patience
        )
    n = jax.lax.cond(
        updated_state.loss < min_loss,
        lambda x: 0,
        lambda x: x + 1,
        n,
    )
    min_loss = jax.lax.cond(
        updated_state.loss < min_loss,
        lambda x, y: x,
        lambda x, y: y,
        updated_state.loss,
        min_loss,
    )
    return (n, min_loss, patience, updated_state, functions), updated_state.loss


@functools.partial(jax.jit, static_argnames="max_steps")
def run(state, step_functions, max_steps, patience):
    (n, min_loss, patience, new_state, _), losses = jax.lax.scan(
        scan_compliant_step,
        (0, jnp.inf, patience, state, step_functions),
        None,
        length=max_steps,
    )
    return (
        new_state,
        losses,
    )


class GradientDescentRefiner:
    def __init__(
        self,
        coordinates: jnp.ndarray,
        experimental_density: jnp.ndarray,
        a: typing.Optional[jnp.ndarray] = None,
        b: typing.Optional[jnp.ndarray] = None,
        mass: typing.Optional[jnp.ndarray] = None,
        pixel_size: typing.Optional[jnp.ndarray] = None,
        n_points: int = 5,
        n_neighbours: int = 8,
        learning_rate: float = 0.1,
        simulation_function: typing.Callable = blur.isp.simulate_densities_from_params,
        reconstruction_loss_function: typing.Callable = loss.density_loss,
        regularisation_loss_function: typing.Callable = loss.neighbour_loss,
    ):
        self.coordinates = coordinates
        self.experimental_density = experimental_density
        self.a = a
        self.b = b
        self.mass = mass
        self.pixel_size = pixel_size
        self.n_neighbours = n_neighbours
        self.n_points = n_points
        self.simulation_function = simulation_function
        self.reconstruction_loss_function = reconstruction_loss_function
        self.regularisation_loss_function = regularisation_loss_function
        self.done_setup = False
        self.run_f = run
        self.progress_bar = None

        data = Data(densities=experimental_density)
        params = Parameters(
            coordinates=coordinates,
            sigmas=np.full(self.coordinates.shape[0], 0.5),
            a=a,
            b=b,
            mass=mass,
            apix=pixel_size,
        )
        extra_params = ExtraParams(
            data_shape=np.array(experimental_density.shape),
            shape=(coordinates.shape[0], self.n_points, 3),
            apix=pixel_size,
            neighbours_ij=None,
            neighbour_distances=None,
        )
        optimiser = optax.chain(
            optax.sgd(learning_rate=learning_rate),
            optax.clip(0.1),
        )
        self.loss_function = loss.get_loss_function(
            simulation_function,
            reconstruction_loss_function,
            regularisation_loss_function,
        )
        self.state = State(
            params=params,
            data=data,
            extra_params=extra_params,
            opt_state=optimiser.init(params),
            key=jax.random.key(12345),
            loss=jnp.inf,
            i=0,
        )
        self.step_functions = Functions(
            loss_and_grads=jax.jit(
                jax.value_and_grad(
                    self.loss_function,
                    argnums=0,
                ),
                inline=True,
            ),
            optimiser=optimiser,
            blurrer=simulation_function,
            progress_bar=None,
        )
        self.losses = None

    @property
    def bfactors(self):
        return self.state.params.sigmas

    @bfactors.setter
    def bfactors(self, val: typing.Union[jnp.ndarray, np.ndarray]):
        if val.shape != self.state.params.sigmas.shape:
            raise ValueError(
                f"New B-factor values must have same shape as existing ones. Got new shape "
                f"{val.shape} and existing shape {self.params.sigmas.shape}"
            )
        self.state.params.sigmas = val

    def setup(self):
        distances, indexes = spatial.get_nearest_neighbour_indexes(
            self.coordinates, window_size=self.n_neighbours
        )
        self.state.extra_params = self.state.extra_params.replace(
            neighbours_ij=indexes, neighbour_distances=distances
        )
        self._step = step
        self.done_setup = True

    def warmup(self):
        self.state.params.sigmas = warmup(self.state)

    def step(self):
        if not self.done_setup:
            raise RuntimeError(
                "step() function called before running setup(), "
                "please call setup() method before step()"
            )
        self.state = self._step(self.state, self.step_functions)

    def add_progress_bar(self, max_steps):
        self.progress_bar = progress_bar = tqdm.tqdm(
            total=max_steps,
        )

        def do_pbar_step(n):
            n = int(n)
            if n >= progress_bar.total - n:
                progress_bar.close()
            else:
                progress_bar.update(n)

        def step_function(n):
            jax.debug.callback(do_pbar_step, n)
            return n

        self.step_functions = self.step_functions.replace(
            progress_bar=step_function,
        )

    def fit(self, max_steps=500, patience=50, warmup=True, verbose=True):
        if verbose:
            self.add_progress_bar(max_steps=max_steps)
        if not self.done_setup:
            self.setup()
        if warmup:
            self.warmup()
        self.state, self.losses = run(
            self.state, self.step_functions, max_steps, patience
        )
        self.finish_up()

    def fit_with_python_loop(
        self, max_steps=500, patience=50, check_every=20, warmup=True, verbose=True
    ):
        if verbose:
            self.add_progress_bar(max_steps=max_steps)
        losses = []
        min_loss = jnp.inf
        n = 0
        self.setup()
        if warmup:
            self.warmup()
        while self.state.i < max_steps:
            for _ in range(check_every):
                self.step()
                losses.append(self.state.loss)
            if self.state.loss < min_loss:
                min_loss = self.state.loss
                n = 0
            else:
                n += check_every
            if self.step_functions.progress_bar is not None:
                self.step_functions.progress_bar(check_every)
            if n >= patience:
                if self.step_functions.progress_bar is not None:
                    self.step_functions.progress_bar(max_steps)
                break
        self.losses = np.stack(losses)
        self.finish_up()

    def finish_up(self):
        if self.progress_bar is not None:
            self.progress_bar.close()
        run.clear_cache()
        step.clear_cache()


class BfactorRefiner(GradientDescentRefiner):
    @classmethod
    def from_file(
        cls,
        model_path: typing.Union[str, pathlib.Path],
        exp_map_path: typing.Union[str, pathlib.Path],
        **kwargs,
    ):
        exp_map = maps.Map.from_file(exp_map_path)
        model = models.Structure.from_file(model_path)
        return cls(model, exp_map, **kwargs)

    def __init__(
        self,
        model: models.Structure,
        exp_map: maps.Map,
        n_points: int = 5,
        n_neighbours: int = 8,
        learning_rate: float = 0.1,
        simulation_function: typing.Callable = blur.isp.simulate_densities_from_params,
        reconstruction_loss_function: typing.Callable = loss.density_loss,
        regularisation_loss_function: typing.Callable = loss.neighbour_loss,
    ):
        self.model = model.copy()
        self.exp_map = exp_map
        self.n_points = n_points
        self.n_neighbours = n_neighbours
        self.done_setup = False
        self.run_f = run

        cropped_map = self.cropped_map = maps.get_cropped_data_from_map(exp_map, model)
        normalised_map = normalise(np.asarray(cropped_map.data))
        self.origin = cropped_map.origin

        coordinates = get_coordinates_from_model(self.model, cropped_map.origin)
        a, b, mass = blur.atom_parameters.get_parameter_array_from_model(model)

        super().__init__(
            coordinates=coordinates,
            experimental_density=normalised_map,
            a=a,
            b=b,
            mass=mass,
            pixel_size=cropped_map.apix,
            n_points=n_points,
            n_neighbours=n_neighbours,
            learning_rate=learning_rate,
            simulation_function=simulation_function,
            reconstruction_loss_function=reconstruction_loss_function,
            regularisation_loss_function=regularisation_loss_function,
        )

    def get_model(self):
        self.set_model_params()
        return self.model

    def set_model_params(self):
        coordinates = np.flip(self.coordinates + np.flip(self.origin), axis=-1)
        bfac = self.bfactors
        self.model.set_columns(["x", "y", "z"], coordinates)
        self.model.set_columns("temp_fac", bfac)

    def finish_up(self):
        self.set_model_params()
        super().finish_up()


def _update_params(optimiser, params, grads, opt_state):
    grads = jax.tree_util.tree_map(jnp.nan_to_num, grads)
    updates, opt_state = optimiser.update(grads, opt_state, params)
    new_params = optax.apply_updates(params, updates)
    new_params = optax.incremental_update(new_params, params, 0.05)
    new_params.sigmas = jnp.clip(new_params.sigmas, 0.01, jnp.inf)
    return new_params, opt_state


def update_params_from_state(state: State, grads, optimiser):
    return _update_params(
        optimiser,
        state.params,
        grads,
        state.opt_state,
    )


def warmup(state, lower_lim=0.5, upper_lim=3.5):
    random_vectors, indexed_data, state.key = spatial.prepare_data_from_state(state)
    random_vectors = (random_vectors / state.params.apix).round(0) * state.params.apix
    trial_bfactors = np.arange(lower_lim, upper_lim, 0.5)
    bfactor_arrays = np.repeat(
        trial_bfactors[:, None], state.params.sigmas.shape[0], axis=1
    )
    losses = jax.vmap(
        loss.warmup_loss,
        in_axes=(0, None, None, None, None),
    )(
        bfactor_arrays,
        state.params,
        indexed_data,
        random_vectors,
        state.extra_params.neighbours_ij,
    )
    best_bfacs = trial_bfactors[np.argmin(losses, axis=0)]

    return best_bfacs
