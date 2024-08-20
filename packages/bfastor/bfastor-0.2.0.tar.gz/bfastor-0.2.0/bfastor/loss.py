import typing
from dataclasses import fields
import jax.numpy as jnp
from bfastor import blur, core
import jax
import jax.scipy as jscipy
import optax


def normalise(data, axis=None, keepdims=False):
    normalised_data = (data - data.mean(axis=axis, keepdims=keepdims)) / data.std(
        axis=axis, keepdims=keepdims
    )
    return normalised_data


def variance_loss(indexed_data: jax.Array, simulated_data: jax.Array) -> jax.Array:
    loss_1 = (
        -jnp.sum(
            normalise(indexed_data.mean(axis=-1))
            * normalise(simulated_data.mean(axis=-1)),
            keepdims=True,
        )
        / indexed_data.shape[0]
    )
    loss_2 = (
        -jnp.sum(
            normalise(indexed_data, -1, True) * normalise(simulated_data, -1, True),
            axis=-1,
        )
        / indexed_data.shape[-1]
    )
    return loss_1 + loss_2


def density_loss(indexed_data: jax.Array, simulated_data: jax.Array) -> jax.Array:
    indexed_data = indexed_data.squeeze()
    v_loss = variance_loss(indexed_data, simulated_data)

    h_loss = (
        optax.huber_loss(normalise(indexed_data), normalise(simulated_data)).sum(
            axis=-1
        )
        / 5
    )

    return jnp.nansum(v_loss + h_loss)


def neighbour_loss(
    sigmas: jax.Array, neighbour_indexes: jax.Array, neighbour_distances: jax.Array
) -> jax.Array:
    weights = jscipy.stats.norm.pdf(neighbour_distances, 0, 2.0)
    weights = weights / weights.max(axis=-1, keepdims=True)
    vals = sigmas[neighbour_indexes] - sigmas[:, None]
    scale = jnp.clip(jax.lax.stop_gradient(sigmas / 2), 0.05, 0.5)
    losses = jax.vmap(
        jscipy.stats.norm.logpdf,
        in_axes=(1, None, None),
        out_axes=1,
    )(vals, 0, scale)
    losses = jnp.average(losses, axis=-1, weights=weights)
    return -jnp.nansum(losses)


def get_loss_function(
    simulation_function: typing.Callable,
    reconstruction_loss_function: typing.Callable = density_loss,
    regularisation_loss_function: typing.Callable = neighbour_loss,
    gradient_params: typing.Tuple[str] = ("sigmas",),
) -> typing.Callable:
    def loss_function(
        params: core.Parameters,
        x: jax.Array,
        indexed_densities: jax.Array,
        neighbour_indexes: jax.Array,
        neighbour_distances: jax.Array,
    ) -> jnp.ndarray:
        for p in fields(params):
            if p.name in gradient_params:
                continue
            setattr(params, p.name, jax.lax.stop_gradient(getattr(params, p.name)))

        simulated_densities = simulation_function(params, x, neighbour_indexes)

        reconstruction_loss = reconstruction_loss_function(
            indexed_densities, simulated_densities
        )
        regularisation_loss = regularisation_loss_function(
            params.sigmas, neighbour_indexes, neighbour_distances
        )

        return reconstruction_loss + regularisation_loss

    return loss_function


@jax.jit
def warmup_loss(
    sigmas: jax.Array,
    params: core.Parameters,
    indexed_density: jax.Array,
    random_vectors: jax.Array,
    neighbours_ij: jax.Array,
) -> jax.Array:
    simulated_density = blur.isp.simulate_summed_densities_from_all_atoms(
        random_vectors,
        params.coordinates[neighbours_ij],
        sigmas[neighbours_ij],
        params.a[neighbours_ij],
        params.b[neighbours_ij],
        params.mass[neighbours_ij],
        params.apix,
    )
    indexed_density = indexed_density.squeeze()
    h_loss = optax.huber_loss(
        normalise(indexed_density), normalise(simulated_density)
    ).sum(axis=-1)

    return h_loss
