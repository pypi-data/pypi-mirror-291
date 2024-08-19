import requests

class FinceptAPI:
    def __init__(self, api_key, base_url="http://localhost:5000"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": self.api_key}

    def get_databases(self):
        url = f"{self.base_url}/databases"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_tables(self, dbname):
        url = f"{self.base_url}/{dbname}/tables"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_table_data(self, dbname, table, limit=500, offset=0):
        url = f"{self.base_url}/{dbname}/{table}/data"
        params = {"limit": limit, "offset": offset}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
