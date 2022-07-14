import datetime as dt
from typing import Dict

import pandas as pd
import pytest

from pezzetti.sources import socrata


@pytest.fixture
def initial_socrata_table_metadata() -> Dict:
    return {
        "_id": "zy99-9z9z",
        "time_of_collection": dt.datetime(2022, 7, 4, 23, 52, 11, 213610),
        "resource": {
            "name": "Mock Data Table",
            "id": "zy99-9z9z",
            "parent_fxf": [],
            "description": "This dataset is a mockup of a geospatial dataset.",
            "attribution": "Mockup City",
            "attribution_link": "http://www.mockupcity.org",
            "contact_email": None,
            "type": "dataset",
            "updatedAt": "2022-05-01T00:05:26.000Z",
            "createdAt": "2016-04-17T13:45:01.000Z",
            "metadata_updated_at": "2017-09-12T17:18:45.000Z",
            "data_updated_at": "2022-05-01T00:05:26.000Z",
            "page_views": {
                "page_views_last_week": 182,
                "page_views_last_month": 712,
                "page_views_total": 46552,
                "page_views_last_week_log": 5.20400668708,
                "page_views_last_month_log": 6.56807791141,
                "page_views_total_log": 10.7483252463,
            },
            "columns_name": ["ADDRESS", "LONGITUDE", "LATITUDE"],
            "columns_field_name": ["address", "longitude", "latitude"],
            "columns_datatype": ["Text", "Text", "Text"],
            "columns_description": ["", "", ""],
            "columns_format": [
                {"align": "left", "aggregate": "count"},
                {},
                {},
            ],
            "download_count": 9591,
            "provenance": "official",
            "lens_view_type": "tabular",
            "lens_display_type": "table",
            "blob_mime_type": None,
            "hide_from_data_json": False,
            "publication_date": "2016-10-15T21:42:32.000Z",
        },
        "classification": {
            "categories": ["public safety"],
            "tags": [],
            "domain_category": "Transportation",
            "domain_tags": ["traffic", "transportation"],
            "domain_metadata": [
                {"key": "Metadata_Frequency", "value": "Updated daily"},
                {"key": "Metadata_Data-Owner", "value": "Transportation"},
                {"key": "Metadata_Time-Period", "value": "Current"},
            ],
        },
        "metadata": {"domain": "data.mockupcity.org"},
        "permalink": "https://data.mockupcity.org/d/zy99-9z9z",
        "link": "https://data.mockupcity.org/Transportation/Mockup-Locations/zy99-9z9z",
        "owner": {"id": "mock-man9", "user_type": "interactive", "display_name": "mockadmin"},
        "creator": {"id": "mock-man9", "user_type": "interactive", "display_name": "mockadmin"},
    }


@pytest.fixture
def updated_socrata_table_metadata(initial_socrata_table_metadata) -> Dict:
    updated_metadata = initial_socrata_table_metadata
    updated_metadata["time_of_collection"] = (dt.datetime(2022, 7, 14, 13, 42, 25, 531425),)
    updated_metadata["resource"] = {
        "name": "Mock Data Table",
        "id": "zy99-9z9z",
        "parent_fxf": [],
        "description": "This dataset is a mockup of a geospatial dataset.",
        "attribution": "Mockup City",
        "attribution_link": "http://www.mockupcity.org",
        "contact_email": None,
        "type": "dataset",
        "updatedAt": "2022-05-01T00:05:26.000Z",
        "createdAt": "2016-04-17T13:45:01.000Z",
        "metadata_updated_at": "2017-09-12T17:18:45.000Z",
        "data_updated_at": "2022-05-01T00:05:26.000Z",
        "page_views": {
            "page_views_last_week": 232,
            "page_views_last_month": 815,
            "page_views_total": 48552,
            "page_views_last_week_log": 5.44673737167,
            "page_views_last_month_log": 6.70318811324,
            "page_views_total_log": 10.7903906675,
        },
        "columns_name": ["ADDRESS", "LONGITUDE", "LATITUDE"],
        "columns_field_name": ["address", "longitude", "latitude"],
        "columns_datatype": ["Text", "Text", "Text"],
        "columns_description": ["", "", ""],
        "columns_format": [
            {"align": "left", "aggregate": "count"},
            {},
            {},
        ],
        "download_count": 9824,
        "provenance": "official",
        "lens_view_type": "tabular",
        "lens_display_type": "table",
        "blob_mime_type": None,
        "hide_from_data_json": False,
        "publication_date": "2016-10-15T21:42:32.000Z",
    }
    return updated_metadata


