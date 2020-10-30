import requests
import json

# Basic function to get the current weather of a user's location based on the inputs city and state
def get_weather(city, state):
    url = "http://api.openweathermap.org/data/2.5/weather?"
    q = "q=" + city + "," + state                           # Set the string query parameters for the location of the user
    units = "&units=imperial"                               # Set the units of measurement (hard-coded as imperial, but this can be set to be by user preference)
    key = "&appid=77d0aa9c2f5fa4e1c6a4e4e87d644e52"         # API key, do NOT hard-code API key in prototype
    get = url + q + units + key                             # Create the full API call
    resp = requests.get(get).json()

    # Print the json response of the api call
    # print(json.dumps(resp, indent=4))

    weather_type = resp["weather"][0]["description"]
    weather_temp = resp["main"]["temp"]

    print("The current weather in " + city + " is " + weather_type + " with a temperature of " + str(round(weather_temp)) + " degrees Fahrenheit.")

# Example function call, state parameter must be in ISO-3166 format
get_weather("Los Angeles","US-CA")