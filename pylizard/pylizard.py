import requests
import json
import pandas as pd

"""
NOTE: compatible with API v4 only. Import as from pylizard import pylizard as liz

"""

"""
TODO: 
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
            r = requests.get(url, headers=self.headers)
            count = r.json()['count']
            if count == 0:
                raise TypeError("No monitoringnetwork found for provided name")
            if count > 1:
                raise TypeError("Multiple monitoringnetworks found for provided name")
            else:
                self.uuid = r.json()['results'][0]['uuid']
                self.url = f"{LIZARD_BASE_URL}/monitoringnetworks/{self.uuid}"

        if name == None:
            self.uuid = uuid
            self.url = f"{LIZARD_BASE_URL}/monitoringnetworks/{self.uuid}"

            r = requests.get(self.url, headers=self.headers)
            
            if r.status_code != 200:
                raise TypeError("No monitoringnetwork found for provided uuid")
            else:
                self.name = r.json()['name'] 


    def get_stats(self):
        """
        Returns the amount of locations, observation_types, and timeseries.
        
        """

        locations_url = f"{self.url}/locations/"
        obs_type_url = f"{self.url}/observationtypes/"
        timeseries_url =f"{self.url}/timeseries/"

        r_locations = requests.get(url=locations_url, headers=self.headers)
        r_obs_types = requests.get(url=obs_type_url, headers=self.headers)
        r_timeseries = requests.get(url=timeseries_url, headers=self.headers)

        location_count = r_locations.json()['count']
        obs_type_count = r_obs_types.json()['count']
        timeseries_count = r_timeseries.json()['count']

        return_string = f"Locations count: {location_count}, observation type count: {obs_type_count}, timeseries count:{timeseries_count}"

        return return_string


    def get_locations(self, dataformat='list'):
        """
        Returns the locations related to the monitoringnetwork in a uuid list or df format
        args: 
            - dataformat: 'list' or 'df'

        returns:
            - list of uuids ('list')
            - DataFrame of all data ('df')
        """
        uuid_list = []
        df_list = []
        next_url = f"{self.url}/locations/?limit=250"
        
        while next_url != None:
            r = requests.get(next_url, headers=self.headers)
            results = r.json()['results']
        
            if dataformat == 'list':
                for result in results:
                    uuid_list.append(result['uuid'])
            elif dataformat == 'df':
                for result in results:
                    df_list.append(result)
        
            next_url = r.json()['next']
        
        if dataformat == 'list':
            return uuid_list
        elif dataformat == 'df':
            df = pd.DataFrame(df_list)
            return df
        
    def get_timeseries(self, dataformat='list'):
        """
        Returns the timeseries related to the monitoringnetwork in a uuid list or df format
        args: 
            - dataformat: 'list' or 'df'

        returns:
            - list of uuids ('list')
            - DataFrame of all data ('df')
        """
        uuid_list = []
        df_list = []
        next_url = f"{self.url}/timeseries/?limit=250"
        
        while next_url != None:
            r = requests.get(next_url, headers=self.headers)
            results = r.json()['results']
        
            if dataformat == 'list':
                for result in results:
                    uuid_list.append(result['uuid'])
            elif dataformat == 'df':
                for result in results:
                    df_list.append(result)
        
            next_url = r.json()['next']
        
        if dataformat == 'list':
            return uuid_list
        elif dataformat == 'df':
            df = pd.DataFrame(df_list)
            return df
    
    def post_timeseries(self, timeseries_uuid_list):
        """
        Function to add timeseries to the monitoringnetwork.
        This automatically adds the locations related to the timeseries to the network

        args:
            - a list of uuids of the timeseries to add
        """
        if len(timeseries_uuid_list) == 0:
            print("The provided list of uuids is empty.")
        else:
            post_url = f"{self.url}/timeseries/"
            r = requests.post(url=post_url, headers=self.headers, data=json.dumps(timeseries_uuid_list))
            r.raise_for_status()

    def delete_timeseries(self, timeseries_uuid_list):
        """
        Function to delete timeseries to the monitoringnetwork.
        This automatically deletes the locations related to the timeseries to the network

        args:
            - a list of uuids of the timeseries to delete
        """
        if len(timeseries_uuid_list) == 0:
            print("The provided list of uuids is empty.")
        else:
            post_url = f"{self.url}/timeseries/"
            r = requests.delete(url=post_url, headers=self.headers, data=json.dumps(timeseries_uuid_list))
            r.raise_for_status()