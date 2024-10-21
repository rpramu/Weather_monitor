// Fetch Weather Data
function fetchWeatherData() {
    const city = document.getElementById('weather-city').value;
    if (!city) return;

    // Ensure the correct URL path is used here
    fetch(`/weather/${city}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('weather-data').innerHTML = `
                <p>City: ${data.city}</p>
                <p>Temperature: ${data.temperature}°C</p>
                <p>Feels Like: ${data.feels_like}°C</p>
                <p>Condition: ${data.condition}</p>
            `;
        });
}

// Fetch Daily Summary
function fetchDailySummary() {
    const city = document.getElementById('weather-city').value;
    const date = document.getElementById('summary-date').value;
    if (!city || !date) return;

    fetch(`/daily_summary/${city}?date=${date}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('daily-summary').innerHTML = `
                <p>Average Temperature: ${data.avg_temp}°C</p>
                <p>Max Temperature: ${data.max_temp}°C</p>
                <p>Min Temperature: ${data.min_temp}°C</p>
                <p>Dominant Condition: ${data.dominant_condition}</p>
            `;
        })
        .catch(err => {
            document.getElementById('daily-summary').innerHTML = `<p>No data available for this date.</p>`;
        });
}

// Fetch Alerts
function fetchAlerts() {
    fetch('/alerts')
        .then(response => response.json())
        .then(data => {
            const alertHTML = data.map(alert => `
                <p>City: ${alert.city}, Type: ${alert.alert_type}, Value: ${alert.value}°C</p>
            `).join('');
            document.getElementById('alerts').innerHTML = alertHTML;
        });
}

// Fetch Temperature Trend Plot
function fetchPlot() {
    const city = document.getElementById('plot-city').value;
    if (!city) return;

    document.getElementById('plot-image').src = `/plot/${city}`;
    document.getElementById('plot-image').style.display = 'block';
}
