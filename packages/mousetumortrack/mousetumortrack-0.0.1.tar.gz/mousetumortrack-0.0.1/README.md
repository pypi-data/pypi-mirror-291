![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 💫 Tumor nodules tracking in mice CT scans

We provide a Python package for tracking tumor nodules in mice CT scans. The project is based on [Trackpy](https://github.com/soft-matter/trackpy) and [Laptrack](https://github.com/yfukai/laptrack/tree/main) (algorithms from both libraries are implemented). It also provides a registration utility to align CT scans before tracking objects based on segmentation masks of the lungs cavity produced by the [mouselungseg](https://gitlab.com/epfl-center-for-imaging/mouselungseg) model.

[[`Installation`](#installation)] [[`Usage`](#usage)]

This project is part of a collaboration between the [EPFL Center for Imaging](https://imaging.epfl.ch/) and the [De Palma Lab](https://www.epfl.ch/labs/depalma-lab/).

## Installation

We recommend performing the installation in a clean Python environment. Install our package from PyPi:

```sh
pip install mousetumortrack
```

or from the repository:

```sh
pip install git+https://github.com/EPFL-Center-for-Imaging/mousetumortrack.git
```

or clone the repository and install with:

```sh
git clone git+https://github.com/EPFL-Center-for-Imaging/mousetumortrack.git
cd mouselungseg
pip install -e .
```

## Usage

Track tumor nodules from a labelled 3D timesereies array:

```py
from mousetumortrack import run_tracking

# labels_timeseries is a 4D array of shape (TZYX)
linkage_df, grouped_df, labels_timeseries_tracked = run_tracking(labels_timeseries)
```

For more details, see [example.py](./scripts/example.py).

## Issues

If you encounter any problems, please file an issue along with a detailed description.

## License

This project is licensed under the [BSD-3](LICENSE.txt) license.

## Related projects

- [Mouse Tumor Net](https://gitlab.com/epfl-center-for-imaging/mousetumornet) | Detect tumor nodules in mice CT scans.
- [Mouse Lungs Seg](https://gitlab.com/epfl-center-for-imaging/mouselungseg) | Detect the lungs cavity in mice CT scans.