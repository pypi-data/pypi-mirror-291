import functools
import types
import typing
import chex
import jax
import jax.numpy as jnp
import numpy as np

import bfastor.models
from bfastor import blur, maps
import inspect
import voxcov as vc


@functools.partial(
    jax.jit,
    static_argnums=(1,),
    inline=False,
)
def get_grid_around_atom(
    ijk_coordinate,
    radius,
):
    chex.assert_shape(ijk_coordinate, (3,))
    x = jnp.arange(-radius, radius + 1, 1)
    grid = jnp.meshgrid(x, x, x, indexing="ij")
    return jnp.stack(grid).T.reshape(-1, 3) + ijk_coordinate


def get_blur_atoms_function(blurring_function, *args):
    @functools.partial(jax.jit, static_argnums=2)
    def blur_atom_function(coordinate, bfactor, radius, map_apix, *args_):
        ijk_points = get_grid_around_atom((xyz_to_ijk(coordinate, map_apix)), radius)
        points = ijk_to_xyz(
            ijk_points,
            map_apix,
            module=inspect.getmodule(blurring_function),
        )
        simulated_points = blurring_function(
            points,
            coordinate,
            bfactor,
            *args_,
        )
        chex.assert_equal(points.shape[0], simulated_points.shape[0])
        return ijk_points, simulated_points

    vmapped_function = jax.vmap(
        blur_atom_function, in_axes=(0, 0, None, None, *[0] * len(args))
    )

    return vmapped_function


@functools.partial(jax.jit, donate_argnums=(0, 1))
def add_unique_points_to_map(
    voxel_index: jnp.ndarray,
    voxel_density: jnp.ndarray,
    density_map: jnp.ndarray,
):
    return density_map.at[tuple(voxel_index.T)].add(voxel_density, unique_indices=True)


def add_unique_points_to_map_scanning(
    args,
    index,
):
    voxel_indexes, voxel_densities, density_map = args
    updated_map = add_unique_points_to_map(
        voxel_indexes[index],
        voxel_densities[index],
        density_map,
    )
    return (voxel_indexes, voxel_densities, updated_map), 0.0


def ijk_to_xyz(
    ijk_points: typing.Union[np.ndarray, jnp.ndarray],
    map_apix: typing.Union[np.ndarray, jnp.ndarray],
    module: types.ModuleType = blur.mvg,
):
    return module.ijk_to_xyz(ijk_points, map_apix)


def xyz_to_ijk(
    xyz,
    map_apix,
):
    return jnp.round(jnp.flip(xyz / map_apix))


def get_radii(bfactors, sigma_cutoff, map_apix):
    radii = np.ceil((bfactors * sigma_cutoff) / max(map_apix))
    if np.any(radii > 25):
        radii = np.ceil((bfactors * sigma_cutoff) / (max(map_apix) * 8 * np.pi**2))
    radius = radii.max()
    return radius


def generic_structure_blurrer(
    coordinates: np.ndarray,
    bfactors: np.ndarray,
    map_apix: np.ndarray,
    map_shape: tuple[int],
    map_origin: np.ndarray,
    *args,
    blurring_function: typing.Callable = blur.mvg.simulate_densities_from_single_atom,
    sigma_cutoff: float = 4.0,
    chunk_size: int = 2000,
):
    sort_ind = np.argsort(bfactors)
    bfactors = np.take_along_axis(bfactors, sort_ind, 0)
    coordinates = (coordinates - map_origin)[sort_ind]
    args = tuple([arg[sort_ind] for arg in args])
    blur_atoms_f = jax.jit(
        get_blur_atoms_function(
            blurring_function,
            *args,
        ),
        static_argnums=2,
    )
    start = 0
    end = chunk_size

    em_map = jnp.zeros(map_shape)
    for _ in range(np.ceil(coordinates.shape[0] / chunk_size).astype(int)):
        radius = get_radii(bfactors[start:end, ...], sigma_cutoff, map_apix)
        ijk_points, sim_points = blur_atoms_f(
            coordinates[start:end, ...],
            bfactors[start:end, ...],
            radius,
            map_apix,
            *(arg[start:end, ...] for arg in args),
        )
        (_, _, em_map), _ = jax.lax.scan(
            add_unique_points_to_map_scanning,
            (ijk_points.astype(int), sim_points, em_map),
            jnp.arange(ijk_points.shape[0]),
        )
        start += chunk_size
        end += chunk_size
        end = min(bfactors.shape[0], end)

    return maps.Map(em_map, map_apix, map_origin)


def blur_structure_with_gaussian_pdf(
    model: bfastor.models.Structure,
    template_map: bfastor.maps.Map,
    sigma_cutoff: float = 4.0,
    chunk_size: int = 2000,
):
    return generic_structure_blurrer(
        model.get_column_data(["x", "y", "z"]),
        model.get_column_data("temp_fac"),
        template_map.apix,
        template_map.data.shape,
        template_map.origin,
        blurring_function=blur.mvg.simulate_densities_from_single_atom,
        sigma_cutoff=sigma_cutoff,
        chunk_size=chunk_size,
    )


def blur_structure_with_scattering_potential(
    model: bfastor.models.Structure,
    template_map: bfastor.maps.Map,
    sigma_cutoff: float = 4.0,
    chunk_size: int = 2000,
):
    a, b, masses = blur.atom_parameters.get_parameter_array_from_model(model)
    return generic_structure_blurrer(
        model.get_column_data(["x", "y", "z"]),
        model.get_column_data("temp_fac"),
        template_map.apix,
        template_map.data.shape,
        template_map.origin,
        a,
        b,
        masses,
        blurring_function=blur.sp.simulate_densities_from_single_atom,
        sigma_cutoff=sigma_cutoff,
        chunk_size=chunk_size,
    )


def blur_structure_with_integrated_scattering_potential(
    model: bfastor.models.Structure,
    template_map: bfastor.maps.Map,
    sigma_cutoff: float = 4.0,
    chunk_size: int = 2000,
):
    a, b, masses = blur.atom_parameters.get_parameter_array_from_model(model)
    apix_array = np.repeat(template_map.apix[None, :], len(masses), axis=0)
    return generic_structure_blurrer(
        model.get_column_data(["x", "y", "z"]),
        model.get_column_data("temp_fac"),
        template_map.apix,
        template_map.data.shape,
        template_map.origin,
        a,
        b,
        masses,
        apix_array,
        blurring_function=blur.isp.simulate_densities_from_single_atom,
        sigma_cutoff=sigma_cutoff,
        chunk_size=chunk_size,
    )


def blur_map_with_bfactors(model, template_map):
    blur_vc = vc.BlurMap(
        template_map.apix,
        template_map.origin,
        np.flip(template_map.data.shape),
        4,
    )
    for x, y, z, temp_fac, mass in model.get_column_data(
        ["x", "y", "z", "temp_fac", "mass"]
    ):
        blur_vc.add_gaussian(
            [x, y, z],
            mass,
            temp_fac,
        )

    return maps.Map(
        blur_vc.to_numpy(),
        origin=template_map.origin,
        apix=template_map.apix,
    )
