from datetime import datetime
import requests
from typing import Dict, List, Union, Optional

class SocrataTable:
    def __init__(self, table_id: str, verbose: bool = False) -> None:
        self.table_id = table_id
        self.verbose = verbose
        self.set_table_metadata()
        self.is_geospatial = self.table_has_geospatial_data()
        self.table_data_domain = self.set_table_data_domain()

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
        table_column_datatypes = self.table_metadata["resource"][
            "columns_datatype"
        ]
        table_has_geo_column = any(
            [
                table_col_dtype in socrata_geo_datatypes
                for table_col_dtype in table_column_datatypes
            ]
        )
        return table_has_geo_column

    def set_table_data_domain(self) -> str:
        return self.table_metadata["metadata"]["domain"]
    
    def table_has_data_columns(self) -> bool:
        """TODO: fix this. I think this is only checking the number of data columns 
        *documented by the table owner*"""
        return len(self.table_metadata["resource"]["columns_name"]) != 0

    def table_has_geo_type_view(self) -> bool:
        return self.table_metadata["resource"]["lens_view_type"] == "geo"

    def table_has_map_type_display(self) -> bool:
        return self.table_metadata["resource"]["lens_display_type"] == "map"

    def table_has_geospatial_data(self) -> bool:
        is_geospatial = (
            (not self.table_has_data_columns())
            and (self.table_has_geo_type_view() or self.table_has_map_type_display())
        ) or (self.table_has_geo_column())
        return is_geospatial

    def _format_geospatial_export_format(self, export_format: str) -> str:
        valid_export_formats = get_valid_geospatial_export_formats_for_socrata_tables()
        if export_format in valid_export_formats.values():
            return export_format
        else:
            assert (
                export_format.lower() in valid_export_formats.keys()
            ), "Invalid geospatial format"
            return valid_export_formats[export_format.lower()]

    def get_data_download_url(self, export_format: str = "Shapefile") -> str:
        export_format = self._format_geospatial_export_format(
            export_format=export_format
        )
        domain = self.table_data_domain
        if self.is_geospatial:
            return f"https://{domain}/api/geospatial/{self.table_id}?method=export&format={export_format}"
        else:
            return f"https://{domain}/api/views/{self.table_id}/rows.csv?accessType=DOWNLOAD"