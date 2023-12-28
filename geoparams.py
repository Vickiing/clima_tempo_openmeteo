from geopy.geocoders import Nominatim

# Inicializa o geocodificador
geolocator = Nominatim(user_agent="geoapiExercises")
locations = ["Copacabana", "Catete"]
for localizacao in locations:
    location = geolocator.geocode(localizacao)
    latitude = location.latitude
    longitude = location.longitude

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": "2023-12-11",
        "end_date": "2023-12-25",
        "hourly": "temperature_2m"
    }
    print(params)