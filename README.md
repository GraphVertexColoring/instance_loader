# test
This package is mean to function as a pytorch like instance downloader which should mitigate storing the actual instances on local hardware, and instead load the needed information into memory when needed, to run Graph-Vertex Coloring algorithms and heuristics on.

A test of the usage of this package can be found under tests/.

# graph-col-loader

A PyTorch dataset loader for DIMACS `.col.gz` graph coloring instances hosted on GitHub.

## Example usage

```python
from graph_col_loader import ColDataset

dataset = ColDataset(
    root='data',
    user='my-github',
    repo='graph-instances',
    dir='datasets',
    download=True
)

print(dataset[0])
