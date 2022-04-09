import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

def make_point_geometry(df: pd.DataFrame, long_col: str, lat_col: str) -> pd.Series:
    latlong_df = df[[long_col, lat_col]].copy()
    df["geometry"] = pd.Series(map(Point, latlong_df[long_col], latlong_df[lat_col]))
    return df


def geospatialize_df_with_point_geometries(
    df: pd.DataFrame, long_col: str, lat_col: str, crs: str = "EPSG:4326"
) -> gpd.GeoDataFrame:
    df = df.copy()
    gdf = make_point_geometry(df=df, long_col=long_col, lat_col=lat_col)
    gdf = gpd.GeoDataFrame(gdf, crs=crs)
    return gdf