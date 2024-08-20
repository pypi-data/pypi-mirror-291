# B-FASTor
![pipeline_status](https://gitlab.com/JoeBeton/jaxref/badges/main/pipeline.svg)
![coverage](https://gitlab.com/JoeBeton/jaxref/badges/main/coverage.svg)

Rapid refinement of atomic B-factors for cryo-EM derived models using the [Jax](https://github.com/google/jax) library.

## Installation

To install the CPU only version of B-FASTor run:
```
pip install bfastor
```

To install B-FASTor configured to run on NVIDIA GPUs, run: 
```
pip install bfastor[cuda12]
```

If you have access to Google's TPU accelerators, it is possible to install a TPU compatible 
version of B-FASTor with the commands:
```
pip install -U "jax[tpu]" -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
pip install bfastor
```

## Usage
B-FASTor can be used a CLI application, via the `bfastor-refine` command. This 
can be run on any map/model combination using the following command:

``` 
bfastor-refine --model path/to/file.pdb --map path/to/map.mrc
```

The output files, including plotting B-factors, and model with refined B-factors will be saved in a folder 
with the name of the input model file, e.g. for the model `7kx7.pdb` the output will be saved in `7kx7/`.  

## Support
If you have any issues please raise them in the issues page. 

## Authors and acknowledgment
B-FASTor is developed and maintained by Joseph Beton, working within Professor Maya Topf's research group 
at the CSSB/Leibniz Institute for virology in Hamburg, Germany. 

## License
B-fastor is licensed under the MIT-license. The full license is [here](LICENSE.txt)