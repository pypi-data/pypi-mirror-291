import sqlite3
import logging
from typing import List, Optional, Dict, Union
import json

try:
    import importlib.resources as resources

except ImportError:
    import pkg_resources as resources


class Atlas:
    def __init__(self):
        # Use the appropriate method to get the path to the database file
        if hasattr(resources, 'files'):
            # Python 3.9+ with enhanced importlib.resources
            self._db_path = str(resources.files(
                'pyworldatlas').joinpath('worldatlas.sqlite3'))
        elif hasattr(resources, 'path'):
            # Python 3.7 and 3.8 with basic importlib.resources
            with resources.path('pyworldatlas', 'worldatlas.sqlite3') as db_path:
                self._db_path = str(db_path)
        else:
            # Fallback to pkg_resources for Python 3.6 and earlier
            self._db_path = resources.resource_filename(
                'pyworldatlas', 'worldatlas.sqlite3')

    class CountryNotFoundError(Exception):
        pass

    def _connect(self) -> sqlite3.Connection:
        # Open the database in read-only mode
        return sqlite3.connect(f'file:{self._db_path}?mode=ro', uri=True)

    def progress(self) -> Optional[float]:
        """
        Returns the percentage of data that the library is aimed to contain.

        Returns:
            - float: The percentage of data currently available in the library.
        """
        query = "SELECT COUNT(id) FROM base_country"
        total_data_size = 285  # Total entries that somewhat should exist in the table

        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                current_data_size = cursor.fetchone()[0]

            progress_percentage = round(
                (current_data_size / total_data_size) * 100, 1)
            logging.info(
                f"Current data size: {current_data_size}, Total data size: {total_data_size}, Progress: {progress_percentage}%")
            return progress_percentage

        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None

    def get_countries(self,
                      continents: Optional[List[str]] = None,
                      min_population: Optional[float] = None,
                      max_population: Optional[float] = None,
                      min_gdp: Optional[float] = None,
                      max_gdp: Optional[float] = None) -> Optional[List[str]]:
        """
        Fetches a list of countries filtered by continents.

        Parameters:
            - continents (list of str, optional): The names of the continents to filter countries by.
            If specified, it must contain at least one of the following:
            ["Asia", "Africa", "North America", "South America", 
            "Antarctica", "Europe", "Oceania"].

        Returns:
            - list: A list of country names (str) from the specified continent(s).
        """

        query = """
        SELECT c.name
        FROM base_country c
        JOIN base_country_continents cc ON c.id = cc.country_id
        JOIN base_continent co ON cc.continent_id = co.id
        """
        params = ()

        try:

            if continents:
                placeholders = ', '.join('?' for _ in continents)
                query += f" WHERE co.name IN ({placeholders})"
                params = tuple(continent.strip() for continent in continents)

            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                countries = cursor.fetchall()

        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None

        else:
            return [country[0] for country in countries]

    def get_languages(self,
                      name: Optional[str] = None,
                      iname: Optional[str] = None,
                      countries: Optional[List[str]] = None,
                      official: Optional[bool] = False,
                      recognized: Optional[bool] = False) -> Optional[List[str]]:
        """  """

        return []

    def get_country_profile(self, name: str = None, country_code: bool = False) -> Dict[str, Union[str, int, float]]:
        """
        Fetches the profile of the country entered.

        Parameters:
            - name (str): The names of the country to fetch the profile of.
            Example: "Algeria" or "Albania", etc.
                NOTE: If country_code = True, then this parameter expect an ISO 3166 Alpha-2 country code.
                    Example: "US" instead of "United States".
            - country_code (bool, optional): If True (default False) it makes the parameter 'name' expect a country code in the ISO 3166 Alpha-2 code format.


        Returns:
            - dict: A dictionary containing the profile of the country.


            profile = {
            "official_names": {
                "official_country_name_1": "Republic of Exampleland",
                "official_country_name_2": "Exampleland",
            },
            "motto": {
                "Latin": "Pro populo, a populo",
                "English": "By the people, for the people",
            },
            "capital": {
                "name": "Example City",
                "coordinates_degree_east": 12.34,
                "coordinates_degree_north": 56.78,
                "is_largest_city": False,
            },
            "largest_city": {
                "name": "Example Largest City",
                "coordinates_degree_east": 22.34,
                "coordinates_degree_north": 46.78,
                "is_largest_city": True,
            },
            "area": {
                "total_km2": 2443506.4,
                "total_km2_with_disputed_territories": 3454563.4,
                "water_percentage": 34.5,
            },
            "largest_city": {
                "name": "Example City",
                "coordinates_degree_east": 12.34,
                "coordinates_degree_north": 56.78,
            },
            "population": {
                "total": 1000000,
                "date_year": 2023,
                "density_km2": 12.3,
            },
            "demonym": "Examplelander",
            "continent": ["Asia"],
            "timezones": {
                "UTC+1": {
                    "DST": False
                }
            },
            "religion": {
                "Christianity": 16.02,
                "Islam": 30.10,
                "Others": 3.55,
            },
            "languages": {
                "official_languages": ["English", "French"],
                "recognized_languages": ["Spanish"],
            },
            "currency": {
                "name": "Example Dollar",
                "symbol": "$",
                "iso_code": "EXD",
            },
            "government": {
                "president": "John Doe",
                "prime_minister": "Jane Smith",
                "declaration_of_state_sovereignty": "1776-07-04",
                "other_leader_title": "Governor",
                "other_leader_name": "Alice Johnson",
                "government_type": "Federal Republic",
                "other_leader_assumed_office_date": "2020-01-01",
                "president_assumed_office_date": "2021-01-20",
                "prime_minister_assumed_office_date": "2022-03-15",
            },
            "ethnic_groups": {
                "Turkmen": 2.0,
                "Others": 98.0,
            },
            "gdp": {
                "ppp_trillions": 0.04596,
                "ppp_per_capita": 3245.4,
                "nominal_total_trillions": 0.04524,
                "nominal_per_capita": 456.5,
                "ppp_gdp_year": 2023,
                "nominal_gdp_year": 2023,
            },
            "gini_index": {
                "value": 45.2,
                "year": 2023,
            },
            "source": {
                "wikipedia_main_article_revision_id": 3494405,
            },
            "last_updated": "2023-08-20",
        }

        """

        if name is None:
            raise self.CountryNotFoundError("Country name is required.")
        
        name = name.strip()
        name = name.lower()


        if country_code:
            query = f"SELECT id from base_country WHERE ISO_3166_CODE = {name}"
        else:
            query = "SELECT * from base_country WHERE LOWER(name) = ?;"


        profile = {}

        with self._connect() as conn:
            conn.row_factory = sqlite3.Row # This makes data accessible by columns name
            cursor = conn.cursor()
            cursor.execute(query, (name,))
            base_country = cursor.fetchone()

            is_capital_largest_city = base_country["capital"] == base_country["largest_city"]

            profile["capital"] = {
                
                "name": base_country["capital"],
                "coordinates_degree_east": base_country["capital_coordinates_degree_east"],
                "coordinates_degree_north": base_country["capital_coordinates_degree_north"],
                "is_largest_city": is_capital_largest_city,
                
                }
            if not is_capital_largest_city:
                profile["largest_city"] = {
                    
                    "name": base_country["largest_city"],
                    "coordinates_degree_east": base_country["largest_city_coordinates_degree_east"],
                    "coordinates_degree_north": base_country["largest_city_coordinates_degree_north"],
                    }
            
            profile["driving_side"] = base_country["driving_side"]
            profile["calling_code"] = base_country["calling_code"]
            profile["iso_3166_code"] = base_country["iso_3166_code"]
            profile["internet_tld"] = base_country["internet_tld"]
  
        return json.dumps(profile, indent=4)