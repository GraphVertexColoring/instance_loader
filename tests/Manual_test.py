import os
import tempfile
import shutil
from instance_loader.dataset import ColDataset

def manual_test_download_and_parse_col_gz_files():
    tmpdir = tempfile.mkdtemp()
    print(f"Using temporary directory: {tmpdir}")

    try:
        dataset = ColDataset(
            root=tmpdir,
            user='GraphVertexColoring',
            repo='gvc-instances',
            dir='Instances',
            branch='master',
            download=True
        )

        print(f"Number of files loaded: {len(dataset)}")
        assert len(dataset) > 0, "No files were loaded."

        # List the downloaded .col.gz files
        raw_dir = os.path.join(tmpdir, 'raw')
        if os.path.exists(raw_dir):
            col_files = [f for f in os.listdir(raw_dir) if f.endswith('.col.gz')]
            print("\nLoaded .col.gz files:")
            for f in col_files:
                print(f"- {f}")
        else:
            print("Raw directory not found. Cannot list .col.gz files.")

        # Grab a sample and inspect its structure
        sample = dataset[0]
        print("Sample keys:", sample.keys())
        assert 'num_nodes' in sample, "'num_nodes' missing from sample."
        assert 'edges' in sample,    "'edges' missing from sample."

        # Validate edges structure
        edges = sample['edges']
        assert isinstance(edges, list),      "Expected 'edges' to be a list."
        assert len(edges) > 0,               "Expected at least one edge."
        for edge in edges:
            assert isinstance(edge, set),    f"Edge {edge} is not a set."
            assert len(edge) == 2,           f"Edge {edge} does not have exactly two nodes."

        print("Test passed ✅")

    except Exception as e:
        print("Test failed ❌")
        print(e)

    finally:
        shutil.rmtree(tmpdir)
        print("Temporary directory cleaned up.")

if __name__ == "__main__":
    manual_test_download_and_parse_col_gz_files()
