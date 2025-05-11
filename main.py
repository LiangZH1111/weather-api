from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID","STANAME                                 "]]

# Home page
@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

# For data on a date at a station
@app.route("/api/v1/<station>/<date>")
def on_date(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"]=="1860-01-05"]["   TG"].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}

# For all data at a station
@app.route("/api/v1/<station>")
def at_station(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result

# For a year of data at a station
@app.route("/api/v1/yearly/<station>/<year>")
def in_year(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result
if __name__ == "__main__":
    app.run(debug=True)