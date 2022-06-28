import json
import math
import requests
from config import credentials as secrets


def check_data():
    file = open("strava.json")
    data = json.load(file)

    file.close()
    return data


def check_date(data, inbound_date):
    for i in data:
        date_item = i["start_date"]
        date = date_item.split("T")[0]

        if date == inbound_date:
            return_data = [(i["name"], i["type"], math.trunc(i["moving_time"]/60))]
            return return_data


def write_json(date, workout_data, filename='training.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        print("file data: ", file_data)
        file_data[date] = workout_data
        print("file data: ", file_data)

        # Join new_data with file_data inside emp_details
        # file_data[date].append(workout_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def date_string(selected_date):
    selected_date_values = str(selected_date).strip(") ").split("(")[1].split(", ")

    new_values = []
    for value in selected_date_values:
        if int(value) < 10:
            value = f"0{value}"
        new_values.append(value)

    selected_date_values = new_values
    print(selected_date_values)
    return f"{selected_date_values[0]}-{selected_date_values[1]}-{selected_date_values[2]}"


def get_data():
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