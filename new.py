import phonenumbers
from phonenumbers import geocoder, carrier
import folium
from opencage.geocoder import OpenCageGeocode

# Importing the phone number from a separate file (ensure 'number' is defined in 'test.py')
from test import number

# Define your OpenCage API key (replace 'YOUR_API_KEY' with your actual key)
key = "738d9519d25f438ab362e14679737304"
geocoder_service = OpenCageGeocode(key)

# Get the location of the phone number
check_number = phonenumbers.parse(number, "CH")
number_location = geocoder.description_for_number(check_number, "en")
print(f"Location: {number_location}")

# Get the service provider of the phone number
service_provider = carrier.name_for_number(phonenumbers.parse(number, "RO"), "en")
print(f"Service Provider: {service_provider}")

# Geocoding the location to get latitude and longitude
query = str(number_location)
result = geocoder_service.geocode(query)

if result and len(result) > 0:
    lat = result[0]['geometry']['lat']
    lng = result[0]['geometry']['lng']
    print(f"Latitude: {lat}, Longitude: {lng}")

    # Create a map with the location
    map_location = folium.Map(location=[lat, lng], zoom_start=9)
    folium.Marker([lat, lng], popup=number_location).add_to(map_location)

    # Save the map to an HTML file
    map_location.save("Location.html")
    print("Map has been saved as 'Location.html'")
else:
    print("Error: Unable to find the coordinates for the given location.")
