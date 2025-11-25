from flask import Flask, request, jsonify
from lat_lon_parser import parse


app = Flask(__name__)

@app.route('/to_dd', methods=['POST'])
def convert_to_dd():
    """
    recieves a coordinate in DMS or DDM format and converts it to DD format
    """

    if not request.is_json:
        return jsonify({'error': 'Invalid input, JSON expected'}), 400

    data = request.get_json()
    
    # get the coordinate from the json payload
    single_coord = data.get('lat_long', None)

    # check if coordinate is provided
    if not single_coord:
        return jsonify({'error': 'No coordinate provided'}), 400

    response = {}

    try:
        # need to seperate lat and long
        if "," in single_coord:
            parts = single_coord.split(",")
            lat = parts[0].strip()
            lon = parts[1].strip()

        # convert the coordinate to DD format
        response['lat_dd'] = parse(lat)
        response['lon_dd'] = parse(lon)
        response['dd_value'] = f"{response['lat_dd']}, {response['lon_dd']}"
        return jsonify(response), 200
    
    except ValueError:
        return jsonify({'error': 'Invalid coordinate format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)









