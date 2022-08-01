import json
import math
import requests
from config import credentials as secrets


def load_strava_data():
    file = open("strava.json")
    data = json.load(file)
    file.close()
    return data


def return_matching_strava_data(data, inbound_date):
    for i in data:
        date_item = i["start_date"]
        date = date_item.split("T")[0]

        if date == inbound_date:
            return_data = [(i["name"], i["type"], math.trunc(i["moving_time"]/60))]
            print("Returning data: ", return_data)
            return return_data
    return []


def extract_date_string_from(selected_date):
    selected_date_values = str(selected_date).strip(") ").split("(")[1].split(", ")

    new_values = []
    for value in selected_date_values:
        if int(value) < 10:
            value = f"0{value}"
        new_values.append(value)

    selected_date_values = new_values
    return f"{selected_date_values[0]}-{selected_date_values[1]}-{selected_date_values[2]}"


def fetch_strava_data():
    auth_url = "https://www.strava.com/oauth/token"
    activities_url = "https://www.strava.com/api/v3/athlete/activities?access_token="

    payload = {
        'client_id': secrets["strava"]["client_id"],
        'client_secret': secrets["strava"]["client_secret"],
        'refresh_token': secrets["strava"]["refresh_token"],
        'grant_type': "refresh_token",
        'f': 'json'
    }

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    print("res", res.json())

    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))

    param = {'per_page': 200, 'page': 5}
    access_url = activities_url + access_token
    print(access_url)
    my_dataset = requests.get(str(access_url)).json()
    print("My dataset: ", my_dataset)

    print(my_dataset[0]["name"])
    print(my_dataset[0]["map"]["summary_polyline"])

    with open("strava.json", 'w') as f:
        json.dump(my_dataset, f)