@pytest.fixture
def MockInitialSocrataMetadata(monkeypatch, initial_socrata_table_metadata):
    def mock_get_table_metadata(*args, **kwargs):
        return initial_socrata_table_metadata

    # def mock_get_table_metadata(*args, **kwargs):
    #     return {
    #         "_id": "zy99-9z9z",
    #         "time_of_collection": dt.datetime(2022, 7, 4, 23, 52, 11, 213610),
    #         "resource": {
    #             "name": "Mock Data Table",
    #             "id": "zy99-9z9z",
    #             "parent_fxf": [],
    #             "description": "This dataset is a mockup of a geospatial dataset.",
    #             "attribution": "Mockup City",
    #             "attribution_link": "http://www.mockupcity.org",
    #             "contact_email": None,
    #             "type": "dataset",
    #             "updatedAt": "2022-05-01T00:05:26.000Z",
    #             "createdAt": "2016-04-17T13:45:01.000Z",
    #             "metadata_updated_at": "2017-09-12T17:18:45.000Z",
    #             "data_updated_at": "2022-05-01T00:05:26.000Z",
    #             "page_views": {
    #                 "page_views_last_week": 182,
    #                 "page_views_last_month": 712,
    #                 "page_views_total": 46552,
    #                 "page_views_last_week_log": 7.515699838284044,
    #                 "page_views_last_month_log": 9.477758266443889,
    #                 "page_views_total_log": 15.506586521461617,
    #             },
    #             "columns_name": ["ADDRESS", "LONGITUDE", "LATITUDE"],
    #             "columns_field_name": ["address", "longitude", "latitude"],
    #             "columns_datatype": ["Text", "Text", "Text"],
    #             "columns_description": ["", "", ""],
    #             "columns_format": [
    #                 {"align": "left", "aggregate": "count"},
    #                 {},
    #                 {},
    #             ],
    #             "download_count": 9591,
    #             "provenance": "official",
    #             "lens_view_type": "tabular",
    #             "lens_display_type": "table",
    #             "blob_mime_type": None,
    #             "hide_from_data_json": False,
    #             "publication_date": "2016-10-15T21:42:32.000Z",
    #         },
    #         "classification": {
    #             "categories": ["public safety"],
    #             "tags": [],
    #             "domain_category": "Transportation",
    #             "domain_tags": ["traffic", "transportation"],
    #             "domain_metadata": [
    #                 {"key": "Metadata_Frequency", "value": "Updated daily"},
    #                 {"key": "Metadata_Data-Owner", "value": "Transportation"},
    #                 {"key": "Metadata_Time-Period", "value": "Current"},
    #             ],
    #         },
    #         "metadata": {"domain": "data.mockupcity.org"},
    #         "permalink": "https://data.mockupcity.org/d/zy99-9z9z",
    #         "link": "https://data.mockupcity.org/Transportation/Mockup-Locations/zy99-9z9z",
    #         "owner": {"id": "mock-man9", "user_type": "interactive", "display_name": "mockadmin"},
    #         "creator": {"id": "mock-man9", "user_type": "interactive", "display_name": "mockadmin"},
    #     }

    monkeypatch.setattr(socrata.SocrataMetadata, "get_table_metadata", mock_get_table_metadata)


@pytest.fixture
def initial_socrata_metadata(MockInitialSocrataMetadata, global_root_data_dir_path):
    return socrata.SocrataMetadata(table_id="zy99-9z9z", root_data_dir=global_root_data_dir_path)


@pytest.fixture
def initial_socrata_table_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "address": {
                0: "6125 N Cicero Ave (Speed Camera)",
                1: "3137 W Peterson (Speed Camera)",
                2: "2080 W Pershing Rd (Speed Camera)",
                3: "5454 W Irving Park (Speed Camera)",
                4: "3534 N Western (Speed Camera)",
            },
            "longitude": {
                0: "-87.74847678515228",
                1: "-87.7095",
                2: "-87.676366",
                3: "-87.76426726425451",
                4: "-87.68838396394528",
            },
            "latitude": {
                0: "41.9921194114274",
                1: "41.9902819135942",
                2: "41.823116",
                3: "41.95332954454448",
                4: "41.9459625867886",
            },
        }
    )


@pytest.fixture
def updated_socrata_table_data(initial_socrata_table_data) -> pd.DataFrame:
    additional_df = pd.DataFrame(
        {
            "address": {5: "8345 S Ashland Ave (Speed Camera)"},
            "longitude": {5: "-87.66307332925098"},
            "latitude": {5: "41.741741651401504"},
        }
    )
    return pd.concat([initial_socrata_table_data, additional_df])


@pytest.fixture
def MockInitialSocrataTable(
    monkeypatch, initial_socrata_metadata, global_root_data_dir_path, initial_socrata_table_data
):
    def mock_get_metadata(*args, **kwargs):
        return initial_socrata_metadata

    def mock__download_raw_table_data(*args, **kwargs):
        initial_socrata_metadata.save_metadata()
        initial_socrata_table_data.to_csv(initial_socrata_metadata.data_raw_file_path, index=False)

    monkeypatch.setattr(socrata.SocrataTable, "get_metadata", mock_get_metadata)
    monkeypatch.setattr(
        socrata.SocrataTable, "_download_raw_table_data", mock__download_raw_table_data
    )


@pytest.fixture
def initial_socrata_table(MockInitialSocrataTable, global_root_data_dir_path):
    socrata_table_obj = socrata.SocrataTable(
        table_id="zy99-9z9z", root_data_dir=global_root_data_dir_path
    )
    return socrata_table_obj


@pytest.fixture
def geospatial_socrata_table_metadata_updated():
    metadata_dict = geospatial_socrata_table_metadata_initial()
    metadata_dict["time_of_collection"] = dt.datetime.now()
    metadata_dict["resource"]["updatedAt"] = "2022-07-01T07:21:33.000Z"
    metadata_dict["resource"]["data_updated_at"] = "2022-07-01T07:21:33.000Z"
    return metadata_dict
