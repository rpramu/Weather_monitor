from app.database import get_db_connection
from config import CITIES

def generate_daily_summary():
    conn = get_db_connection()
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
            dominant_condition = max(set(conditions), key=conditions.count)
            
            cursor.execute('''
            INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition)
            VALUES (?, DATE('now'), ?, ?, ?, ?)
            ''', (city, avg_temp, max_temp, min_temp, dominant_condition))
    
    conn.commit()
    conn.close()

def display_daily_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM daily_summary WHERE date = DATE("now")')
    summaries = cursor.fetchall()
    
    if summaries:
        for summary in summaries:
            print(f"City: {summary[1]}, Avg Temp: {summary[3]:.2f}°C, Max Temp: {summary[4]:.2f}°C, Min Temp: {summary[5]:.2f}°C, Dominant Condition: {summary[6]}")
    else:
        print("No data for today yet.")
    
    conn.close()
