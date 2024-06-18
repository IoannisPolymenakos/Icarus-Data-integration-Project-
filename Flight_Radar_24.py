import requests
import cx_Oracle
from datetime import datetime

# Oracle connection details
dsn = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
connection = cx_Oracle.connect(user='System', password='13101993gP', dsn=dsn)
cursor = connection.cursor()

# List of IATA codes
iata_codes = ['ATH', 'SKG', 'HER', 'JMK', 'CHQ', 'PAS', 'JNX', 'JTR']

# Function to insert data into Oracle
def insert_data(airport_info, weather_info, departures_data, today_stats):
    # Preparing values
    iata_code = airport_info['code']['iata']
    name = airport_info['name']
    city = airport_info['city']
    country = airport_info['country']['name']
    icao_code = airport_info['code']['icao']
    latitude = airport_info['latitude']
    longitude = airport_info['longitude']

    temperature = f"{weather_info['temp']['celsius']}°C ({weather_info['temp']['fahrenheit']}°F)"
    wind_direction = weather_info['wind']['direction']['text']
    wind_speed = f"{weather_info['wind']['speed']['kmh']} km/h ({weather_info['wind']['speed']['kts']} kts / {weather_info['wind']['speed']['mph']} mph) - {weather_info['wind']['speed']['text']}"
    sky_condition = weather_info['sky']['condition']['text']

    delay_index = departures_data['index']
    average_delay = departures_data['averageDelayMin']
    on_time_flights = departures_data['ontime']
    delayed_flights = departures_data['delayed']
    cancelled_flights = departures_data['cancelled']
    trend = departures_data['trend']
    delayed_percentage = departures_data['delayedPercentage']
    cancelled_percentage = departures_data['cancelledPercentage']

    total_flights_today = today_stats['total']
    delayed_flights_today = today_stats['delayed']
    cancelled_flights_today = today_stats['cancelled']

    # Check if IATA code exists in Flight_Radar_Airport_Info table
    cursor.execute("SELECT COUNT(*) FROM Flight_Radar_Airport_Info WHERE IATA_Code = :iata_code", {"iata_code": iata_code})
    exists = cursor.fetchone()[0] > 0

    if not exists:
        # Insert data into the Flight_Radar_Info table
        cursor.execute("""
            INSERT INTO Flight_Radar_Airport_Info (
                Name, City, Country, IATA_Code, ICAO_Code, Latitude, Longitude
            ) VALUES (:1, :2, :3, :4, :5, :6, :7)
        """, (name, city, country, iata_code, icao_code, latitude, longitude))

    # Insert data into the Flight_Radar_Airport_Stats table
    cursor.execute("""
        INSERT INTO Flight_Radar_Airport_Stats (
            Stat_Date, IATA_Code, Temperature, Wind_Direction, Wind_Speed, Sky_Condition,
            Delay_Index, Average_Delay, On_time_Flights, Delayed_Flights, Cancelled_Flights, Trend,
            Total_Flights_Today, Delayed_Flights_Today, Cancelled_Flights_Today, Delayed_Percentage, Cancelled_Percentage
        ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17)
    """, (datetime.now(), iata_code, temperature, wind_direction, wind_speed, sky_condition,
          delay_index, average_delay, on_time_flights, delayed_flights, cancelled_flights, trend,
          total_flights_today, delayed_flights_today, cancelled_flights_today, delayed_percentage, cancelled_percentage))

# Loop through the list of IATA codes
for iata_code in iata_codes:
    # API request
    url = "https://flightradar243.p.rapidapi.com/v1/airports/disruptions"
    querystring = {"code": iata_code}
    headers = {
        "x-rapidapi-key": "dfaab71a31mshb65dc4767a71b66p18ddffjsnaf241a3bd992",
        "x-rapidapi-host": "flightradar243.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # Check if 'data' key is in the response
    if 'data' in data and 'data' in data['data']:
        airport_data = data['data']['data']
        # Fetching data for a specific airport
        if 'airport' in airport_data:
            airport_info = airport_data['airport']
            weather_info = airport_info.get('weather', {})
            departures_data = airport_data.get('departures', {}).get('live', {})
            today_stats = airport_data.get('departures', {}).get('today', {})
            insert_data(airport_info, weather_info, departures_data, today_stats)
        else:
            print(f"No 'airport' key in data for IATA code {iata_code}")
    else:
        print(f"No 'data' key in response for IATA code {iata_code}")
        print(data)  # Print the entire response for debugging

# Commit the transaction
connection.commit()

# Close the connection
cursor.close()
connection.close()

print("Data inserted successfully!")
