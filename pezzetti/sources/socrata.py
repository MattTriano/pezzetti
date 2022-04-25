import datetime as dt
from hashlib import sha256
import json
import os
import requests
import shutil
from typing import Dict, List, Union, Optional

import geopandas as gpd
import pandas as pd

from pezzetti.utils import extract_file_from_url, get_global_root_data_dir
from pezzetti.errors import DataMetadataParityError


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
            results = {"_id": self.table_id, "time_of_collection": dt.datetime.utcnow()}
            results.update(response_json["results"][0])
            self.table_metadata = results
            self.set_hash_of_column_details()

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
        os.makedirs(os.path.join(self.table_metadata_dir, "archive"), exist_ok=True)
        self.table_data_raw_dir = os.path.join(self.table_data_dir, "raw")
        os.makedirs(os.path.join(self.table_data_raw_dir, "archive"), exist_ok=True)
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

    def get_data_download_url(self, export_format: str = "GeoJSON") -> str:
        export_format = self._format_geospatial_export_format(export_format=export_format)
        domain = self.data_domain
        if self.is_geospatial:
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

    def set_metadata_file_path(self) -> None:
        self.metadata_file_path = os.path.join(self.table_metadata_dir, self.metadata_file_name)

    def set_data_file_name(self) -> None:
        self.data_file_name = f"{self.table_name}.{self.file_ext}"

    def set_data_raw_file_path(self) -> None:
        self.data_raw_file_path = os.path.join(self.table_data_raw_dir, self.data_file_name)

    def set_hash_of_column_details(self) -> None:
        source_domain = self.table_metadata["metadata"]["domain"]
        table_details = self.table_metadata["resource"]
        table_description = table_details["description"]
        col_details = zip(
            table_details["columns_name"],
            table_details["columns_field_name"],
            table_details["columns_datatype"],
            table_details["columns_description"],
        )
        col_str = "".join(
            [
                name + field_name + datatype + descr
                for name, field_name, datatype, descr in col_details
            ]
        )
        prehash_str = self.table_id + source_domain + table_description + col_str
        detail_hash_str = sha256(prehash_str.encode(encoding="utf-8")).hexdigest()
        self.table_metadata["table_details_hash"] = detail_hash_str
        self.table_metadata_hash = detail_hash_str

    def save_metadata(self) -> None:
        with open(self.metadata_file_path, "w", encoding="utf-8") as mfile:
            json.dump(self.table_metadata, mfile, ensure_ascii=False, indent=4, default=str)

    def read_latest_table_metadata(self) -> Dict:
        if os.path.isfile(self.metadata_file_path):
            with open(self.metadata_file_path) as mfile:
                return json.load(mfile)
        else:
            return None

    def get_latest_update_date(self) -> dt.datetime:
        metadata_dict = self.table_metadata.copy()
        last_updated = metadata_dict["resource"]["updatedAt"]
        last_updated_date = dt.datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.000Z")
        return last_updated_date

    def get_latest_update_date_of_saved_metadata(self) -> dt.datetime:
        assert os.path.isfile(self.metadata_file_path), "No saved metadata files found"
        metadata_dict = self.read_latest_table_metadata()
        last_updated = metadata_dict["resource"]["updatedAt"]
        last_updated_date = dt.datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.000Z")
        return last_updated_date

    def archive_latest_saved_metadata(self) -> None:
        last_updated = self.get_latest_update_date_of_saved_metadata()
        last_updated_str = last_updated.strftime("%Y%m%d__%H%M%S")
        archive_file_path = os.path.join(
            os.path.dirname(self.metadata_file_path),
            "archive",
            f"{self.table_name}_{last_updated_str}.json",
        )
        shutil.copy2(self.metadata_file_path, archive_file_path)


class SocrataTable:
    def __init__(
        self,
        table_id: str,
        root_data_dir: os.path = get_global_root_data_dir(),
        verbose: bool = False,
        enforce_metadata_parity: bool = True,
    ) -> None:
        self.table_id = table_id
        self.verbose = verbose
        self.metadata = SocrataMetadata(table_id=table_id, root_data_dir=root_data_dir)
        self.enforce_metadata_parity = enforce_metadata_parity

    def new_table_data_available(self) -> bool:
        if os.path.isfile(self.metadata.metadata_file_path):
            public_data_last_updated = self.metadata.get_latest_update_date()
            saved_metadata_last_updated = self.metadata.get_latest_update_date_of_saved_metadata()
            return public_data_last_updated > saved_metadata_last_updated
        else:
            return True

    def _archive_latest_saved_raw_data(self) -> None:
        last_updated = self.metadata.get_latest_update_date(
            metadata_dict=self.metadata.read_latest_table_metadata()
        )
        last_updated_str = last_updated.strftime("%Y%m%d__%H%M%S")
        archive_file_path = os.path.join(
            os.path.dirname(self.metadata.table_data_raw_dir),
            "archive",
            f"{self.metadata.table_name}_{last_updated_str}.{self.metadata.file_ext}",
        )
        if os.path.isfile(self.metadata.data_raw_file_path):
            shutil.copy2(self.metadata.data_raw_file_path, archive_file_path)

    def _download_raw_table_data(self) -> None:
        self.metadata.save_metadata()
        extract_file_from_url(
            file_path=self.metadata.data_raw_file_path,
            url=self.metadata.get_data_download_url(),
            data_format=self.metadata.file_ext,
            force_repull=True,
            return_df=False,
        )

    def _update_raw_table_data(self) -> None:
        self.metadata.archive_latest_saved_metadata()
        self.metadata.save_metadata()
        self._archive_latest_saved_raw_data()
        self._download_raw_table_data()

    def _refresh_raw_data(self) -> None:
        prior_raw_data_file_exists = os.path.isfile(self.metadata.data_raw_file_path)
        prior_metadata_file_exists = os.path.isfile(self.metadata.metadata_file_path)
        if (not prior_raw_data_file_exists) and (not prior_metadata_file_exists):
            self._download_raw_table_data()
        elif prior_raw_data_file_exists and prior_metadata_file_exists:
            if self.new_table_data_available():
                self._update_raw_table_data()
        else:
            raise DataMetadataParityError(
                prior_raw_data_file_exists, prior_metadata_file_exists, self.metadata.table_name
            )

    def read_raw_data(self) -> pd.DataFrame:
        self._refresh_raw_data()
        if self.metadata.is_geospatial:
            return gpd.read_file(self.metadata.data_raw_file_path)
        else:
            return pd.read_csv(self.metadata.data_raw_file_path)
