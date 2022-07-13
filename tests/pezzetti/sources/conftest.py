import datetime as dt

import pytest

from pezzetti.sources import socrata


@pytest.fixture
def geospatial_socrata_table_metadata_initial():
    return {
        "_id": "zy99-9z9z",
        "time_of_collection": dt.datetime(2022, 7, 4, 23, 52, 11, 213610),
        "resource": {
            "name": "Mock GeoSpatial Table",
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
                "page_views_last_week_log": 7.515699838284044,
                "page_views_last_month_log": 9.477758266443889,
                "page_views_total_log": 15.506586521461617,
            },
            "columns_name": ["ADDRESS", "LONGITUDE", "LATITUDE", "LOCATION"],
            "columns_field_name": ["address", "longitude", "latitude", "location"],
            "columns_datatype": ["Text", "Text", "Text", "Point"],
            "columns_description": ["", "", "", ""],
            "columns_format": [
                {"align": "left", "aggregate": "count"},
                {},
                {},
                {"view": "coords", "align": "left"},
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
def MockInitialSocrataMetadata(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get_table_metadata(*args, **kwargs):
        return {
            "_id": "zy99-9z9z",
            "time_of_collection": dt.datetime(2022, 7, 4, 23, 52, 11, 213610),
            "resource": {
                "name": "Mock GeoSpatial Table",
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
                    "page_views_last_week_log": 7.515699838284044,
                    "page_views_last_month_log": 9.477758266443889,
                    "page_views_total_log": 15.506586521461617,
                },
                "columns_name": ["ADDRESS", "LONGITUDE", "LATITUDE", "LOCATION"],
                "columns_field_name": ["address", "longitude", "latitude", "location"],
                "columns_datatype": ["Text", "Text", "Text", "Point"],
                "columns_description": ["", "", "", ""],
                "columns_format": [
                    {"align": "left", "aggregate": "count"},
                    {},
                    {},
                    {"view": "coords", "align": "left"},
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

    monkeypatch.setattr(socrata.SocrataMetadata, "get_table_metadata", mock_get_table_metadata)


@pytest.fixture
def geospatial_socrata_table_metadata_updated():
    metadata_dict = geospatial_socrata_table_metadata_initial()
    metadata_dict["time_of_collection"] = dt.datetime.now()
    metadata_dict["resource"]["updatedAt"] = "2022-07-01T07:21:33.000Z"
    metadata_dict["resource"]["data_updated_at"] = "2022-07-01T07:21:33.000Z"
    return metadata_dict
