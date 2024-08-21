from functools import cache
import datetime
from typing import Tuple

from shapely import Polygon

from nigeria_geodata.config import Config
from nigeria_geodata.datasources.base import DataSource
from nigeria_geodata.models.common import FeatureCollection
from nigeria_geodata.utils.api import make_request
from nigeria_geodata.utils import logger
from nigeria_geodata.utils.exceptions import PackageNotFoundError


class GeodataUtils:
    @staticmethod
    @cache
    def get_states() -> FeatureCollection:
        """
        Fetch the GeoJSON data from the github gist.

        Returns:
            Dict: The GeoJSON data as a dictionary.
        """
        service_url: str = Config.get_service_url(
            DataSource.NGSA, "NIGERIA_STATES_BOUNDARY_URL"
        )
        response = make_request(service_url)
        return response

    @staticmethod
    def get_state_geometry(state_name: str) -> Tuple[float, float, float, float]:
        """
        Get the bounding box for a given state.

        Args:
            state_name (str): The name of the state.

        Returns:
            Tuple[float, float, float, float]: The bounding box (minx, miny, maxx, maxy).
        """

        states_geojson = GeodataUtils.get_states()

        state_geometry = list(
            filter(
                lambda feature: feature["properties"]["ADM1NAME_"].lower()
                == state_name.lower(),
                states_geojson["features"],
            )
        )
        if len(state_geometry) > 0:
            return state_geometry[0]["geometry"]
        else:
            msg = f"State '{state_name}' not found in the GeoJSON data."
            logger.error(msg)
            raise ValueError(msg)

    @staticmethod
    def geojson_to_esri_type(geojson_type: str) -> str:
        """
        Convert a GeoJSON geometry type to an ESRI geometry type.
        """
        geojson_to_esri = {
            "Point": "esriGeometryPoint",
            "MultiPoint": "esriGeometryMultipoint",
            "LineString": "esriGeometryPolyline",
            "Polygon": "esriGeometryPolygon",
            "MultiPolygon": "esriGeometryPolygon",  # We can add this here since ESRI treats MultiPolygon similarly to Polygon
        }
        esri_type = geojson_to_esri.get(geojson_type)
        if not esri_type:
            raise ValueError(f"Unsupported GeoJSON type: {geojson_type}")
        return esri_type

    @staticmethod
    def geojson_to_esri_json(geojson_data: Polygon):
        """
        Convert a GeoJSON geometry type to an ESRI JSON.
        """
        # ref - https://developers.arcgis.com/rest/services-reference/enterprise/geometry-objects/
        if geojson_data["type"] == "Point":
            esri_json = {
                "x": geojson_data["coordinates"][0],
                "y": geojson_data["coordinates"][1],
            }

        elif geojson_data["type"] == "LineString":
            esri_json = {"paths": [geojson_data["coordinates"]]}

        elif geojson_data["type"] == "Polygon":
            esri_json = {"rings": geojson_data["coordinates"]}
        elif geojson_data["type"] == "MultiPolygon":
            esri_json = {
                "rings": [
                    ring for polygon in geojson_data["coordinates"] for ring in polygon
                ]
            }
        else:
            raise ValueError(
                f"Unsupported GeoJSON geometry type: {geojson_data['type']}"
            )

        return esri_json


class CheckDependencies:
    @staticmethod
    def pandas():
        """
        Check if the 'pandas' module is installed and return it if available.
        Raises an error with instructions if the module is not found.

        Returns:
            module: The imported 'pandas' module.

        Raises:
            PackageNotFoundError: If 'pandas' is not installed.
        """
        try:
            import pandas

            return pandas
        except PackageNotFoundError as err:
            # Raise an error with a message to install the missing package
            raise PackageNotFoundError(
                "pandas is required for rendering results as a dataframe.\n"
                "Run `pip install pandas`."
            ) from err

    @staticmethod
    def geopandas():
        """
        Check if the 'geopandas' module is installed and return it if available.
        Raises an error with instructions if the module is not found.

        Returns:
            module: The imported 'geopandas' module.

        Raises:
            PackageNotFoundError: If 'geopandas' is not installed.
        """
        try:
            import geopandas

            return geopandas
        except PackageNotFoundError as err:
            # Raise an error with a message to install the missing package
            raise PackageNotFoundError(
                "geopandas is required for rendering results as a geodataframe.\n"
                "Run `pip install geopandas`."
            ) from err

    @staticmethod
    def typer():
        """
        Check if the 'typer' module is installed and return it if available.
        Raises an error with instructions if the module is not found.

        Returns:
            module: The imported 'typer' module.

        Raises:
            PackageNotFoundError: If 'typer' is not installed.
        """
        try:
            import typer

            return typer
        except PackageNotFoundError as err:
            # Raise an error with a message to install the missing package
            raise PackageNotFoundError(
                "typer is required for CLI support.\n" "Run `pip install typer`."
            ) from err

    @staticmethod
    def lonboard():
        """
        Check if the 'lonboard' module is installed and return it if available.
        Raises an error with instructions if the module is not found.

        Returns:
            module: The imported 'lonboard' module.

        Raises:
            ImportError: If 'lonboard' is not installed.
        """
        try:
            from lonboard import viz

            return viz
        except PackageNotFoundError as err:
            # Raise an error with a message to install the missing package
            raise ImportError(
                "lonboard is required for map visualization.\n"
                "Run `pip install lonboard`."
            ) from err


def timestamp_to_datetime(timestamp_ms: int):
    # Convert to seconds by dividing by 1000
    timestamp_sec = timestamp_ms / 1000

    # Convert to datetime
    date_time = datetime.datetime.fromtimestamp(timestamp_sec)

    return date_time
