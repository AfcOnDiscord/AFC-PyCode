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

from quart import Quart, render_template, url_for, request, redirect, session
from datetime import datetime
from func.weather import get_weather

app = Quart(__name__, static_folder='static',
            template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
async def _searchWeb():
    if request.method == "POST":
        city = (await request.form)["city"]
        return redirect(url_for('_weather', city=city))
    return await render_template('index.html')


@app.route('/<city>')
async def _weather(city):
    weather = await get_weather(city)

    if weather is None:
        return await render_template('error.html')

    temp_celsius = weather.get('temp_celsius')
    windSpeedKmh = weather.get('windSpeedKmh')
    humidity = weather.get('humidity')
    sunriseTime = weather.get('sunriseTime')
    sunsetTime = weather.get('sunsetTime')
    icon = weather.get('icon')
    iconLink = weather.get('iconLink')
    main = weather.get('main')

    return await render_template('weather.html', city=city, temp_celsius=temp_celsius, windSpeedKmh=windSpeedKmh, humidity=humidity, sunriseTime=sunriseTime, sunsetTime=sunsetTime, icon=icon, iconLink=iconLink, main=main)


if __name__ == '__main__':
    app.run()
