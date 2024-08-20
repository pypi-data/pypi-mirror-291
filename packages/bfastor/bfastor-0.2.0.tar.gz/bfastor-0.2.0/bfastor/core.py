import chex
import jax.random
import numpy as np
import jax.numpy as jnp
import typing
import flax.struct

import optax


@chex.dataclass
class Parameters:
    coordinates: typing.Union[jnp.ndarray, np.ndarray]
    sigmas: typing.Union[jnp.ndarray, np.ndarray]
    a: typing.Union[jnp.ndarray, np.ndarray]
    b: typing.Union[jnp.ndarray, np.ndarray]
    mass: typing.Union[jnp.ndarray, np.ndarray]
    apix: typing.Union[jnp.ndarray, np.ndarray, None] = None


@flax.struct.dataclass
class Data:
    densities: jnp.ndarray


@flax.struct.dataclass
class ExtraParams:
    data_shape: tuple
    shape: tuple = flax.struct.field(pytree_node=False)
    apix: jnp.ndarray
    neighbours_ij: jnp.ndarray
    neighbour_distances: jnp.ndarray


@flax.struct.dataclass
class Functions:
    loss_and_grads: typing.Callable = flax.struct.field(pytree_node=False)
    optimiser: typing.Callable = flax.struct.field(pytree_node=False)
    blurrer: typing.Callable = flax.struct.field(pytree_node=False)
    progress_bar: typing.Callable = flax.struct.field(pytree_node=False)


@chex.dataclass  # mutable
class State:
    params: Parameters
    data: Data
    extra_params: ExtraParams
    opt_state: optax.OptState
    key: jax.random.PRNGKey
    loss: jnp.ndarray
    i: int = 0
