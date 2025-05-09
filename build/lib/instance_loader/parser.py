import gzip

def read_dimacs(path: str):
    open_fn = gzip.open if path.endswith('.gz') else open

    with open_fn(path, 'rt') as f:
        num_nodes = 0
        edges = []
        for line in f:
            if line.startswith('p'):
                _, _, n, _ = line.split()
                num_nodes = int(n)
            elif line.startswith('e'):
                _, u, v = line.split()
                edges.append({int(u)-1, int(v)-1})
    return num_nodes, edges
