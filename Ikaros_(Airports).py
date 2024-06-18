import requests
import cx_Oracle

# Skyscanner API details
url = "https://sky-scanner3.p.rapidapi.com/flights/airports"
headers = {
    "x-rapidapi-key": "dfaab71a31mshb65dc4767a71b66p18ddffjsnaf241a3bd992",
    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
}

# Fetch data from Skyscanner API
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    print("Keys in the response:", data.keys())  # Print the keys of the JSON response
    print("Sample data:", data)  # Print a sample of the data
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    exit()

# Assuming the correct key for the airports data
airports_key = None
for key in data.keys():
    if isinstance(data[key], list) and data[key] and isinstance(data[key][0], dict):
        airports_key = key
        break

if airports_key:
    print(f"Found airports data under key '{airports_key}'")

    # Database connection details
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
    conn = cx_Oracle.connect(user='System', password='13101993gP', dsn=dsn_tns)

    # Create a cursor object
    cursor = conn.cursor()

    # Initialize counters
    inserted_count = 0
    skipped_count = 0

    # Insert data into Oracle DB
    for airport in data[airports_key]:
        iata = airport.get('iata')
        icao = airport.get('icao')
        name = airport.get('name')
        location = airport.get('location')
        time = airport.get('time')
        id = airport.get('id')
        skyId = airport.get('skyId')

        # Skip records with missing mandatory fields
        if not iata or not name:
            print(f"Skipping airport with missing mandatory fields: {airport}")
            skipped_count += 1
            continue

        sql_insert = """INSERT INTO Airports (iata, icao, name, location, time, id, skyId)
                        VALUES (:1, :2, :3, :4, :5, :6, :7)"""
        cursor.execute(sql_insert, (
            iata,
            icao,
            name,
            location,
            time,
            id,
            skyId
        ))
        inserted_count += 1

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Summary of operations
    print(f"Inserted records: {inserted_count}")
    print(f"Skipped records: {skipped_count}")

else:
    print("No suitable key for airport data found in the JSON response.")