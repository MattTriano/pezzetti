import datetime as dt
import json
import os
import shutil
from typing import Dict, List, Union, Optional

from bs4 import BeautifulSoup
import requests

from pezzetti.utils import get_global_root_data_dir


class CensusMetadataNode:
    root_node_url = "https://www2.census.gov"

    def __init__(self, url: str, root_data_dir: os.path = get_global_root_data_dir()):
        self.url = url
        self.root_data_dir = root_data_dir
        self.node_data_relpath = os.sep.join(self.url.strip(self.root_node_url).split("/"))
        self.child_nodes = {}
        self.is_root_node = self.url == self.root_node_url
        self.set_node_data_dir()
        self.node_metadata_file_path = os.path.join(self.node_data_dir, "node_metadata.json")
        self.scrape_child_node_metadata()
        self._count_child_node_dirs_and_files()
        self.set_last_modified_date()
        self.set_node_metadata()

    def set_node_data_dir(self) -> None:
        self.node_data_dir = os.path.join(self.root_data_dir, "us_census", self.node_data_relpath)
        os.makedirs(self.node_data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.node_data_dir, "archive"), exist_ok=True)

    def _is_node_a_dir(self, url: str) -> bool:
        return (url.endswith("/")) or (url == self.root_node_url)

    def _parse_last_mod_date_str(self, node_date_str: str) -> str:
        node_date = dt.datetime.strptime(node_date_str, "%d-%b-%Y %H:%M")
        return node_date.strftime("%Y_%m_%d__%H%M")

    def _extract_node_data_from_row(self, row_elements: List) -> Dict:
        child_name = row_elements[1].find("a").get("href")
        child_url = "/".join([self.url, child_name])
        child_date_str = self._parse_last_mod_date_str(node_date_str=row_elements[2].text.strip())
        child_node_size = row_elements[3].text.strip()
        child_node_descr = row_elements[4].text.strip()
        return {
            "url": child_url,
            "name": child_name,
            "last_modified": child_date_str,
            "size": child_node_size,
            "description": child_node_descr,
            "is_file": (child_node_size != "-"),
        }

    def scrape_child_node_metadata(self) -> None:
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, features="lxml")
        html_table_rows = soup.find_all("tr")

        if self.is_root_node:
            index_of_first_data_row = 2
        else:
            index_of_first_data_row = 3
        index_of_last_data_row = len(html_table_rows) - 2

        for row_index in range(index_of_first_data_row, index_of_last_data_row + 1):
            html_table_row_elements = html_table_rows[row_index].find_all("td")
            if len(html_table_row_elements) == 5:
                row_data = self._extract_node_data_from_row(row_elements=html_table_row_elements)
                self.child_nodes[row_data["url"]] = row_data
            else:
                pass

    def get_child_dir_nodes(self) -> List:
        child_dir_nodes = []
        for child_node in self.child_nodes.values():
            if self._is_node_a_dir(url=child_node["url"]):
                child_dir_nodes.append(child_node)
        return child_dir_nodes

    def get_child_file_nodes(self) -> List:
        child_file_nodes = []
        for child_node in self.child_nodes.values():
            if not self._is_node_a_dir(url=child_node["url"]):
                child_file_nodes.append(child_node)
        return child_file_nodes

    def _count_child_node_dirs_and_files(self) -> None:
        self.child_node_dir_count = 0
        self.child_node_file_count = 0
        for child_node in self.child_nodes.values():
            if self._is_node_a_dir(child_node["url"]):
                self.child_node_dir_count = self.child_node_dir_count + 1
            else:
                self.child_node_file_count = self.child_node_file_count + 1

    def _get_date_of_most_recently_modified_child_node(self) -> str:
        latest_mod_date = "0"
        for child_node in self.child_nodes.values():
            if child_node["last_modified"] > latest_mod_date:
                latest_mod_date = child_node["last_modified"]
        return latest_mod_date

    def set_last_modified_date(self) -> None:
        self.last_modified_date = self._get_date_of_most_recently_modified_child_node()

    def _read_latest_node_metadata_file(self) -> Dict:
        if os.path.isfile(self.node_metadata_file_path):
            with open(self.node_metadata_file_path) as mfile:
                return json.load(mfile)
        else:
            return None

    def _save_node_metadata(self) -> None:
        with open(self.node_metadata_file_path, "w", encoding="utf-8") as mfile:
            json.dump(self.node_metadata, mfile, ensure_ascii=False, indent=4, default=str)

    def set_node_metadata(self) -> None:
        self.node_metadata = {
            "url": self.url,
            "last_modified": self.last_modified_date,
            "is_root_node": self.is_root_node,
            "child_nodes": self.child_nodes,
            "child_dir_nodes": self.child_node_dir_count,
            "child_file_nodes": self.child_node_file_count,
        }

    def get_last_modified_date_of_latest_node_cache(self) -> str:
        if os.path.isfile(self.node_metadata_file_path):
            cached_node = self._read_latest_node_metadata_file()
            cached_node_last_modified = cached_node["last_modified"]
        else:
            cached_node_last_modified = "0"
        return cached_node_last_modified

    def archive_node_metadata_cache(self) -> None:
        cached_node_last_modified = self.get_last_modified_date_of_latest_node_cache()
        archive_file_path = os.path.join(
            os.path.dirname(self.node_metadata_file_path),
            "archive",
            f"node_metadata_{cached_node_last_modified}.json",
        )
        shutil.copy2(self.node_metadata_file_path, archive_file_path)

    def get_updated_child_dir_nodes(self) -> List:
        cached_node_last_modified = self.get_last_modified_date_of_latest_node_cache()
        if self.last_modified_date > cached_node_last_modified:
            cached_node = self._read_latest_node_metadata_file()
            if cached_node is None:
                updated_dir_nodes = self.get_child_dir_nodes()
            else:
                updated_dir_nodes = []
                for child_dir_node_url, child_dir_node_data in self.get_child_dir_nodes().items():
                    if (child_dir_node_url in cached_node) and (
                        child_dir_node_data["last_modified"]
                        <= cached_node[child_dir_node_url]["last_modified"]
                    ):
                        pass
                    else:
                        updated_dir_nodes.append({child_dir_node_url: child_dir_node_data})
            return updated_dir_nodes
