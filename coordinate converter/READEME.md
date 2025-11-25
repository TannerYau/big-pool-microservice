# Coordinate Converter Microservice

A Flask-based microservice for converting geographic coordinates. Specifically designed to handle **DMS** (Degrees Minutes Seconds) and **DDM** (Degrees Decimal) formates, converting them into standard **DD** (Decimal Degrees) for easier database storage and processing.  

# Installation

After cloning: pip install -r requirements.txt  

..venv\Scripts\Activate to use on powershell  

# Usage
Run the coord_converter.py  
*The server will start on 'http://127.0.0.1:5001'*  
*Endpoint: 'POST /to_dd'*  

Request (JSON): 
Send a JSON object with the **lat_long** key containing your coordinate string.

example:
```
{
    "lat_long": "22°17'7.87\"N, 114°9'27.68\"E"
}
```

Response (JSON)
Returns the converted coordinates in Decimal Degrees (DD).

example:
```
{
    "lat_dd": "22.285519",
    "lng_dd": "114.157689",
    "dd_value": "22.285519, 114.157689"
}
```