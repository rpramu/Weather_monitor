from fastapi import FastAPI
from app.weather_api import fetch_weather_data, process_weather_data
from app.summary import display_daily_summary
from app.database import get_db_connection
from fastapi import FastAPI, HTTPException
from app.database import get_db_connection
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import io
import os
from sqlite3 import connect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io




app = FastAPI()

DB_FILE = 'weather_mvp.db'


app.mount("/static", StaticFiles(directory="static"), name="static")


# Root route to serve the HTML file
@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    with open("templates/index.html") as f:
        return f.read()



@app.get("/weather/{city}")
def get_weather(city: str, unit: str = 'Celsius'):
    data = fetch_weather_data(city)
    if data:
        processed_data = process_weather_data(data, unit)
        return processed_data
    else:
        return {"error": "Could not retrieve data"}

@app.get("/daily_summary")
def get_daily_summary():
    return display_daily_summary()


@app.get("/all_weather_data")
def get_all_weather_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM weather_data")
    weather_data = cursor.fetchall()
    
    conn.close()
    return weather_data



@app.get("/daily_summary/{city}")
def get_daily_summary(city: str, date: Optional[str] = None):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT city, date, avg_temp, max_temp, min_temp, dominant_condition
    FROM daily_summary
    WHERE city = ? AND date = ?
    ''', (city, date))
    
    summary = cursor.fetchone()
    
    conn.close()
    
    if summary is None:
        raise HTTPException(status_code=404, detail=f"No summary found for {city} on {date}.")
    
    return {
        "city": summary[0],
        "date": summary[1],
        "avg_temp": summary[2],
        "max_temp": summary[3],
        "min_temp": summary[4],
        "dominant_condition": summary[5]
    }



@app.get("/plot/{city}")
async def plot_temperature(city: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Fetch temperature data for the last 7 days
    cursor.execute('''
        SELECT temperature, timestamp FROM weather_data
        WHERE city = ? AND timestamp >= strftime('%s', 'now', '-7 days')
        ORDER BY timestamp
    ''', (city,))
    
    results = cursor.fetchall()
    conn.close()

    if not results:
        raise HTTPException(status_code=404, detail="No temperature data found for the specified city.")

    # Prepare data for plotting
    temperatures = [r[0] for r in results]
    timestamps = [datetime.fromtimestamp(r[1]) for r in results]

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temperatures, marker='o', linestyle='-', color='b')
    plt.title(f'Temperature Trend for {city}')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid()

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Clear the current figure to free memory
    plt.clf()
    
    return StreamingResponse(buf, media_type='image/png')




@app.get("/alerts")
def get_alerts():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT city, alert_type, value FROM alerts')
    alerts = cursor.fetchall()
    
    conn.close()

    if not alerts:
        return ["No alerts found"]  

    return [{'city': alert[0], 'alert_type': alert[1], 'value': alert[2]} for alert in alerts]
