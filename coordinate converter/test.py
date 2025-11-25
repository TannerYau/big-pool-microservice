import unittest
import requests

class TestLiveServer(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5001/to_dd'

    def test_dms_conversion(self):
        """test dms to dd conversion on live server"""
        payload = {'lat_long': "22°17'7.87\"N, 114°9'27.68\"E"}

        try:
            # send post request
            response = requests.post(self.BASE_URL, json=payload)

            # check response status code
            self.assertEqual(response.status_code, 200, f"Expected status code 200, got {response.status_code}")

            # check response content
            data = response.json()
            print(f"Sent: {payload['lat_long']}, Received: {data['dd_value']}")

        except requests.exceptions.RequestException as e:
            self.fail(f"Request failed: {e}")

    def test_ddm_conversion(self):
        """test ddm to dd conversion on live server"""
        payload = {'lat_long': "22° 18' N, 114° 10' E"}

        try:
            # send post request
            response = requests.post(self.BASE_URL, json=payload)

            # check response status code
            self.assertEqual(response.status_code, 200, f"Expected status code 200, got {response.status_code}")

            # check response content
            data = response.json()
            print(f"Sent: {payload['lat_long']}, Received: {data['dd_value']}")

        except requests.exceptions.RequestException as e:
            self.fail(f"Request failed: {e}")

if __name__ == '__main__':
    unittest.main()