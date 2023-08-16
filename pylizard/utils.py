import requests
import pandas as pd
from .config import *

def get_organisation_endpoint_assets(endpoint, dataformat, organisation_uuid, json_field, headers):
    """
    Function that handles all endpoint asset requests.
    Generally used in the methods of pylizard classes that start with 'get_'
    """
    if endpoint == 'timeseries':
        next_url = f'{LIZARD_BASE_URL}/{endpoint}/?location__organisation__uuid={organisation_uuid}&limit=250'
    else:
        next_url = f'{LIZARD_BASE_URL}/{endpoint}/?organisation__uuid={organisation_uuid}&limit=250'

    uuid_list = []
    df_list = []

    while next_url != None:       
        r = requests.get(url=next_url, headers=headers)
        results = r.json()["results"]

        if dataformat == "list":
            for result in results:
                uuid_list.append(result[json_field])
        elif dataformat == "df":
            for result in results:
                df_list.append(result)

        next_url = r.json()['next']

    if dataformat == "list":
        return uuid_list
    elif dataformat == "df":
        df = pd.DataFrame(df_list)
        return df