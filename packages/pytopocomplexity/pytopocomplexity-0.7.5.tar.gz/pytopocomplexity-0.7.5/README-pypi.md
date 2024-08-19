# pyTopoComlexity
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11239338.svg)](https://doi.org/10.5281/zenodo.11239338)

**pyTopoComplexity** is an open-source Python package designed to measure the topographic complexity (i.e., surface roughness) of land surfaces using digital elevation model (DEM) data. This package includes modules for three methods commonly used in the fields of geomorphology and oceanography for measuring topographic complexity, which are not fully available in Geographic Information System (GIS) software like QGIS.

| Modules  | Classes | Method Descriptions |
| ------------- | ------------- | ------------- |
| pycwtmexhat.py | CWTMexHat | Quanitfy the wavelet-based curvature of the terrain surface using two-dimensional continuous wavelet transform (2D-CWT) with a Mexican Hat wevalet |
| pyfracd.py | FracD | Conduct fractal dimension analysis on the terrain surface using variogram procedure |
| pyrugostiy.py | RugosityIndex | Calculate rugosity index of the terrain surface |

## Installation

```
pip install pytopocomplexity
```

## Modules for Surface Complexity Measurement

### 1. Two-Dimensional Continuous Wavelet Transform Analysis

```python
from pytopocomplexity import CWTMexHat
```

The module **pycwtmexhat.py** uses two-dimensional continuous wavelet transform (2D-CWT) with a Mexican Hat wevalet to measure the topographic complexity (i.e., surface roughness) of a land surface from a Digital Elevation Model (DEM). Such method quanitfy the wavelet-based curvature of the surface, which has been proposed to be a effective geomorphic metric for identifying and estimating the ages of historical deep-seated landslide deposits.

The method and early version of the code was developed by Dr. Adam M. Booth (Portland State Univeristy) in [2009](https://doi.org/10.1016/j.geomorph.2009.02.027), written in MATLAB (Source code available from [Booth's personal website](https://web.pdx.edu/~boothad/tools.html)). This MATLAB code was later revised and adapted by Dr. Sean R. LaHusen (Univeristy of Washington) and Dr. Erich N. Herzig (Univeristy of Washington) in their research ([LaHusen et al., 2020](https://doi.org/10.1126/sciadv.aba6790); [Herzig et al. (2023)](https://doi.org/10.1785/0120230079)). Dr. Larry Syu-Heng Lai (Univeristy of Washington), under the supervision of Dr. Alison R. Duvall (Univeristy of Washington), translated the code into this optimized open-source Python version in 2024.

### 2. Fractal Dimentsion Analysis

```python
from pytopocomplexity import FracD
```

The **pyfracd.py** module calculates local fractal dimensions to assess topographic complexity. It also computes reliability parameters such as the standard error and the coefficient of determination (R²). The development of this module was greatly influenced by the Fortran code shared by Dr. Eulogio Pardo-Igúzquiza from his work in [Pardo-Igúzquiza and Dowd (2022)](https://doi.org/10.1016/j.icarus.2022.115109).

The local fractal dimension is determined by intersecting the surface within a moving window with four vertical planes in principal geographical directions, simplifying the problem to one-dimensional topographic profiles. The fractal dimension of these profiles is estimated using the variogram method, which models the relationship between dissimilarity and distance using a power-law function. While the fractal dimension value does not directly scale with the degree of surface roughness, smoother or more regular surfaces generally have lower fractal dimension values (closer to 2), whereas surfaces with higher fractal dimension values tend to be more complex or irregular. This method has been applied in terrain analysis for understanding spatial variability in surface roughness, classifying geomorphologic features, uncovering hidden spatial structures, and supporting geomorphological and geological mapping on Earth and other planetary bodies.

### 3. Rugosity Index Calculation

```python
from pytopocomplexity import RugosityIndex
```

The module **pyrugosity.py** measure rugosity index of the land surface, which is widely used to assess landscape structural complexity.

By definition, the rugosity index has a minimum value of one, representing a completely flat surface. Typical values of the conventional rugosity index without slope correction ([Jenness, 2004](https://onlinelibrary.wiley.com/doi/abs/10.2193/0091-7648%282004%29032%5B0829%3ACLSAFD%5D2.0.CO%3B2)) range from one to three, although larger values are possible in very steep terrains. The slope-corrected rugosity index, also known as the Arc-Chord Ratio (ACR) rugosity index ([Du Preez, 2015](https://doi.org/10.1007/s10980-014-0118-8)), provides a better representation of local surface complexity. This method has been applied in classifying seafloor types by marine geologists and geomorphologists, studying small-scale hydrodynamics by oceanographers, and assessing available habitats in landscapes by ecologists and coral biologists.

## Requirements
For `pytopocomplexity` package
* Python >= 3.10
* `numpy` >= 1.24
* `scipy` >= 1.10
* `rasterio` >= 1.3
* `dask` >= 2024.3
* `matplotlib` >= 3.7
* `tqdm` >= 4.66
* `numba` >= 0.57
* `statsmodels` >= 0.14

## License
**pyTopoComlexity** is licensed under the [Apache License 2.0](LICENSE).
