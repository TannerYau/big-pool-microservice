import requests
import json

BASE_URL = "http://localhost:5001"



def test_coords_to_address():
    print("Testing /coords_to_address endpoint...")

    url = f"{BASE_URL}/coords_to_address"

    payload = {
        "lat": 22.2951,
        "lon": 114.1717
    }

    try:
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("Success:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("Error:")
            print(response.text)

    except Exception as e:
        print(f"Exception during request: {e}")

def test_calculate_distance():
    print("Testing /calculate_distance endpoint...")

    url = f"{BASE_URL}/calculate_distance"

    
    payload = {
        "start": [22.3185, 114.1686],
        "end": [22.2937, 114.1695]
    }

    try:
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("Success:")
            print(json.dumps(data, indent=2, ensure_ascii=False))

        else:
            print("Error:")
            print(response.text)

    except Exception as e:
        print(f"Exception during request: {e}")

if __name__ == "__main__":
    test_coords_to_address()
    test_calculate_distance()

