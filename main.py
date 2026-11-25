import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

WEATHER_PARAMS = {
    "lat": 45.406433,
    "lon": 11.876761,
    "appid": api_key,
    "cnt": 4
}

response = requests.get(OWM_Endpoint, params=WEATHER_PARAMS)
response.raise_for_status()
weather_data  = response.json()
# print(weather_data["list"][1]["weather"][0]["id"])

will_rain = False

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        print("Bring an umbrella!")
        will_rain = True
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's raining!",
        from_="whatsapp:+17372508034",
        to="whatsapp:+905060982399"
    )
    print(message.status)
