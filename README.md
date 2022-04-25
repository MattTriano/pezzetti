# Pezzetti
*A package of little pieces.*

This package centralizes utils I've developed along the way. Rather than continually repeat myself, I'll just DRY out these pieces and put them in this toolbox.

## Installation

For now, I'd recommend installing it into a conda environment via pip with the `-e` *editable* flag.

```bash
(geo_env) matt@matt:~/.../pezzetti$ python -m pip install -e .
```

Or if you don't feel like cloning the repo, you can just install it from the repo via

```bash
(geo_env) matt@matt:~/.../pezzetti$ python -m pip install git+https://github.com/MattTriano/pezzetti.git
```

although I'd advise installing from a specific commit (as demonstrated below) if you expect you'll use your code in the future but don't want to deal with debugging any possible issues caused by evolution of this codebase.

```bash
(geo_env) matt@matt:~/.../pezzetti$ python -m pip install git+https://github.com/MattTriano/pezzetti.git@352e5ea8e7d5b8f0a3b4d9c7047c65fbb4b3fe49
```

# Usage

This is really kind of a bundle of helper functionality, so this section may (and likely will) evolve over time but at present...

## DataSource Utils:

These tools provide functionality for pulling data and metadata for publicly available data sources.

### DataSource: Socrata

Many cities and public agencies or organizations use the Socrata data platform to make subsets of their database tables publicly available. Each table hosted on Socrata can be uniquely identified by its `table_id`, which will consist of 4 alphanumeric characters, a hyphen, and then 4 more alphanumeric characters, and can be found in the URL of a data table's description page. For example:
* Chicago's **Crimes - 2001 to Present** data table:
    * url: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)
    * `table_id`: ijzp-q8t2
* The Cook County Assessor's Property Sales data table:
    * url: https://datacatalog.cookcountyil.gov/Property-Taxation/Cook-County-Assessor-s-Sales/93st-4bxh
    * `table_id`: 93st-4bxh

[Socrata data platform](https://dev.socrata.com/data/)

#### Working with SocrataTable

Create a SocrataTable object for your table of interest by passing in said table's `table_id` and if you don't want to use the default `root_data_dir` (which is `~/projects/data`, ie a subdirectory off of your home/user directory), you can specify a location. The relative path shown below would work for a typical project structure with code in a directory one level from the project-root-directory.

```python
import os
from pezzetti.sources.socrata import SocrataTable

cook_county_property_sales = SocrataTable(
    table_id="93st-4bxh",
    root_data_dir=os.path.join("..", "data")
)
```

You can access a Socrata table's metadata through the SocrataTable object `.metadata` object. The `metadata.table_metadata` attribute contains the metadata Socrata publishes for the table and can be inspected via the command below. Many other metadata features for the table can be accessed through `.metadata`.

```python
print(cook_county_property_sales.metadata.table_metadata)
```

To read up-to-date table data to a pandas DataFrame or geopandas GeoDataFrame (depending on whether the table is geospatial or not), the `.read_raw_data()` method will download table metadata and see if up-to-date data is available locally. If the local data is not up to date, the local raw data and metadata will be copied to archive directories and fresh data will be downloaded and returned, otherwise the local data will be read in and returned.

```python
print(cook_county_property_sales_df = cook_county_property_sales.read_raw_data())
```