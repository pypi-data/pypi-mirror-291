import jax.numpy as jnp
import jax
from jax.typing import ArrayLike
import chex


def smoothmax(log_x: ArrayLike, log_y: ArrayLike) -> jax.Array:
    return jnp.log(1 + jnp.exp(log_y - log_x))


def add_logs(log_x: ArrayLike, log_y: ArrayLike) -> jax.Array:
    return log_x + smoothmax(log_x, log_y)


def sum_logs(log_arr: ArrayLike) -> jax.Array:
    chex.assert_rank(log_arr, 1)
    arr = log_arr[1:]

    def add_logs_in_scan(carry, x):
        result = add_logs(carry, x)
        return result, result

    return jax.lax.scan(add_logs_in_scan, log_arr[0], arr)[0]
