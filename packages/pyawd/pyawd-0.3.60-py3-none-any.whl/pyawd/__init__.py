# pyawd
# Tribel Pascal - pascal.tribel@ulb.be
r"""
# pyawd
Pyawd (standing for Pytorch Acoustic Wave Dataset) is a powerful tool for building datasets containing custom simulations of the propagation of Acoustic Wave through a given medium.
It uses the finite differences scheme (implemented in the Devito package) to solve the Acoustic Wave Equation, and offers convenient tools for the customisation of the parameters, the handling of the data, the visualisation of the simulations.

## Acoustic Wave Equation
The equation of propagation of an acoustic wave is given by $\frac{d^2u}{dt^2} = c \nabla^2 u + f(x, y)$, where
- $u(x, y)$ is the displacement field, and can be either a scalar or a vector field
- $c(x, y)$ is the wave  propagation speed
- $\nabla^2$ is the _laplacian operator_
- $f(x, y)$ is an external force applied on the system, for which the value can vary through time


## Installation
The package (along with the dependencies) is accessible via [PyPI](https://pypi.org/project/PyAWD/):

```bash
pip install pyawd
```

## Documentation
The API documentation is available [here](https://pascaltribel.github.io/pyawd/).
Basic help is provided for each class and function, and is accessible via the Python `help()` function.

## Getting started

Basic imports:
```python
import pyawd
from pyawd import ScalarAcousticWaveDataset
```

Let us generate a Dataset made of 10 simulations. Each simulation is run in a $250\times 250$ matrix. We store the field state every $2$ seconds and we run the simulation for $10$ seconds:

```python
dataset = ScalarAcousticWaveDataset(2, nx=250, dt=2, t=10)
```

Then we plot the first simulation.

```python
dataset.plot_item(0)
```

Finally, we can generate a video of this simulation. We will use $200$ frames, which yields a final rate of $20 fps$:

```python
dataset.generate_video(0, "example", 200)
```


By default, the point `(0, 0)` contains an interrogator. This means that the continuous measurement on this position (at least with a $\Delta t=dt$) can be obtained by:

```python
dataset.interrogate((0, 0))
```

## More advanced usage
Using the `VectorAcousticWaveDataset` classes, you can produce simulations which are more realistic:

```python
dataset = VectorAcousticWaveDataset2D(2, nx=250, dt=2, interrogators=[(-10, 0), (10, 0)], t=10)
```

Especially, this provides measurements along orthogonal dimensions:

```python
dataset.plot_item(0)
dataset.plot_interrogators_response(0)
```


## Examples
Multiple IPython notebooks are presented in the [examples](examples/) directory. If [Jupyter](https://jupyter.org) is installed, those examples can be explored by starting Jupyter:

```bash
jupyter-notebook
```

- `ScalarAcousticWavePropagation.ipynb`: an introduction to PDE solving and simulation using Devito applied on the scalar acoustic wave propagation
- `VectorAcousticWavePropagation.ipynb`: an introduction to PDE solving and simulation using Devito applied on the vector acoustic wave propagation
- `VectorAcousticWaveDataset.ipynb`: an introduction to the VectorAcousticWaveDataset possibilities
- `Marmousi.ipynb`: a visualisation of the Marmousi velocity field used in the simulations
- `Interrogators.ipynb`: an introduction to the PyAWD Interrogators usage
- `GenerateVectorAcousticWaveDataset.ipynb`: how to generate dataset using `pyawd`

## Related Works:
- https://essd.copernicus.org/preprints/essd-2023-470/
"""
from pyawd.VelocityModel import VelocityModel
from pyawd.VelocityModel2D import VelocityModel2D
from pyawd.VelocityModel3D import VelocityModel3D
from pyawd.Marmousi import Marmousi
#from pyawd.ScalarAcousticWaveDataset import ScalarAcousticWaveDataset
from pyawd.AcousticWaveDataset import AcousticWaveDataset
from pyawd.VectorAcousticWaveDataset import VectorAcousticWaveDataset
from pyawd.VectorAcousticWaveDataset2D import VectorAcousticWaveDataset2D
from pyawd.VectorAcousticWaveDataset3D import VectorAcousticWaveDataset3D