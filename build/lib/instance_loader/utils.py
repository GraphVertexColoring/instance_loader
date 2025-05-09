from torchvision.datasets.utils import download_url
import requests

# takes a user/org name, a repository and a directory to search for all .col files
# should be modified to col.gz files later
def list_col_files(user, repo, directory, branch='main'):
    api_url = f'https://api.github.com/repos/{user}/{repo}/contents/{directory}?ref={branch}'
    response = requests.get(api_url)
    response.raise_for_status()
    contents = response.json()
    
    col_files = [
        f'https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file["path"]}'
        for file in contents if file['name'].endswith('.col.gz')
    ]
    return col_files
