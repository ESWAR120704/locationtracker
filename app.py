from flask import Flask, request, render_template, send_file
import phonenumbers
from phonenumbers import geocoder, carrier
import folium
from opencage.geocoder import OpenCageGeocode

app = Flask(__name__)

# Replace with your actual OpenCage API key
API_KEY = "738d9519d25f438ab362e14679737304"
geocoder_service = OpenCageGeocode(API_KEY)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        number = request.form.get("phone_number")
        
        # Debugging Output
        print(f"Received Number: {number}")

        if not number:
            return "Error: No phone number provided."

        try:
            # Parse phone number
            check_number = phonenumbers.parse(number, "CH")
            number_location = geocoder.description_for_number(check_number, "en")
            service_provider = carrier.name_for_number(phonenumbers.parse(number, "RO"), "en")

            print(f"Location: {number_location}, Provider: {service_provider}")

            # Get Latitude & Longitude
            result = geocoder_service.geocode(number_location)
            if result:
                lat, lng = result[0]['geometry']['lat'], result[0]['geometry']['lng']

                # Generate Map
                map_location = folium.Map(location=[lat, lng], zoom_start=9)
                folium.Marker([lat, lng], popup=number_location).add_to(map_location)
                map_location.save("templates/map.html")

                print("✅ Successfully Generated Map!")
                return render_template("result.html", location=number_location, provider=service_provider)
            else:
                return "❌ Error: Unable to retrieve location."
        except Exception as e:
            return f"⚠️ Error: {e}"

    return render_template("index.html")

@app.route("/map")
def show_map():
    try:
        return send_file("templates/map.html")
    except Exception as e:
        return f"⚠️ Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
