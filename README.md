# MongoDB Flask IoT Data Server

This is a Flask web app that exposes an API to insert and fetch data from a MongoDB.
The index.html page uses ApexCharts.js library to render data fetched via the API.

Currently supports temperature data but could be expanded to other types.

### Running The Project

You must complete these prerequisites:
- `pip install -r requirements.txt`
- Have a running instance of MongoDB Server
- Edit the `CONNECTION_STRING` value inside of `server_app.py` if you aren't using the default host and port for MongoDB.
  The default URL is `localhost:27017`.


To run the server:
```
python server_app.py
```

There is a script provided that can insert some randomized sample data for you on a 10 second interval.
To run it:
```
python post_temperature_10sec_interval.py
```

To View the charts page load `http://localhost:5000/`

There is a dropdown and number input box that can be used to set how much data to include in the chart.

