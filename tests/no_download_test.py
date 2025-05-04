import os
import shutil
import tempfile
import requests  # only if you want to fetch a sample .col.gz on the fly
from instance_loader.dataset import ColDataset

def manual_test_no_download():
    # 1) Prepare a temp dir and raw/ subfolder
    tmpdir = tempfile.mkdtemp()
    raw_dir = os.path.join(tmpdir, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    print(f"Prepared raw dir at: {raw_dir}\n")

    # 2) Option A: Copy an existing local .col.gz into raw/
    #    (Uncomment & adjust the path if you already have one)
    #
    # src_gz = "/path/to/local/your_sample.col.gz"
    # dst = os.path.join(raw_dir, os.path.basename(src_gz))
    # shutil.copy(src_gz, dst)
    # print(f"Copied local sample to {dst}")

    # 2) Option B: Download one sample on the fly for testing
    sample_url = (
        "https://raw.githubusercontent.com/"
        "GraphVertexColoring/gvc-instances/master/Instances/"
        "1-FullIns_3.col.gz"
    )
    dst = os.path.join(raw_dir, os.path.basename(sample_url))
    print("Downloading a single .col.gz for no-download test:")
    resp = requests.get(sample_url)
    resp.raise_for_status()
    with open(dst, "wb") as f:
        f.write(resp.content)
    print(f"  → Saved to {dst}\n")

    # 3) Now instantiate dataset with download=False
    dataset = ColDataset(
        root=tmpdir,
        user="GraphVertexColoring",   # args only matter if download=True
        repo="gvc-instances",
        dir="Instances",
        branch="master",
        download=False                # do NOT try to fetch anything
    )

    # 4) Check that it found the file(s)
    print(f"Dataset length (should be >=1): {len(dataset)}")
    assert len(dataset) >= 1, "Dataset did not pick up the pre-seeded file."

    # List all loaded files
    print("Loaded files:")
    for path in dataset.files:
        print("  -", os.path.basename(path))

    # 5) Fetch and inspect the single sample
    sample = dataset[0]
    print("Sample keys:", sample.keys())
    assert 'num_nodes' in sample, "'num_nodes' missing from sample."
    assert 'edges' in sample,    "'edges' missing from sample."

    edges = sample['edges']
    print(f"  num_nodes → {sample['num_nodes']}")
    print(f"  edges     → {edges}")

    # Validate edges structure
    assert isinstance(edges, list),      "Expected 'edges' to be a list."
    assert len(edges) > 0,               "Expected at least one edge."
    for edge in edges:
        assert isinstance(edge, set),    f"Edge {edge} is not a set."
        assert len(edge) == 2,           f"Edge {edge} does not have exactly two nodes."

    print("\nNo‐download test passed ✅")

    # 6) Cleanup
    shutil.rmtree(tmpdir)
    print("Cleaned up temporary directory.")

if __name__ == "__main__":
    manual_test_no_download()
