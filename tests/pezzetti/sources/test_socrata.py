import os

import pytest

from pezzetti.sources import socrata


@pytest.fixture(scope="session")
def global_root_data_dir_path(tmp_path_factory):
    root_data_dir_path = tmp_path_factory.mktemp("data")
    print(f"root_data_dir_path: {root_data_dir_path}")
    return root_data_dir_path


def test_get_global_root_data_dir(global_root_data_dir_path):
    root_data_dir = socrata.get_global_root_data_dir(root_data_dir=global_root_data_dir_path)
    print(f"root_data_dir in getter test: {root_data_dir}")


# @pytest.mark.usefixtures("MockInitialSocrataMetadata", "global_root_data_dir_path")
def test_initial_metadata_retrieval(MockInitialSocrataMetadata, global_root_data_dir_path):
    metadata_obj = socrata.SocrataMetadata(
        table_id="zy99-9z9z", root_data_dir=global_root_data_dir_path
    )
    print(metadata_obj)
    print(f"dir(metadata_obj): {dir(metadata_obj)}")
    print(f"table_metadata: {metadata_obj.table_metadata}")
    print(f"metadata_obj.data_raw_file_path: {metadata_obj.data_raw_file_path}")


def test_initial_metadata_obj(initial_socrata_metadata):
    metadata_obj = initial_socrata_metadata
    print("\n\n\n\n\n")
    print(metadata_obj)
    print(f"dir(metadata_obj): {dir(metadata_obj)}")
    print(f"table_metadata: {metadata_obj.table_metadata}")


def test_initial_socrata_table_retrieval(initial_socrata_table):
    # socrata_table_obj = initial_socrata_table
    print("\n\n\n\n\n\n\n")
    print(f"dir(initial_socrata_table): {dir(initial_socrata_table)}\n\n")
    print(f"dir(initial_socrata_table.metadata): {dir(initial_socrata_table.metadata)}\n\n")
    print(f"initial_socrata_table.metadata: {initial_socrata_table.metadata.table_metadata}")
    print(
        f"initial_socrata_table.metadata.data_raw_file_path: {initial_socrata_table.metadata.data_raw_file_path}"
    )
    assert not os.path.isfile(initial_socrata_table.metadata.data_raw_file_path)
    table_df = initial_socrata_table.read_raw_data()
    assert table_df.shape == (5, 3)
    assert os.path.isfile(initial_socrata_table.metadata.data_raw_file_path)


def test_no_archive_before_update(initial_socrata_table):
    archived_files = os.listdir(
        os.path.join(os.path.dirname(initial_socrata_table.metadata.data_raw_file_path), "archive")
    )
    assert len(archived_files) == 0


def test_check_updated_socrata_table_data(updated_socrata_table_data):
    print("\n\n")
    print(updated_socrata_table_data)
