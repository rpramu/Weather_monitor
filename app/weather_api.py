import requests
import logging
from app.database import get_db_connection
from config import API_KEY

def fetch_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather = {
            'city': city,
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'condition': data['weather'][0]['main'],
            'timestamp': data['dt']
        }
        return weather
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {city}: {e}")
        return None

def process_weather_data(data, unit='Celsius'):
    # Convert Kelvin to Celsius or Fahrenheit
    if unit == 'Celsius':
        data['temperature'] = round(data['temperature'] - 273.15, 2)
        data['feels_like'] = round(data['feels_like'] - 273.15, 2)
    elif unit == 'Fahrenheit':
        data['temperature'] = round((data['temperature'] - 273.15) * 9/5 + 32, 2)
        data['feels_like'] = round((data['feels_like'] - 273.15) * 9/5 + 32, 2)
    return data

def store_weather_data(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO weather_data (city, temperature, feels_like, condition, timestamp)
    VALUES (?, ?, ?, ?, ?)
    ''', (data['city'], data['temperature'], data['feels_like'], data['condition'], data['timestamp']))
    
    conn.commit()
    conn.close()
