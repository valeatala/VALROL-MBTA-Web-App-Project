import os
import urllib.request
from dotenv import load_dotenv
import json
import requests

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")
GOOGLE_PLACES_API = os.getenv("GOOGLE_PLACES_API")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
GOOGLE_BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    response = requests.get(url,verify=False)
    return response.json()
     
     # we added this because we expected many errors when inputing the location into our website
     # we asked AI what our problem was, and recommended to add this to the code
     # this skips SSL verification, since our error was an SSL error
     
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))

    # this grabs the data from the url we provided and returns a dictionary

    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    #pass


def get_lat_lng(place_name: str) -> tuple[str, str]:
    
    query = urllib.parse.quote(place_name)
    url = f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi"
    data = get_json(url)
    
    if data ["features"]:
        coordinates  = data ["features"][0]["geometry"]["coordinates"]
        longitude, latitude = coordinates [0], coordinates[1]
        return str (latitude), str (longitude)
    else:
        return None, None
    
    # this gives us a the latitude and longitude from the place provided,
    # using help from the MAPBOX API
    # if the place is not found, it returns None
    
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    # pass


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    
    url = f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&sort=distance&filter[latitude]={latitude}&filter[longitude]={longitude}"
    data = get_json(url)
    
    if data ["data"]:
        nearest_stop = data["data"][0]
        station_name= nearest_stop["attributes"]["name"]
        wheelchair_accesible = nearest_stop["attributes"]["wheelchair_boarding"] == 1
        return station_name, wheelchair_accesible
    else:
        return None, None
    
    # using lat and long, and the MBTA url and API , this defines
    # the nearest station to the location/place that is put as input
    # it also indicates whether it is wheelchair friendly or not
    # if there is no station found, it returns none
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    # pass

def get_nearby_coffee (latitude: str, longitude: str) -> list:
    url = (f"{GOOGLE_BASE_URL}?location={latitude},{longitude}"
           f"&radius=300&type=cafe&keyword=coffee&key={GOOGLE_PLACES_API}")
    data = get_json(url)
    
    # this link specifies the chosen radius for the nearby coffee shop
    
    coffee_shops= []
    for shop in data.get("results",[]):
        shop_name = shop.get("name")
        shop_adress = shop.get("vicinity")
        coffee_shops.append((shop_name, shop_adress))
    
    return coffee_shops

# here is where we decided to add our WOW factor
# we decided to also include nearby coffee shops for those
# who want a drink before heading to their train station
# we used Google Places API for this

# word 

def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    
    latitude, longitude = get_lat_lng (place_name)
    if latitude is None or longitude is None:
        return "Location error, enter a new location " , False
    
    station_name , wheelchair_accesible = get_nearest_station (latitude, longitude)
    if station_name:
        coffee_shops = get_nearby_coffee(latitude, longitude)
        return station_name, wheelchair_accesible, coffee_shops
    else:
        return "no nearby MBTA stations" , False, []
    
    # this code returns coffee shops and nearest MBTA station depending on the location that was inputed
    #if location is not found, it will give an error message
    # if there is no nearby MBTA stations, it will also return a message
    # pass


def main():
    """
    You should test all the above functions here
    """
    place = " 660 Washington St"
    station_name, accesible,coffee_shops = find_stop_near(place)
    accesible_message = "is wheelchair friendly" if accesible else "is not wheelchair friendly"
    print (f"The nearest MBTA station to {place} is {station_name}, and it {accesible_message}.")
    
    if coffee_shops:
        print("\nNearby coffee shops:")
        for shop_name, shop_adress in coffee_shops:
            print (f"- {shop_name}, located at {shop_adress}")
    else:
        print ("\nNo nearby coffee shops found within 300 meters")
    
    # this tests the function by testing out a location
    # you input location in "place"
    # the result will give you whether it is wheelchair friendly or not
    # as well as giving you the nearby coffee shops within a 300 meter radius
    
    
    # pass


if __name__ == "__main__":
    main()
