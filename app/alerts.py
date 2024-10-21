from app.database import get_db_connection
from config import THRESHOLDS


def check_alerts(data):
    temperature = data['temperature']
    city = data['city']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT temperature FROM weather_data WHERE city = ? ORDER BY timestamp DESC LIMIT 2
    ''', (city,))
    last_two = [r[0] for r in cursor.fetchall()]
    
    if len(last_two) == 2 and all(temp > THRESHOLDS['temperature']['max'] for temp in last_two):
        generate_alert(city, 'High Temperature', temperature)
    
    conn.close()

def generate_alert(city, alert_type, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO alerts (city, alert_type, value, timestamp)
    VALUES (?, ?, ?, strftime('%s', 'now'))
    ''', (city, alert_type, value))
    
    conn.commit()
    conn.close()
