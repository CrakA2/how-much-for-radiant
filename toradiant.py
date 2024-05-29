import requests
import os
import time
import argparse


print("Checkout the source code at:")
print("https://github.com/CrakA2/how-much-for-radiant")
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
    headers = {'Authorization': 'HDEV-2f464838-0399-4bfd-9c01-1b22e6f4f5ac'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        data = response.json()["data"]
        mmr_current = data["elo"] -2100
        print(f"MMR Current: {mmr_current}")
    except (requests.HTTPError, KeyError, ValueError):
        print("Error fetching or parsing data.")

def fetch_radiant_mmr():
    headers = {'Authorization': 'HDEV-2f464838-0399-4bfd-9c01-1b22e6f4f5ac'}
    try:
        response = requests.get('https://api.henrikdev.xyz/valorant/v2/leaderboard/ap', headers=headers)
        response.raise_for_status()
        data = response.json()
        radiantMMR = data['players'][499]['rankedRating'] if len(data['players']) > 499 else None
        print(f"Radiant MMR: {radiantMMR}")
        return radiantMMR
    except (requests.HTTPError, KeyError, ValueError):
        print("Error fetching or parsing data.")

def calculate_rr_required():
    radiantMMR = fetch_radiant_mmr()
    if radiantMMR is not None and mmr_current is not None:
        if mmr_current < 0:
            return "Player is not Immortal"
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
        file.write(str(rrRequired))

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