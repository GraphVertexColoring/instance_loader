import os
from torch.utils.data import Dataset
import requests
from instance_loader.parser import read_dimacs
from instance_loader.utils import list_col_files

class ColDataset(Dataset):
    def __init__(self,root, user, repo, dir, branch='main', transform=None, download=False, instances: list[str] = None):
        self.root = os.path.expanduser(root)
        self.raw_dir = os.path.join(self.root, 'raw')
        self.transform = transform
        self.user = user
        self.repo = repo
        self.dir = dir
        self.branch = branch

        if download:
            self.download(instances)

        # builds the list of all filepaths
        all_urls = list_col_files(self.user, self.repo, self.dir, self.branch)
        all_paths = [os.path.join(self.raw_dir, os.path.basename(u)) for u in all_urls]

        # filters the files to only include the user specified ones if any
        if instances:
            basenames = set(instances)
            self.files = [p for p in all_paths if os.path.basename(p) in basenames]
        else:
            self.files = all_paths

    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, idx):
        path = self.files[idx]
        num_nodes, edges = read_dimacs(path)  # edges is a List[Set[int]]
        
        data = {
            'num_nodes': num_nodes,
            'edges': edges  # edges as list of sets, e.g., [{0, 1}, {1, 2}]
        }

        return self.transform(data) if self.transform else data

    def download(self, instances=None):
        os.makedirs(self.raw_dir, exist_ok=True)

        if instances:
            basenames = set(instances)
            all_urls = list_col_files(self.user, self.repo, self.dir, self.branch)
            urls = [u for u in all_urls if os.path.basename(u) in basenames]
        else:
            urls = list_col_files(self.user, self.repo, self.dir, self.branch)

        for url in urls:
            filename = os.path.basename(url)
            filepath = os.path.join(self.raw_dir, filename)
            if not os.path.exists(filepath):
                response = requests.get(url)
                response.raise_for_status()
                with open(filepath, 'wb') as f:
                    f.write(response.content)



##
# Convenience instance, that always takes directly from the repo that it is intended to be used for.
##
def GVCInstances(root: str ="root", tranform=None, download: bool = False, instances: list[str] = None):
    return ColDataset(
        root = root,
        user='GraphVertexColoring',
        repo='gvc-instances',
        dir='Instances',
        branch='master',
        transform=tranform,
        download=download,
        instances=instances
    )
