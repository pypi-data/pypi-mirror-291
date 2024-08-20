import numpy as np
import dataclasses
from sys import modules

import bfastor.models


@dataclasses.dataclass(frozen=True)
class AtomicParameters:
    m: float
    a: np.ndarray
    b: np.ndarray


def get_parameter_array_from_model(model: bfastor.models.Structure):
    """Get numpy arrays of a, b and mass values needed for simulating EM-maps.

    :param model: Instance of bfastor.models.Structure
    :return: 3 numpy.ndarrays containing all a, b, and mass parameters for the model. Arrays have shape (N, 4) for a
    and b and (N,) for masses for a model of N atoms.
    """
    elements = model.get_columns("element")
    unique_elements, indices = np.unique(elements, return_inverse=True)
    a_s = np.array(
        [modules.get(__name__).__dict__.get(e, C).a for e in unique_elements]
    )[indices]
    b_s = np.array(
        [modules.get(__name__).__dict__.get(e, C).b for e in unique_elements]
    )[indices]
    masses = np.array(
        [modules.get(__name__).__dict__.get(e, C).m for e in unique_elements]
    )[indices]

    return a_s, b_s, masses


H = AtomicParameters(
    m=1.0,
    a=np.array((0.0367, 0.1269, 0.2360, 0.1290)),
    b=np.array(
        (
            0.5608,
            3.7913,
            13.5557,
            37.7229,
        )
    ),
)


C = AtomicParameters(
    m=12.0,
    a=np.array(
        (
            0.1361,
            0.5482,
            1.2266,
            0.5971,
        )
    ),
    b=np.array((0.3731, 3.2814, 13.0456, 41.0202)),
)

N = AtomicParameters(
    m=14.0,
    a=np.array(
        (
            0.1372,
            0.5344,
            1.0862,
            0.4547,
        )
    ),
    b=np.array(
        (
            0.3287,
            2.6733,
            10.3165,
            32.7631,
        )
    ),
)


O = AtomicParameters(  # noqa: E741
    m=16.0,
    a=np.array(
        (
            0.1433,
            0.5103,
            0.9370,
            0.3923,
        )
    ),
    b=np.array((0.3055, 2.2683, 8.2625, 25.6645)),
)


P = AtomicParameters(
    m=31,
    a=np.array(
        (
            0.3540,
            0.9397,
            2.6203,
            1.5707,
        )
    ),
    b=np.array(
        (
            0.3941,
            3.1810,
            15.6579,
            49.5239,
        )
    ),
)

S = AtomicParameters(
    m=32,
    a=np.array(
        (
            0.3478,
            0.9158,
            2.5066,
            1.3884,
        )
    ),
    b=np.array(
        (
            0.3652,
            2.8915,
            13.0522,
            40.1848,
        )
    ),
)
