import requests
import os

class FinceptAPI:
    def __init__(self, api_key=None, base_url="https://fincept.share.zrok.io/"):
        self.api_key = api_key or os.getenv("FINCEPT_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set it in the environment or pass it directly.")
        self.base_url = base_url

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def get_databases(self):
        return self._get("databases")

    def get_tables(self, dbname):
        return self._get(f"{dbname}/tables")

    def get_table_data(self, dbname, table, limit=500, offset=0):
        params = {"limit": limit, "offset": offset}
        return self._get(f"{dbname}/{table}/data", params=params)

    # Additional methods can be added as needed
