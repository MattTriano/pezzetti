from datetime import datetime
import os
import requests
from typing import Dict, List, Union, Optional

from pezzetti.utils import extract_file_from_url, get_global_root_data_dir

import requests


class SocrataMetadata:
    def __init__(self, table_id: str, root_data_dir: os.path = get_global_root_data_dir()) -> None:
        self.table_id = table_id
        self.root_data_dir = root_data_dir
        self.set_table_metadata()
        self.set_data_domain()
        self.set_table_name()
        self.set_table_data_dir()
        self.table_has_geospatial_data()
        self.set_table_data_dirs()
        self.set_file_extension()
        self.set_metadata_file_name()
        self.set_data_file_name()
        self.set_metadata_file_path()
        self.set_data_raw_file_path()

    def set_table_metadata(self) -> None:
        api_call = f"http://api.us.socrata.com/api/catalog/v1?ids={self.table_id}"
        response = requests.get(api_call)
        if response.status_code == 200:
            response_json = response.json()
            results = {"_id": self.table_id, "time_of_collection": datetime.utcnow()}
            results.update(response_json["results"][0])
            self.table_metadata = results

    def get_table_metadata(self) -> Optional[Dict]:
        if self.table_metadata is None:
            self.set_table_metadata()
        if self.table_metadata is not None:
            return self.table_metadata
        else:
            print("Couldn't retrieve table_metadata. Debug this issue.")

    def set_data_domain(self) -> str:
        self.data_domain = self.table_metadata["metadata"]["domain"]

    def table_has_geo_type_view(self) -> bool:
        return self.table_metadata["resource"]["lens_view_type"] == "geo"

    def table_has_map_type_display(self) -> bool:
        return self.table_metadata["resource"]["lens_display_type"] == "map"

    def get_columns_datatype(self):
        return self.table_metadata["resource"]["columns_datatype"]

    def table_has_data_columns(self) -> bool:
        """TODO: fix this. I think this is only checking the number of data columns
        *documented by the table owner*"""
        return len(self.table_metadata["resource"]["columns_name"]) != 0

    def set_table_name(self) -> None:
        table_name = self.table_metadata["resource"]["name"]
        self.table_name = "_".join(table_name.split())

    def set_table_data_dir(self) -> None:
        self.table_data_dir = os.path.join(self.root_data_dir, self.data_domain, self.table_name)
        os.makedirs(self.table_data_dir, exist_ok=True)

    def set_table_data_dirs(self) -> None:
        self.table_metadata_dir = os.path.join(self.table_data_dir, "metadata")
        os.makedirs(self.table_metadata_dir, exist_ok=True)
        self.table_data_raw_dir = os.path.join(self.table_data_dir, "raw")
        os.makedirs(self.table_data_raw_dir, exist_ok=True)
        self.table_data_intermediate_dir = os.path.join(self.table_data_dir, "intermediate")
        os.makedirs(self.table_data_intermediate_dir, exist_ok=True)
        self.table_data_clean_dir = os.path.join(self.table_data_dir, "clean")
        os.makedirs(self.table_data_clean_dir, exist_ok=True)

    def get_valid_geospatial_export_formats(self) -> Dict:
        valid_export_formats = {
            "shp": "Shapefile",
            "shapefile": "Shapefile",
            "geojson": "GeoJSON",
            "kmz": "KMZ",
            "kml": "KML",
        }
        return valid_export_formats

    def table_has_geo_column(self) -> bool:
        socrata_geo_datatypes = [
            "Line",
            "Location",
            "MultiLine",
            "MultiPoint",
            "MultiPolygon",
            "Point",
            "Polygon",
        ]
        table_column_datatypes = self.get_columns_datatype()
        table_has_geo_column = any(
            [table_col_dtype in socrata_geo_datatypes for table_col_dtype in table_column_datatypes]
        )
        return table_has_geo_column

    def table_has_geospatial_data(self) -> None:
        self.is_geospatial = (
            (not self.table_has_data_columns())
            and (self.table_has_geo_type_view() or self.table_has_map_type_display())
        ) or (self.table_has_geo_column())

    def _format_geospatial_export_format(self, export_format: str) -> str:
        valid_export_formats = self.get_valid_geospatial_export_formats()
        if export_format in valid_export_formats.values():
            return export_format
        else:
            assert export_format.lower() in valid_export_formats.keys(), "Invalid geospatial format"
            return valid_export_formats[export_format.lower()]

    def get_data_download_url(self, export_format: str = "Shapefile") -> str:
        export_format = self._format_geospatial_export_format(export_format=export_format)
        domain = self.data_domain
        if self.table_metadata.is_geospatial:
            return f"https://{domain}/api/geospatial/{self.table_id}?method=export&format={export_format}"
        else:
            return f"https://{domain}/api/views/{self.table_id}/rows.csv?accessType=DOWNLOAD"

    def set_file_extension(self):
        if self.is_geospatial:
            self.file_ext = "geojson"
        else:
            self.file_ext = "csv"

    def set_metadata_file_name(self) -> None:
        self.metadata_file_name = f"{self.table_name}.json"

    def set_data_file_name(self) -> None:
        self.data_file_name = f"{self.table_name}.{self.file_ext}"

    def set_metadata_file_path(self) -> None:
        self.metadata_file_path = os.path.join(self.table_metadata_dir, self.metadata_file_name)

    def set_data_raw_file_path(self) -> None:
        self.data_raw_file_path = os.path.join(self.table_data_raw_dir, self.data_file_name)


class SocrataTable:
    def __init__(
        self,
        table_id: str,
        root_data_dir: os.path = get_global_root_data_dir(),
        verbose: bool = False,
    ) -> None:
        self.table_id = table_id
        self.verbose = verbose
        self.metadata = SocrataMetadata(table_id=table_id, root_data_dir=root_data_dir)
