import os

from pezzetti.utils import get_global_root_data_dir

class CensusMetadataNode:
    root_node_url = "https://www2.census.gov"

    def __init__(self, url: str, root_data_dir: os.path = get_global_root_data_dir()):
        self.url = url
        self.root_data_dir = root_data_dir
        self.child_nodes = {}
        self.is_root_node = (self.url == root_node_url)
        self.isdir = self._is_node_a_dir()
        self.set_local_dataset_dir()

    def set_local_dataset_dir(self) -> None:
        self.local_dataset_dir = os.path.join(
            self.root_data_dir, "us_census",  
            os.sep.join(self.url.strip(root_node_url).split("/"))
        )
        os.makedirs(self.local_dataset_dir, exist_ok=True)

    def _is_node_a_dir(self) -> bool:
        return self.url.endswith("/")