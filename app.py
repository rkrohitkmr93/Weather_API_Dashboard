from flask import Flask, render_template, request
import requests
import configparser


app = Flask(__name__)
app.debug = True

@app.route('/')
def weather_dashboard():
  return render_template('home.html')

@app.route('/results', methods = ['POST'])
def results():
  zip_code = request.form['zipCode']

  api_key = get_api_key()
  data = get_weather_results(zip_code, api_key)
  temp = "{0:.2f}".format(data["main"]["temp"])
  #print(type(temp))
  temp_c = float(temp)
  temp_c=str(temp_c-273.15)
  #print(type(temp_c))
  feels_like = "{0:.2f}".format(data["main"]["feels_like"])
  f_c = float(feels_like)
  
  f_c = str(f_c-273.15)
 
  weather = data["weather"][0]["main"]
  location = data["name"]

  return render_template('results.html', location = location,
    temp = temp_c, feels_like = f_c, weather = weather)



def get_api_key():
  config = configparser.ConfigParser()
  config.read('config.ini')
  return config['openweathermap']['api']

def get_weather_results(zip_code, api_key):
  #api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
            #api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={your api key}
  api_url = "https://api.openweathermap.org/data/2.5/weather?zip={},IN&appid={}".format(zip_code, api_key)
  r = requests.get(api_url)
  return r.json()


if __name__ == '__main__':
  app.run()