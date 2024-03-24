import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder
from flask import Flask, render_template

app = Flask(__name__)

def get_astronauts_info():
    url = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    astronauts_info = "There are currently {} astronauts on the ISS:\n".format(result['number'])
    for person in result["people"]:
        astronauts_info += f"{person['name']} - on board\n"
    return astronauts_info

astronaut_info = get_astronauts_info()
print("{}".format(astronaut_info.split("\n")[0]))
print("\n".join(astronaut_info.split("\n")[1:]))


def get_current_location():
    g = geocoder.ip("me")
    return g.latlng

def update_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    location = result["iss_position"]
    lat, lon = float(location["latitude"]), float(location["longitude"])
    return lat, lon

@app.route('/')
def index():
    astronauts_info = get_astronauts_info()
    current_location = get_current_location()
    info_to_display = astronauts_info 
    return render_template('index.html', info=info_to_display)

@app.route('/update')
def update_location():
    lat, lon = update_iss_location()
    return {'latitude': lat, 'longitude': lon}

if __name__ == '__main__':
    app.run(debug=True)
