import requests
import pandas as pd
from .config import *


def get_organisation_endpoint_assets(
    endpoint, return_format, organisation_uuid, json_field, headers
):
    """
    Function that handles the Organisation class get methods.
    """
    if endpoint == "timeseries":
        next_url = f"{LIZARD_BASE_URL}/{endpoint}/?location__organisation__uuid={organisation_uuid}&limit=250"
    else:
        next_url = f"{LIZARD_BASE_URL}/{endpoint}/?organisation__uuid={organisation_uuid}&limit=250"

    uuid_list = []
    df_list = []

    while next_url != None:
        r = requests.get(url=next_url, headers=headers)
        results = r.json()["results"]

        if return_format == "list":
            for result in results:
                uuid_list.append(result[json_field])
        elif return_format == "df":
            for result in results:
                df_list.append(result)

        next_url = r.json()["next"]

    if return_format == "list":
        return uuid_list
    elif return_format == "df":
        df = pd.DataFrame(df_list)
        return df


def get_monitoringnetwork_enpoint_assets(endpoint, return_format, url, headers):
    """
    Function that handles the monitoringnetwork class get methods.
    """
    uuid_list = []
    df_list = []
    next_url = f"{url}/{endpoint}/?limit=250"

    while next_url != None:
        r = requests.get(next_url, headers=headers)
        results = r.json()["results"]

        if return_format == "list":
            for result in results:
                uuid_list.append(result["uuid"])
        elif return_format == "df":
            for result in results:
                df_list.append(result)

        next_url = r.json()["next"]

    if return_format == "list":
        return uuid_list
    elif return_format == "df":
        df = pd.DataFrame(df_list)
        return df
