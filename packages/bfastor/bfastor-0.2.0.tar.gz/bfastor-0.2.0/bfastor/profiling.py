import typing

import jax
import time
import numpy as np


def get_jit_lowering_times(
    jitted_function,
    *args: typing.Any,
    n_repeats: int = 1,
) -> np.ndarray[float]:
    lower_times = []
    for _ in range(n_repeats):
        start = time.time()
        jitted_function.lower(*args)
        lower_times.append(time.time() - start)
        jax.clear_caches()
        jitted_function.clear_cache()
    return np.array(lower_times)


def get_jit_compilation_times(
    lowered_function, n_repeats: int = 1
) -> np.ndarray[float]:
    compilation_times = []
    for _ in range(n_repeats):
        start = time.time()
        lowered_function.compile()
        compilation_times.append(time.time() - start)
        jax.clear_caches()

    return np.array(compilation_times)


def get_function_execution_times(
    function,
    *args,
    n_repeats: int = 10,
) -> np.ndarray[float]:
    times = []
    for _ in range(n_repeats):
        start = time.time()
        function(*args)
        times.append(time.time() - start)
    return np.array(times)


def get_jitted_function_execution_times(
    compiled_function,
    *args,
    n_repeats: int = 10,
) -> np.ndarray[float]:
    # run function once to ensure its compiled
    compiled_function(*args)

    execution_times = []
    for _ in range(n_repeats):
        start = time.time()
        compiled_function(*args).block_until_ready()
        execution_times.append(time.time() - start)
    return np.array(execution_times)


def get_class_init_times(
    cls,
    *init_args,
    n_repeats: int = 10,
) -> np.ndarray[float]:
    speeds = []
    for _ in range(n_repeats):
        start = time.time()
        _ = cls(*init_args)
        speeds.append(time.time() - start)
    return np.array(speeds)
