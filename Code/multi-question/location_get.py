import requests
import json

def get_coordinates(location):
    # Define the Nominatim API endpoint
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    
    # Parameters for the Nominatim API request
    params = {
        "q": location,
        "format": "json",
    }
    
    # Make the request to Nominatim to get the coordinates
    response = requests.get(nominatim_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data:
            # Get the latitude and longitude of the first result
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return lat, lon
    return None

def get_current_weather(location, unit="celcius"):
    # Get the latitude and longitude of the location
    coordinates = get_coordinates(location)
    
    if coordinates:
        lat, lon = coordinates
        # Define the Open Meteo API endpoint and parameters
        openmeteo_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max",
            "timezone": "auto",
            "current_weather": "true",
        }

        # Make the HTTP request to the Open Meteo API
        response = requests.get(openmeteo_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            
            data = response.json()
            # print(data)

            # Extract the relevant weather information
            temperature = data["current_weather"]["temperature"]
            # forecast = data["current_weather"]["condition"]["text"]

            # Convert temperature to Fahrenheit if required
            # if unit.lower() == "fahrenheit":
            #     temperature = (temperature * 9/5) + 32

            # Create a weather_info dictionary
            weather_info = {
                "location": location,
                "latitude": lat,
                "longitude": lon,
                "temperature": temperature,
                "unit": unit,
                # "forecast": forecast,
            }

            # Return the weather information as a JSON string
            return json.dumps(data)
    
    # If the location or coordinates retrieval fails, return an error message
    return json.dumps({"error": "Failed to retrieve location or weather data"})

# Example usage:
location = "New York, USA"
weather_data = get_current_weather(location)
# print(weather_data)
