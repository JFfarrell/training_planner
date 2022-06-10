import json
import math


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


