# %%
import os
import json
from tqdm import tqdm
import requests as rq
from heart import RAW

# %%
username = os.getenv("heart_user")
password = os.getenv("heart_password")

# %%
class HEART:
    def __init__(self):
        self._token_url = "https://heart-dms.risa.eu/token"
        self._urls = {
            "bioassist" : "https://heart-dms.risa.eu/questionnaire/get",
            "sentio" : "https://heart-dms.risa.eu/questionnaire/get/questionnaire-v2"
        }
        self._headers = {
            "Content-Type": "application/json",
        }
    def connect(self, username:str = username, password:str = password) -> None:
        """Connect to the HEART API
        This function will authenticate the user and get an access token.

        Parameters
        ----------
        username : str, optional
            the username, by default username
        password : str, optional
            the passowrd, by default password

        Raises
        ------
        Exception
            if the request fails.
        """
        data = {
            "app" : "heart", 
            "username" : username,
            "password" : password
        }
        response = rq.post(self._token_url, headers = self._headers, json=data)
        if response.status_code == 200:
            self._token = response.json()["access_token"]
            print("Connected to HEART API")
        else:
            raise Exception("Connection failed")
    def get_data(self, endpoint = "bioassist", query = {}) -> list[dict]:
        """Get data from the HEART API

        Parameters
        ----------
        endpoint : str, optional
            the name of the endpoing, by default "bioassist"
        query : dict, optional
            additional parameters to pass to the get request, by default {}

        Returns
        -------
        list[dict]
            a list of dictionaires containing data from the API. The content of the dictionaries depends on the endpoint.

        Raises
        ------
        Exception
            if the request fails.
        """
        headers = {**query, **self._headers}
        headers["Authorization"] = f"Bearer {self._token}"
        response = rq.get(self._urls[endpoint], headers = headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception("Failed to get data")
    def write_out(self, file_name: str, endpoint: str = "bioassist", query = {}) -> None:
        """Write out the data to a json file

        Parameters
        ----------
        file_name : str
            the name of the file to write to
        endpoint : str, optional
            the name of the endpoing, by default "bioassist"
        query : dict, optional
            additional parameters to pass to the get request, by default {}
        """
        with open(RAW / file_name, "w") as file:
            for item in tqdm(self.get_data(endpoint = endpoint, query = query), desc="Writing out data"):
                file.write(json.dumps(item) + "\n")
