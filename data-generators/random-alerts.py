import requests
import time
import random
from datetime import datetime, timedelta
import schedule
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Get the directory of the current script
script_dir = Path(__file__).parent

# Construct the path to .env.local within the script's directory
env_path = script_dir / '.env.local.session'
load_dotenv(dotenv_path=env_path)

TARGET_KEY = os.getenv('TINYBIRD_TARGET_TOKEN')

EVENTS_API_URL = "https://api.us-west-2.aws.tinybird.co/v0/events?name=nested_json"

# City names
cities = [
    "Akron", "Albuquerque", "Alexandria", "Amarillo", "Anchorage", "Arlington", "Atlanta", "Augusta", "Austin", "Baltimore",
    "Baton Rouge", "Birmingham", "Boise", "Boston", "Bridgeport", "Brownsville", "Buffalo", "Cape Coral", "Cary", "Chandler",
    "Charlotte", "Chattanooga", "Chesapeake", "Chicago", "Chula Vista", "Cincinnati", "Clarksville", "Colorado Springs", "Columbus",
    "Corona", "Corpus Christi", "Dallas", "Dayton", "Denver", "Des Moines", "Detroit", "Durham", "El Paso", "Elk Grove",
    "Escondido", "Eugene", "Fayetteville", "Fontana", "Fort Collins", "Fort Lauderdale", "Fort Lee", "Fort Wayne", "Fort Worth",
    "Fremont", "Fresno", "Fullerton", "Garden Grove", "Garland", "Gilbert", "Glendale", "Grand Prairie", "Grand Rapids", "Greensboro",
    "Hayward", "Henderson", "Hialeah", "Hollywood", "Houston", "Huntington Beach", "Huntsville", "Indianapolis", "Irvine", "Irving",
    "Jackson", "Jacksonville", "Jersey City", "Joliet", "Kansas City", "Knoxville", "Lakewood", "Lancaster", "Laredo", "Las Vegas",
    "Lexington", "Lincoln", "Little Rock", "Long Beach", "Los Angeles", "Louisville", "Lubbock", "Macon", "Madison", "Memphis",
    "Mesa", "Mesquite", "Miami", "Milwaukee", "Minneapolis", "Miramar", "Mobile", "Modesto", "Montgomery", "Moreno Valley",
    "Naperville", "Nashville", "New Orleans", "New York City", "Newark", "Newport News", "Norfolk", "North Las Vegas", "Oakland",
    "Oceanside", "Oklahoma City", "Omaha", "Ontario", "Orange", "Orlando", "Overland Park", "Oxnard", "Palmdale", "Pasadena",
    "Paterson", "Pembroke Pines", "Peoria", "Philadelphia", "Phoenix", "Pittsburgh", "Plano", "Pomona", "Pompano Beach",
    "Port St. Lucie", "Portland", "Providence", "Raleigh", "Rancho Cucamonga", "Reno", "Richmond", "Riverside", "Rochester",
    "Rockford", "Sacramento", "Salem", "Salinas", "Salt Lake City", "San Antonio", "San Bernardino", "San Diego", "San Francisco",
    "San Jose", "Santa Ana", "Santa Clarita", "Santa Rosa", "Savannah", "Scottsdale", "Seattle", "Shreveport", "Sioux Falls",
    "Spokane", "Springfield", "St. Louis", "St. Petersburg", "Stockton", "Sunnyvale", "Tacoma", "Tallahassee", "Tampa", "Tempe",
    "Toledo", "Torrance", "Tucson", "Tulsa", "Vancouver", "Virginia Beach", "Washington", "Wichita", "Winston-Salem", "Worcester",
    "Yonkers"
]

# Function to pick a random city
def random_city():
    return random.choice(cities)

# Function to post an alert
def post_alert():

    alert_types = [
        "Severe Thunderstorm Watch", "Severe Thunderstorm Warning", "Tornado Watch", "Tornado Warning", "Flood Watch",
        "Flood Warning", "Flash Flood Watch", "Flash Flood Warning", "High Wind Watch/Warning", "Dense Fog Advisory"
    ]

    message = {}

    # Set the expire_time to now + a random number of hours between 6-24
    expiration_time = (datetime.utcnow() + timedelta(hours=random.randint(6, 24))).strftime('%Y-%m-%dT%H:%M:%SZ')
    message['expire_time'] = expiration_time

    # Pick a random city
    site_name = random_city()

    # Pick a random alert type
    alert_type = random.choice(alert_types)

    message['message'] = f"Weather Alert for {site_name}. {alert_type}. Expires at {expiration_time}."
    message['source'] = 'dev'

    json_payload = {}
    json_payload['event_type'] = 'alert'

    # Set 'timestamp' to NOW in UTC
    json_payload['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_payload['site_name'] = site_name  # Use the selected site_name
    json_payload['message'] = message

    json_payload = json.dumps(json_payload)

    headers_target = {
        "Authorization": f"Bearer {TARGET_KEY}"
    }

    events_response = requests.post(EVENTS_API_URL, data=json_payload, headers=headers_target)
    if events_response.status_code == 202:
        print(f"ALERT posted successfully! {json_payload}")
    else:
        print(f"Failed to post data point. Status code: {events_response.status_code}")
        print(f"Response: {events_response.text}")

# Schedule the task to run at a random interval between 5 and 60 minutes
schedule.every(random.randint(1, 3)).minutes.do(post_alert)
# schedule.every(1).minutes.do(post_alert)

# Run any pending tasks now
schedule.run_all()

while True:
    schedule.run_pending()
    time.sleep(random.randint(1, 3))