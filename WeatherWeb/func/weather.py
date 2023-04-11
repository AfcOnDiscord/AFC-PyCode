# ----------------- WATERMARK ----------------- #
"""
 ________  ________ ________
|\   __  \|\  _____\\   ____\
\ \  \|\  \ \  \__/\ \  \___|
 \ \   __  \ \   __\\ \  \
  \ \  \ \  \ \  \_| \ \  \____
   \ \__\ \__\ \__\   \ \_______\
    \|__|\|__|\|__|    \|_______|
"""
# ----------------- WATERMARK ----------------- #
import os
import datetime as dt
import aiohttp
from dotenv import load_dotenv, find_dotenv

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = f"http://api.openweathermap.org/data/2.5/weather?"


async def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius


async def get_weather(city):
    URL = f"{BASE_URL}appid={API_KEY}&q={city}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            text = await resp.json()
    try:
        temp_kelvin = text.get('main').get('temp', "N/A")
        temp_celsius = await kelvin_to_celsius(temp_kelvin)
        windSpeedms = text.get('wind').get('speed', "N/A")
        windSpeedMph = windSpeedms * 3.6 / 1.61
        windSpeedKmh = windSpeedms * 3.6
        humidity = text.get('main').get('humidity', "N/A")
        sunriseTime = dt.datetime.utcfromtimestamp(
            text.get('sys').get('sunrise', "N/A") + text.get('timezone', "N/A")).strftime("%H:%M")  # Aufgang
        sunsetTime = dt.datetime.utcfromtimestamp(
            text.get('sys').get('sunset', "N/A") + text.get('timezone', "N/A")).strftime("%H:%M")  # Untergang

        icon = text.get('weather')[0].get('icon', "N/A")
        iconLink = f"https://openweathermap.org/img/wn/{icon}@2x.png"

        main = text.get('weather')[0].get('main', "N/A")

        weather = {
            'temp_celsius': f"{temp_celsius:.0f}",
            'windSpeedms': windSpeedms,
            'windSpeedMph': windSpeedMph,
            'windSpeedKmh': f"{windSpeedKmh:.0f}",
            'humidity': humidity,
            'sunriseTime': sunriseTime,
            'sunsetTime': sunsetTime,
            'icon': icon,
            'iconLink': iconLink,
            'main': main
        }

        return weather
    except Exception as e:
        print(e)
        return None
