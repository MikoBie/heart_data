import requests as rq
import os
import json
from tqdm import tqdm
from heart import RAW


class HEART:
    """Class for getting data from DMS"""

    def __init__(self):
        self._connected = False
        self._token = ""
        self._path = RAW
        self._urls = {
            "bioassist": "https://heart-dms.risa.eu/questionnaire/get",
            "sentio": "https://heart-dms.risa.eu/questionnaire/get/questionnaire-v2",
        }

    def connect_api(self, username: str, password: str, app: str = "heart") -> str:
        """Connects to API and returns the token.

        Parameters
        ----------
        username : str
            username for the API, by default it is an environment variable.
        password : str
            password for the API, by default it is an environment variable.
        app : str
            name of the application, by default it is "heart".

        Returns
        -------
            (str): a string with access token.

        Raises
        ------
        TypeError
            raises a TypeError when the connection to API failed.
        """
        url = "https://heart-dms.risa.eu/token"
        headers = {"Content-Type": "application/json"}
        dt = {"app": app, "username": username, "password": password}
        response = rq.post(url=url, headers=headers, json=dt)
        if response.status_code == 200:
            self._connected = True
            self._token = response.json().get("access_token", "")
            print(f"Status code: {response.status_code}")
        else:
            raise rq.exceptions.ConnectionError(
                f"Connection failed due to status code: {response.status_code}"
            )

    def query(self, endpoint: str = "bioassist", query: dict = {}) -> list[dict]:
        """Sends a query request to url and returns a list of dictionaries.

        Parameters
        ----------
        query, optional
            a dictionary with query options, by default it is and empty
            dictionary that returns all records. Please see the example of
            a query dictionary below:
            {
                "userId" : "123456",
                "from" : "2007-12-03T10:15:30.00Z"
                "to" : "2007-12-03T10:15:30.00Z"
            }
        endpoint, optional
            name of the endpoint from which it should query documents, by default "bioassist". The other option is "sentio".

        Returns
        -------
            a list of dictionaries.
        """
        payload = {**query}
        if not self._connected:
            return []
        headers = {"Authorization": f"Bearer {self._token}"}
        response = rq.get(url=self._urls[endpoint], params=payload, headers=headers)
        if response.status_code == 200:
            return response.json()

    def write_out(
        self, file_name: str, endpoint: str = "bioassist", query: dict = {}
    ) -> None:
        """Writes out the data to a file.

        Parameters
        ----------
        file_name : str
            name of the file to write out.
        endpoint : str, optional
            the name of the endpoing, by default "bioassist"
        query : dict, optional
            additional parameters to pass to the get request, by default {}
        """
        if not os.path.exists(self._path):
            os.makedirs(self._path)
        with open(self._path / file_name, "w") as file:
            for line in tqdm(self.query(endpoint=endpoint, query=query)):
                file.write(json.dumps(line) + "\n")
