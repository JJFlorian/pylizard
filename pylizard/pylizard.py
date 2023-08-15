import requests
import pandas as pd

"""
NOTE: compatible with API v4 only. Import as from pylizard import pylizard as liz

"""

"""
TODO: 
    - monitoringnetworks
    - groundwaterstations
    - pumpstations
    - measuringstations
    - locations
    - timeseries
"""

LIZARD_BASE_URL = "https://demo.lizard.net/api/v4"

class Auth():
    """
    Class for handling the Lizard auth. 
    Can be used as follows to easily create headers:
        headers =  liz.Auth('LIZARD_API_KEY').headers
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "username": "__key__",
            "password": self.api_key,
            "Content-Type": "application/json",
        }

class Monitoringnetwork():
    """
    Class for working with monitoringnetworks.
    Initialization requires either name or uuid.
    """

    def __init__(self, name=None, uuid=None, headers=None):
        self.headers = headers

        if uuid == None:
            self.name = name
            url = f"{LIZARD_BASE_URL}/monitoringnetworks/?name={self.name}"
            r = requests.get(url, self.headers)
            count = r.json()['count']
            if count == 0:
                raise TypeError("No monitoringnetwork found for provided name")
            if count > 1:
                raise TypeError("Multiple monitoringnetworks found for provided name")
            else:
                self.uuid = r.json()['results'][0]['uuid']

        if name == None:
            self.uuid = uuid
            url = f"{LIZARD_BASE_URL}/monitoringnetworks/{self.uuid}/"

            r = requests.get(url ,self.headers)
            
            if r.status_code != 200:
                raise TypeError("No monitoringnetwork found for provided uuid")
            else:
                self.name = r.json()['name'] 

    def get_stats(self):
        """
        Returns the amount of locations, observation_types, and timeseries.
        
        """

        locations_url = f"{LIZARD_BASE_URL}/monitoringnetworks/{self.uuid}/locations/"
        obs_type_url = f"{LIZARD_BASE_URL}/monitoringnetworks/{self.uuid}/observationtypes/"
        timeseries_url =f"{LIZARD_BASE_URL}/monitoringnetworks/{self.uuid}/timeseries/"

        r_locations = requests.get(url=locations_url, headers=self.headers)
        r_obs_types = requests.get(url=obs_type_url, headers=self.headers)
        r_timeseries = requests.get(url=timeseries_url, headers=self.headers)

        location_count = r_locations.json()['count']
        obs_type_count = r_obs_types.json()['count']
        timeseries_count = r_timeseries.json()['count']

        return_string = f"Locations count: {location_count}, observation type count: {obs_type_count}, timeseries count:{timeseries_count}"

        return return_string
