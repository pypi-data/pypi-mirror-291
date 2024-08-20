import sqlite3
import logging

try:
    import importlib.resources as resources

except ImportError:
    import pkg_resources as resources

class Atlas:
    def __init__(self):
        # Use the appropriate method to get the path to the database file
        if hasattr(resources, 'files'):
            # Python 3.9+ with enhanced importlib.resources
            self.db_path = str(resources.files('pyworldatlas').joinpath('worldatlas.sqlite3'))
        elif hasattr(resources, 'path'):
            # Python 3.7 and 3.8 with basic importlib.resources
            with resources.path('pyworldatlas', 'worldatlas.sqlite3') as db_path:
                self.db_path = str(db_path)
        else:
            # Fallback to pkg_resources for Python 3.6 and earlier
            self.db_path = resources.resource_filename('pyworldatlas', 'worldatlas.sqlite3')

    def _connect(self):
        # Open the database in read-only mode
        return sqlite3.connect(f'file:{self.db_path}?mode=ro', uri=True)

    def progress(self):
        """
        Returns the percentage of data that the library is aimed to contain.

        Returns:
            - float: The percentage of data currently available in the library.
        """
        query = "SELECT COUNT(id) FROM base_country"
        total_data_size = 285 # Total entries that somewhat should exist in the table
        
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                current_data_size = cursor.fetchone()[0]
            
            progress_percentage = round((current_data_size / total_data_size) * 100, 1)
            logging.info(f"Current data size: {current_data_size}, Total data size: {total_data_size}, Progress: {progress_percentage}%")
            return progress_percentage

        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None


    def get_countries(self, continents=None):
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