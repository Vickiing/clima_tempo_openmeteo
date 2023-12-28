import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from geopy.geocoders import Nominatim


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 60)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

days = 16

url_antiga = "https://api.open-meteo.com/v1/forecast" 
url = f"https://api.open-meteo.com/v1/forecast?forecast_days={days}"

# Inicializa o geocodificador
geolocator = Nominatim(user_agent="geoapi_zonasul")
locations = ["Copacabana", "Catete"]

for localizacao in locations:
    location = geolocator.geocode(localizacao)
    latitude = location.latitude
    longitude = location.longitude

    params = {
        "latitude": latitude,
        "longitude": longitude,
        #"start_date": "2023-12-13",
        #"end_date": "2024-01-12",
        "hourly": "temperature_2m"
    }

    print(f'Local: {localizacao} - Parametros:{params}')
    
    responses = openmeteo.weather_api(url, params=params)

    # Process each response for the location
    for response in responses:
        print(f"Coordenadas {response.Latitude()}°E {response.Longitude()}°N")
        print(f"Elevacao {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s"),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )
        }
        hourly_data["temperature_2m"] = hourly_temperature_2m
        region_names = [localizacao] * len(hourly_data["date"])
        hourly_data["region"] = region_names
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        with open ("teste_dados_clima.txt", "a") as arquivo:
            hourly_dataframe.columns =['Data', 'Temperatura', 'Local']
            arquivo.write(hourly_dataframe.to_string(index=False, header=True))
            arquivo.write("\n")
