import argparse
import pathlib

from bfastor import helpers, jax_gmm, models, maps, blur
import jax
import numpy as np


def jax_has_gpu_or_tpu():
    try:
        _ = jax.device_put(jax.numpy.ones(1), device=jax.devices("gpu")[0])
        return True
    except RuntimeError:
        try:
            _ = jax.device_put(jax.numpy.ones(1), device=jax.devices("tpu")[0])
            return True
        except RuntimeError:
            return False


def main():
    args = jaxref_parser.parse_args()
    model = models.read_model(args.model)
    initial_bfactors = model.get_column_data("temp_fac")
    exp_map = maps.Map.from_file(args.map)
    path_to_model = pathlib.Path(model.filename)

    if args.output_dir == "":
        output_dir = pathlib.Path(path_to_model.stem)
    else:
        output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    patience = args.patience if args.patience != -1 else np.inf

    refiner = jax_gmm.BfactorRefiner(model, exp_map, args.n_points, args.n_neighbours)
    if jax_has_gpu_or_tpu():
        refiner.fit(args.max_steps, patience, warmup=args.dont_warmup)
    else:
        refiner.fit_with_python_loop(args.max_steps, patience, warmup=args.dont_warmup)

    model_with_bfactors = refiner.get_model()
    model_with_xray_bfactors = model_with_bfactors.copy()
    model_with_xray_bfactors.set_columns(
        "temp_fac",
        model_with_xray_bfactors.get_column_data("temp_fac") ** 2 * 8 * np.pi**2,
    )
    model_with_xray_bfactors.write_pdb(
        output_dir / f"{path_to_model.stem}-with-xray-bfactors.pdb"
    )

    # write out model with bfactors
    model_output_path = output_dir / f"{path_to_model.stem}-with-bfactors.pdb"
    model_with_bfactors.write_pdb(model_output_path)

    # todo: add an object capable of keeping track of these parameters
    helpers.plot_and_save_line(
        refiner.losses, output_dir, title="Loss", xlabel="Iterations", ylabel="Loss"
    )
    helpers.plot_and_save_bfactors(
        initial_bfactors, refiner.bfactors**2 * 8 * np.pi**2, output_dir
    )

    # simulate the map based on the bfactors
    bfactor_map = blur.simulate_map.blur_structure_with_integrated_scattering_potential(
        models.remove_hydrogens(model_with_bfactors),
        exp_map,
    )
    if args.save_simulated_map:
        bfactor_map.write_mrc(output_dir / "simulated-map.mrc")

    original_model = model_with_bfactors.copy()
    original_model.set_columns("temp_fac", (initial_bfactors / (8 * np.pi**2)) ** 0.5)
    global_resolution_map = (
        blur.simulate_map.blur_structure_with_integrated_scattering_potential(
            models.remove_hydrogens(original_model),
            exp_map,
        )
    )
    ccc_no_bfactors = helpers.ccc(exp_map, global_resolution_map)
    print(f"CCC value for blurring with ORIGINAL bfactors: {ccc_no_bfactors}")
    ccc_with_bfactors = helpers.ccc(exp_map, bfactor_map)
    print(f"CCC value for blurring with REFINED bfactors: {ccc_with_bfactors}")


jaxref_parser = argparse.ArgumentParser(
    "JaxRef Bfactor Refine - refine B-factors using gradient descent optimisation"
)
jaxref_parser.add_argument(
    "--model",
    help="Path to the pdb/cif file containing model information.",
    required=True,
    type=str,
)
jaxref_parser.add_argument(
    "--map",
    help="Path to file containing the em map, should be .mrc format.",
    required=True,
    type=str,
)

bfac_args = jaxref_parser.add_argument_group("B-factor refinement args")
bfac_args.add_argument(
    "--n-points",
    help="Compare N points per atom, per iteration. Default: 5.",
    default=5,
    type=int,
    dest="n_points",
)
bfac_args.add_argument(
    "--n-neighbours",
    help="Sum intensity contributions from N nearest neighbouring atoms, per atom. Default: 24",
    default=24,
    type=int,
    dest="n_neighbours",
)

convergence_args = jaxref_parser.add_argument_group("Convergence")
convergence_args.add_argument(
    "--max-steps",
    help="Maximum number of refinement steps. Default: 5000",
    default=5000,
    type=int,
    dest="max_steps",
)
convergence_args.add_argument(
    "--patience",
    help="Finish refinement if loss doesn't improve after this many iterations. "
    "Set to -1 to not check for convergence. Default: 250",
    default=250,
    type=int,
)
convergence_args.add_argument(
    "--dont-warmup",
    help="Don't do a coarse 'warm-up' refinement to find good starting parameters",
    action="store_false",
)

output_args = jaxref_parser.add_argument_group("Output")
output_args.add_argument(
    "--output-dir",
    help="Write output files to this directory. Default: stem of input file, e.g. for 7kx7.pdb output would be 7kx7/",
    required=False,
    default="",
    dest="output_dir",
)
output_args.add_argument(
    "--save-simulated-map",
    help="Write out the simulated map, generated using refined b-factors, as an .mrc file.",
    action="store_true",
)


if __name__ == "__main__":
    main()
