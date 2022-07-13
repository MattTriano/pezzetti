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




@pytest.mark.usefixtures("MockInitialSocrataMetadata", "global_root_data_dir_path")
def test_initial_metadata_retrieval(global_root_data_dir_path):
    metadata_obj = socrata.SocrataMetadata(
        table_id="zy99-9z9z",
        root_data_dir=global_root_data_dir_path
    )
    print(metadata_obj)
    print(f"dir(metadata_obj): {dir(metadata_obj)}")
