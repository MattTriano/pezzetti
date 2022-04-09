import json
import os
from typing import Dict, List, Union, Optional

import requests


def get_socrata_table_metadata(table_id: str) -> Dict:
    api_call = f"http://api.us.socrata.com/api/catalog/v1?ids={table_id}"
    response = requests.get(api_call)
    if response.status_code == 200:
        response_json = response.json()
        results = {"_id": table_id, "time_of_collection": datetime.utcnow()}
        results.update(response_json["results"][0])
        return results


def dump_socrata_metadata_to_json(table_metadata: Dict, file_path: os.path) -> None:
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(table_metadata, json_file, ensure_ascii=False, indent=4, default=str)

