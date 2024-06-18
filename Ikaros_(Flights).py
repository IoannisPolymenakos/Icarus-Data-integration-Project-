import requests
import cx_Oracle

# List of fromId values
from_ids = [
    "eyJlIjoiOTU2NzM2MjQiLCJzIjoiQVRIIiwiaCI6IjI3NTQ4MTc0IiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiMTI4NjY4NDY4IiwicyI6IkFPSyIsImgiOiIyNzUzNjU4NSIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY4MzA1IiwicyI6IkFYRCIsImgiOiIyNzU0ODIyMCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiOTU2NzQyNTIiLCJzIjoiQ0ZVIiwiaCI6IjI3NTM5NzY3IiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiOTU2NzQxNDMiLCJzIjoiQ0hRIiwiaCI6IjI3NTM5Nzg5IiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiOTU2NzQ0MDciLCJzIjoiRUZMIiwiaCI6IjM4MzEwOTcyIiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiOTU2NzQxNDIiLCJzIjoiSEVSIiwiaCI6IjI3NTQyMDI4IiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiOTU2NzQzMTQiLCJzIjoiSU9BIiwiaCI6IjI3NTQyODczIiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiMTI4NjY3OTI2IiwicyI6IkpJSyIsImgiOiI4MTk3MjUwNiIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiOTU2NzM0MDIiLCJzIjoiSktIIiwiaCI6IjI3NTQyOTkxIiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiOTU2NzQ0MTAiLCJzIjoiSktMIiwiaCI6IjM4MzE0OTYxIiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiMTA0MTIwMzMxIiwicyI6IkpNSyIsImgiOiIzODMwNDM2MCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY4NzA5IiwicyI6IkpOWCIsImgiOiIyNzU0MzAwOCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY4NTYwIiwicyI6IkpTSCIsImgiOiIyNzU0MzAyNCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY4NzExIiwicyI6IkpTSSIsImgiOiIyNzU0MzAyNSIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY3NTAwIiwicyI6IkpTWSIsImgiOiI4MTk3MjQ4OSIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiOTU2NzQxNDQiLCJzIjoiSlRSIiwiaCI6IjM4MzA4ODg0IiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiMTI4NjY3OTg0IiwicyI6IkpUWSIsImgiOiIzODUwODEwOCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTA0MTIwMjYxIiwicyI6IktHUyIsImgiOiI4MTk3MjQ0NCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY4NzM2IiwicyI6IktJVCIsImgiOiIyNzU0Mzg2OCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY3NDk0IiwicyI6IktMWCIsImgiOiIyNzU0MzkwMCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY3MTIxIiwicyI6IktTSiIsImgiOiI4MTk3MjQ0MiIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY3NTQwIiwicyI6IktTTyIsImgiOiIyNzU0MzgyNSIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY3OTcwIiwicyI6IktWQSIsImgiOiIyNzU0MzkzMiIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY3NDkwIiwicyI6IktaSSIsImgiOiIyNzU0Mzk1NyIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY3MTE3IiwicyI6IktaUyIsImgiOiIzODU1NDQ3NCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY3OTYwIiwicyI6IkxSUyIsImgiOiI0NDU2NDA3NCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTI4NjY4Njg5IiwicyI6IkxYUyIsImgiOiI4MTk3MjUwOCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiOTU2NzM0MDAiLCJzIjoiTUpUIiwiaCI6IjI3NTQ0OTQ0IiwidCI6IkFJUlBPUlQifQ==",
    "eyJlIjoiMTA0MTIwMzMzIiwicyI6Ik1MTyIsImgiOiIyNzU0NDk2NCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTA0MTIwMzMyIiwicyI6IlBBUyIsImgiOiIyNzU0NTI5NCIsInQiOiJBSVJQT1JUIn0=",
    "eyJlIjoiMTA0MTIwMjY0IiwicyI6IlJITyIsImgiOiIyNzU0NjE2MiIsInQiOiJBSVJQT1JUIn0="
]

# API request URL
url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-everywhere"

# Common query parameters
common_querystring = {
    "adults": "1",
    "cabinClass": "economy",
    "currency": "EUR",
    "market": "GR",
    "locale": "el-GR"
}

# Headers for the API request
headers = {
    "x-rapidapi-key": "dfaab71a31mshb65dc4767a71b66p18ddffjsnaf241a3bd992",
    "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
}

# Database connection details
dsn = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
connection = cx_Oracle.connect(user='System', password='13101993gP', dsn=dsn)
cursor = connection.cursor()

# Insert query
insert_query = '''
INSERT INTO Flights_From_Greek_Airports_Final (ID, LocationName, SkyCode, CheapestPrice, CheapestDirect, DirectPrice, FromId, DepartDate)
VALUES (:1, :2, :3, :4, :5, :6, :7, TO_DATE(:8, 'YYYY-MM-DD'))
'''

# Iterate over each fromId
for from_id in from_ids:
    # Update the departure date to today's date
    future_depart_date = "2024-06-24"



    # Create the querystring for the current fromId
    querystring = common_querystring.copy()
    querystring.update({
        "fromId": from_id,
        "departDate": future_depart_date
    })

    # Perform the API request
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # Check if 'data' key is present
    if 'data' in data and 'everywhereDestination' in data['data'] and 'results' in data['data'][
        'everywhereDestination']:
        results = data['data']['everywhereDestination']['results']
    else:
        print(f"No results found for fromId {from_id}.")
        continue

    # Insert data into the database
    for result in results:
        content = result['content']
        location = content['location']

        flight_quotes = content.get('flightQuotes', {})
        cheapest = flight_quotes.get('cheapest', {})
        direct = flight_quotes.get('direct', {})

        cursor.execute(
            insert_query,
            (
                result['id'],
                location['name'],
                location['skyCode'],
                cheapest.get('rawPrice', None),
                'True' if cheapest.get('direct', False) else 'False',
                direct.get('rawPrice', None),
                from_id,
                future_depart_date
            )
        )

# Commit the transaction
connection.commit()

# Close the connection
cursor.close()
connection.close()
