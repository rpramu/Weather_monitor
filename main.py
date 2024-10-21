import schedule
import time
import uvicorn
from app.weather_api import fetch_weather_data, process_weather_data, store_weather_data
from app.alerts import check_alerts
from app.summary import generate_daily_summary, display_daily_summary
from config import CITIES
from app.database import initialize_database

initialize_database()

def collect_weather_data():
    for city in CITIES:
        data = fetch_weather_data(city)
        if data:
            processed_data = process_weather_data(data)
            store_weather_data(processed_data)
            check_alerts(processed_data)

schedule.every(1).minutes.do(collect_weather_data)
schedule.every().day.at("00:00").do(generate_daily_summary)
schedule.every().day.at("00:05").do(display_daily_summary)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    from threading import Thread
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()
    
    uvicorn.run("app.fastapi_routes:app", host="0.0.0.0", port=8000)
