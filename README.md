# test
This package is meant to function as a pytorch like instance downloader which should mitigate storing the actual instances on local hardware, and instead load the needed information into memory when needed, to run Graph-Vertex Coloring algorithms and heuristics on.

A test of the usage of this package can be found under tests/.

# graph-col-loader

A PyTorch dataset loader for DIMACS `.col.gz` graph coloring instances hosted on GitHub.

## Installation

To install this package, simply clone this repository.
Navigate into the directory of the cloned repo.

Then run the following command: pip install .

## Example usage

```python
from graph_col_loader import ColDataset

ds = GVCInstances(
    root=tmpdir,
    download=True
)
print(dataset[0])
