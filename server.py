from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__) #this makes app a flask app

@app.route('/') #home page!
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city') #value comes from form data
    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        city = "Princeton Junction"

    weather_data = get_current_weather(city) 

    #if api doesn't find city... (then cod of api data == '404' meaning unsucessful)
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    #send data to template
    return render_template( #retrieves data from api, look at api dump for data
        "weather.html",
        title = weather_data["name"],
        status = weather_data["weather"][0]["description"].capitalize(),
        temp = f"{weather_data['main']['temp']:.1f}",
        feels_like = f"{weather_data['main']['feels_like']:.1f}"
    )

if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = 8000)