import requests
import os
import time
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Process launch arguments.")

# Add the arguments
parser.add_argument('puuid', type=str, help='The puuid to use.')
parser.add_argument('region', type=str, help='The region to use.')

# Parse the arguments
args = parser.parse_args()

# Set the global variables
puuid = args.puuid
region = args.region
mmr_current = None

# Function to check and create a file if it doesn't exist
def check_and_create_file(filename):
    if not os.path.exists(filename):
        open(filename, 'w').close()

def fetch_and_parse_mmr():
    global mmr_current
    url = f"https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/{region}/{puuid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["data"]
        mmr_current = data["elo"] -2100
        print(f"MMR Current: {mmr_current}")
    else:
        print(f"Error fetching data. Status code: {response.status_code}")

def fetch_radiant_mmr():
    response = requests.get('https://api.henrikdev.xyz/valorant/v2/leaderboard/ap')
    data = response.json()
    radiantMMR = data['players'][499]['rankedRating'] if len(data['players']) > 499 else None
    print(f"Radiant MMR: {radiantMMR}")
    return radiantMMR

def calculate_rr_required():
    radiantMMR = fetch_radiant_mmr()
    if radiantMMR is not None and mmr_current is not None:
        rrRequired = radiantMMR - mmr_current 
        if rrRequired < 0:
            return "Player is Radiant"
        else:
            return rrRequired
    else:
        print("Error: radiantMMR or mmr_current is None")
        return None

def write_to_file(rrRequired):
    with open('/var/www/html/tr.txt', 'w') as file:
        if isinstance(rrRequired, str):
            file.write(rrRequired)
        else:
            file.write(f"{str(rrRequired)} RR Required for Radiant")

def main():
    while True:
        fetch_and_parse_mmr()
        rrRequired = calculate_rr_required()
        if rrRequired is not None:
            print(f"RR required for Radiant: {rrRequired}")
            write_to_file(rrRequired)
        time.sleep(20)

if __name__ == "__main__":
    main()