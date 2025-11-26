import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# your API_KEY, create one in .env if you do not have one (ORS_API_KEY = "your_api_key_here")
ORS_API_KEY = os.getenv("ORS_API_KEY")

# help function: convert coordinates to address
def _latlong_to_address(lat, lon):
    url = f"https://api.openrouteservice.org/geocode/reverse"

    params = {
        "api_key": ORS_API_KEY,
        "point.lat": lat,
        "point.lon": lon,
        "size": 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and "features" in data and len(data["features"]) > 0:
            # get the first feature's properties, usually the location info
            props = data["features"][0]["properties"]
            # if no such place data exists, return "Unknown location"
            return props.get("label", "Unknown location")
        return "Unknown location"
    
    except Exception as e:
        print(f"Error in coords_to_address: {e}")
        return "Error retrieving address"
    
# help function: calculate distance between two coordinates
def _get_route_data(start_lon, start_lat, end_lon, end_lat, profile):
    # profile can be driving-car, cycling-regular, foot-walking, etc.

    url = f"https://api.openrouteservice.org/v2/directions/{profile}"
    
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    # **The format of coordinates in ORS is [lon, lat]**
    body = {
        "coordinates": [[start_lon, start_lat], [end_lon, end_lat]],
        "units": "m"
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        data = response.json()

        # make sure there is at least one route
        if "routes" in data and len(data["routes"]) > 0:
            summary = data["routes"][0]["summary"]
            return {
                "distance_meters": summary.get("distance", 0),
                "duration_seconds": summary.get("duration", 0)
            }
        return None
    
    except Exception as e:
        print(f"Error in get_route_data: {e}")
        return None


# API endpoint: convert coordinates to address
@app.route('/coords_to_address', methods=['POST'])
def coords_to_address():
    data = request.get_json()

    # verify input
    if not data or "lat" not in data or "lon" not in data:
        return jsonify({"error": "Invalid input, 'lat' and 'lon' required"}), 400
    
    lat = data["lat"]
    lon = data["lon"]

    address = _latlong_to_address(lat, lon)

    if address:
        return jsonify({
            "status": "success",
            "data": {
                "coords": [lat, lon],
                "address": address
            }
        })
    
    else:
        return jsonify({"error": "Failed to retrieve address"}), 500

# API endpoint: calculate distance between two coordinates
@app.route('/calculate_distance', methods=['POST'])
def calculate_distance():
    data = request.get_json()

    # verify format (expecting {"start": [lat1, lon1], "end": [lat2, lon2])
    if not data or "start" not in data or "end" not in data:
        return jsonify({"error": "Invalid input, 'start' and 'end' coordinates required"}), 400
    
    # extract coordinates
    start_lat, start_lon = data["start"]
    end_lat, end_lon = data["end"]

    # get driving data and walking data
    drive_data = _get_route_data(start_lon, start_lat, end_lon, end_lat, "driving-car")
    walk_data = _get_route_data(start_lon, start_lat, end_lon, end_lat, "foot-walking")

    # distance in km, duration in minutes
    response_data = {
        "start_coords": [start_lat, start_lon],
        "end_coords": [end_lat, end_lon],
        "driving": {
            "distance_km": round(drive_data["distance_meters"]/1000, 2),
            "duration_min": round(drive_data["duration_seconds"]/60, 1)
        },
        "walking": {
            "distance_km": round(walk_data["distance_meters"]/1000, 2),
            "duration_min": round(walk_data["duration_seconds"]/60, 1)
        }
    }

    return jsonify({
        "status": "success",
        "data": response_data
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)


