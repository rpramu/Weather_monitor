

# Weather Monitoring Application

## Overview

The Weather Monitoring Application is a comprehensive system that retrieves, stores, and visualizes weather data for various cities in India. Built using FastAPI, SQLite, and Matplotlib, this application allows users to access real-time weather information, alerts for high temperatures, and daily weather summaries, as well as visual representations of temperature trends.

## Architecture

### Components

- **FastAPI:** A modern web framework for building APIs with Python 3.6+ based on standard Python type hints. It handles all HTTP requests and responses.
- **SQLite:** A lightweight database for storing weather data, alerts, and daily summaries. 
- **Matplotlib:** A plotting library for Python that is used to generate visualizations of temperature trends.
- **Docker:** Containerization tool that simplifies deployment and scalability by allowing the application to run in isolated environments.

### Application Flow

1. **Data Retrieval:** The application fetches weather data from the OpenWeatherMap API at regular intervals.
2. **Data Processing:** The retrieved data is processed, including temperature conversion and alert checking.
3. **Data Storage:** Processed data is stored in an SQLite database for persistence.
4. **Alert Generation:** The system generates alerts for high temperatures based on defined thresholds.
5. **Daily Summaries:** A summary of daily weather statistics is generated for each city.
6. **Data Visualization:** Temperature trends can be visualized through dynamically generated plots.
7. **Frontend Interface:** A simple web interface allows users to interact with the API and view weather data, alerts, and summaries.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.6+
- Pip (Python package manager)
- Docker (for containerized deployment)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/weather_monitor.git
   cd weather_monitor
   ```

2. **Set Up a Virtual Environment (Optional but Recommended):**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database:**

   Before running the application, initialize the SQLite database by running:

   ```bash
   python app/initialize_db.py
   ```

### Configuration

- **API Key:** Add your OpenWeatherMap API key in the code where required.

### Running the Application

#### Method 1: Using Uvicorn

1. Start the FastAPI server:

   ```bash
   uvicorn app.fastapi_routes:app --reload
   ```

2. Access the application at `http://127.0.0.1:8000`.

#### Method 2: Using Docker

1. Build the Docker image:

   ```bash
   docker build -t weather_monitor_app .
   ```

2. Run the Docker container:

   ```bash
   docker run -d -p 8000:8000 weather_monitor_app
   ```

3. Access the application at `http://127.0.0.1:8000`.

### API Endpoints

- `GET /weather/{city}`: Retrieve current weather data for a specified city.
- `GET /alerts`: Retrieve active weather alerts.
- `GET /daily_summary`: Retrieve daily weather summary.
- `GET /plot/{city}`: Retrieve a plot of temperature trends for the last 7 days for the specified city.

### Frontend Interface

1. Access the frontend at `http://127.0.0.1:8000`.
2. Use the interface to view weather data, alerts, and temperature plots.

### Testing

You can manually test the API endpoints using tools like [Postman](https://www.postman.com/) or [cURL](https://curl.se/).

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLite](https://www.sqlite.org/)
- [Matplotlib](https://matplotlib.org/)
- [OpenWeatherMap API](https://openweathermap.org/api)

---
