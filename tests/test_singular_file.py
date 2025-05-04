import os
import tempfile
import shutil
from instance_loader.dataset import GVCInstances

def manual_test_gvcinstances_all():
    """
    Manual test: download and load all instances from the GVC repository.
    """
    tmpdir = tempfile.mkdtemp()
    print(f"[All] Using temporary directory: {tmpdir}")

    try:
        # Instantiate and download all files
        ds = GVCInstances(
            root=tmpdir,
            download=True
        )

        count = len(ds)
        print(f"[All] Number of instances loaded: {count}")
        assert count > 0, "Expected at least one instance from the repo"

        # List files on disk
        raw_dir = os.path.join(tmpdir, 'raw')
        files_on_disk = sorted(os.listdir(raw_dir)) if os.path.isdir(raw_dir) else []
        print("[All] Files in raw directory:")
        for f in files_on_disk:
            print("  -", f)
        assert files_on_disk, "No files were downloaded into raw/"

        # Compare dataset.files to actual files
        loaded = sorted(os.path.basename(p) for p in ds.files)
        assert loaded == files_on_disk, (
            f"Dataset files {loaded} != raw/ contents {files_on_disk}"
        )

        # Spot–check that each loaded sample has the new 'edges' key
        sample = ds[0]
        assert 'num_nodes' in sample, "'num_nodes' missing from sample."
        assert 'edges' in sample,    "'edges' missing from sample."
        print("[All] Sample has edges; manual test passed ✅\n")

    except Exception as e:
        print("[All] Manual test failed ❌")
        print(e)
    finally:
        shutil.rmtree(tmpdir)
        print(f"[All] Cleaned up {tmpdir}\n")


def manual_test_gvcinstances_subset():
    """
    Manual test: load a specific subset of instances without using the dataset's download method.
    """
    tmpdir = tempfile.mkdtemp()
    raw_dir = os.path.join(tmpdir, 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    print(f"[Subset] Using temporary directory: {tmpdir}")

    try:
        # 1) Hardcoded subset filenames
        subset_files = [
            "1-FullIns_3.col.gz",
            "2-FullIns_4.col.gz"
        ]
        print(f"[Subset] Subset filenames: {subset_files}")

        # 2) Instantiate dataset with download=True and filter by filenames
        ds_sub = GVCInstances(
            root=tmpdir,
            download=True,
            instances=subset_files
        )

        # 3) Verify only those files were downloaded
        downloaded = sorted(os.listdir(raw_dir)) if os.path.isdir(raw_dir) else []
        print(f"[Subset] Files in raw directory: {downloaded}")
        assert set(downloaded) == set(subset_files), (
            f"Expected only {subset_files}, got {downloaded}"
        )

        # 4) Verify dataset.files matches downloaded
        loaded = [os.path.basename(p) for p in ds_sub.files]
        assert set(loaded) == set(subset_files), (
            f"Dataset files {loaded} != raw/ contents {downloaded}"
        )
        assert len(ds_sub) == len(subset_files), "Dataset length mismatch for subset"

        # 5) Inspect each data item for the new 'edges' format
        for data in ds_sub:
            print(f"[Subset] Sample num_nodes: {data['num_nodes']}")
            # New check: edges is a non-empty list of 2-element sets
            assert 'edges' in data, "'edges' missing from data"
            edges = data['edges']
            print(f"[Subset] Edges: {edges}")
            assert isinstance(edges, list),    "Expected 'edges' to be a list"
            assert edges,                     "Expected at least one edge"
            for edge in edges:
                assert isinstance(edge, set), "Each edge should be a set"
                assert len(edge) == 2,       "Each edge-set should contain exactly two nodes"

        print("[Subset] Manual test passed ✅\n")

    except Exception as e:
        print("[Subset] Manual test failed ❌")
        print(e)
    finally:
        shutil.rmtree(tmpdir)
        print(f"[Subset] Cleaned up {tmpdir}\n")


if __name__ == '__main__':
    # manual_test_gvcinstances_all()
    manual_test_gvcinstances_subset()
