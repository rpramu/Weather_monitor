import sqlite3
import requests
import logging
import schedule
import time
from datetime import datetime
import matplotlib.pyplot as plt


API_KEY = "3224254e17c121c489e40f55f05cd5c7"
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
THRESHOLDS = {'temperature': {'max': 35}}  #Alert if temperature > 35°C for 2 consecutive readings
DB_FILE = 'weather_mvp.db'





def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create a table to store raw weather readings
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        feels_like REAL,
        condition TEXT,
        timestamp INTEGER
    )
    ''')

    # Create a table to store daily summaries
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date TEXT,
        avg_temp REAL,
        max_temp REAL,
        min_temp REAL,
        dominant_condition TEXT
    )
    ''')

    # Create a table to store alerts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        alert_type TEXT,
        value REAL,
        timestamp INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

initialize_database()





def fetch_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Extract relevant data
        weather = {
            'city': city,
            'temperature': data['main']['temp'],  # in Kelvin
            'feels_like': data['main']['feels_like'],  # in Kelvin
            'condition': data['weather'][0]['main'],  # e.g., Clear, Rain, etc.
            'timestamp': data['dt']  # Unix timestamp
        }
        return weather
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {city}: {e}")
        return None





def process_weather_data(data):
    # Convert Kelvin to Celsius
    data['temperature'] = round(data['temperature'] - 273.15, 2)
    data['feels_like'] = round(data['feels_like'] - 273.15, 2)
    return data





def store_weather_data(data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO weather_data (city, temperature, feels_like, condition, timestamp)
    VALUES (?, ?, ?, ?, ?)
    ''', (data['city'], data['temperature'], data['feels_like'], data['condition'], data['timestamp']))
    
    conn.commit()
    conn.close()



def generate_daily_summary():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    for city in CITIES:
        cursor.execute('''
        SELECT temperature, condition FROM weather_data
        WHERE city = ? AND DATE(timestamp, 'unixepoch') = DATE('now')
        ''', (city,))
        
        results = cursor.fetchall()
        if results:
            temps = [r[0] for r in results]
            conditions = [r[1] for r in results]
            avg_temp = sum(temps) / len(temps)
            max_temp = max(temps)
            min_temp = min(temps)
            dominant_condition = max(set(conditions), key=conditions.count)  # Most frequent condition
            
            cursor.execute('''
            INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition)
            VALUES (?, DATE('now'), ?, ?, ?, ?)
            ''', (city, avg_temp, max_temp, min_temp, dominant_condition))
    
    conn.commit()
    conn.close()





def check_alerts(data):
    temperature = data['temperature']
    city = data['city']
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Fetch the last two temperature readings for this city
    cursor.execute('''
    SELECT temperature FROM weather_data WHERE city = ? ORDER BY timestamp DESC LIMIT 2
    ''', (city,))
    last_two = [r[0] for r in cursor.fetchall()]
    
    if len(last_two) == 2 and all(temp > THRESHOLDS['temperature']['max'] for temp in last_two):
        generate_alert(city, 'High Temperature', temperature)
    
    conn.close()

def generate_alert(city, alert_type, value):
    logging.info(f"Alert: {alert_type} in {city}. Value: {value}°C")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO alerts (city, alert_type, value, timestamp)
    VALUES (?, ?, ?, strftime('%s', 'now'))
    ''', (city, alert_type, value))
    
    conn.commit()
    conn.close()




def display_daily_summary():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM daily_summary WHERE date = DATE("now")')
    summaries = cursor.fetchall()
    
    if summaries:
        for summary in summaries:
            print(f"City: {summary[1]}, Avg Temp: {summary[3]:.2f}°C, Max Temp: {summary[4]:.2f}°C, Min Temp: {summary[5]:.2f}°C, Dominant Condition: {summary[6]}")
    else:
        print("No data for today yet.")
    
    conn.close()







def collect_weather_data():
    for city in CITIES:
        data = fetch_weather_data(city)
        if data:
            processed_data = process_weather_data(data)
            store_weather_data(processed_data)
            check_alerts(processed_data)

# Schedule the data collection every 5 minutes
schedule.every(1).minutes.do(collect_weather_data)

# Schedule daily summary at midnight
schedule.every().day.at("00:00").do(generate_daily_summary)
schedule.every().day.at("00:05").do(display_daily_summary)

# Main loop to run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)




