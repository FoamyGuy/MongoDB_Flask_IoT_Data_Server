import datetime
import json

from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, request, Response, send_from_directory
from bson.json_util import dumps

app = Flask(__name__)

def utc_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)
def get_database(name):
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create / Get the database and return the connection to it.
    return client[name]

@app.route("/", methods=['GET'])
def index():
    return send_from_directory("static", "index.html")


@app.route("/temperature", methods=['GET', 'POST'])
def temperature():
    """
    URL: /temperature
    Methods: GET, POST

    Fetch or Insert Temperature data.

    GET Args:
      device_id (string): The device ID to fetch data for
      time_ago_unit (string): The units to measure the time interval in. Valid values: min, hour, day
      time_ago_value (number): The value of the time interval. E.g. 5 min will fetch data for the last 5 minutes.

    POST Content-Type: application/json
    POST Args (JSON Body):
      device_id (string): The device ID to insert the new data reading for
      temperature (float): The temperature reading value.
    """
    db = get_database("iot_data")
    temperature_data = db["temperatures"]
    if request.method == 'GET':
        device_id = request.args.get("device_id")
        time_ago_unit = request.args.get("time_ago_unit")
        time_ago_value = request.args.get("time_ago_value")

        valid_time_ago_units = ("min", "hour", "day")

        find_arg = {}
        if device_id is not None:
            #all_temperatures = temperature_data.find({"device_id": device_id})
            find_arg["device_id"] = device_id
        if time_ago_value is not None:
            if time_ago_unit is None:
                time_ago_unit = "min"
            else:
                if time_ago_unit not in valid_time_ago_units:
                    return Response(json.dumps({"error", "invalid time_ago_unit"}), content_type="application/json")
            utc_time = utc_now()

            if time_ago_unit == "min":
                start_time = utc_time - datetime.timedelta(minutes=int(time_ago_value))
            elif time_ago_unit == "hour":
                start_time = utc_time - datetime.timedelta(hours=int(time_ago_value))
            elif time_ago_unit == "day":
                start_time = utc_time - datetime.timedelta(days=int(time_ago_value))

            find_arg["timestamp"] = {"$gte": start_time}

        if len(find_arg) == 0:
            all_temperatures = temperature_data.find()
        else:
            all_temperatures = temperature_data.find(find_arg)
        return Response(dumps(all_temperatures), content_type="application/json")

    if request.method == 'POST':
        json_data = request.get_json()
        required_fields = ["temperature", "device_id"]
        missing_fields = []
        for field in required_fields:
            if field not in json_data:
                missing_fields.append(field)
        if len(missing_fields) > 0:
            return json.dumps({"error": "Missing fields: {}".format(missing_fields)})

        json_data["timestamp"] = utc_now()
        result = temperature_data.insert_one(json_data)
        return json.dumps({"result": str(result)})

if __name__ == '__main__':
    app.run()