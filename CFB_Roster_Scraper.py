import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("CFB_API_KEY")

if not API_KEY:
    raise ValueError("Missing API Key! Please set CFB_API_KEY in a .env file.")

BASE_URL = "https://apinext.collegefootballdata.com/roster"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

# Automatically set years 2016-2024
YEARS = list(range(2016, 2025))

# List of schools to include
TEAMS = [
    "Wisconsin", "Oregon", "Utah", "USC", "Texas A&M", "North Carolina State", "Texas", "Minnesota", "Kentucky", "Kansas State", "Miami (FL)", "Florida", "Florida State", "West Virginia", "Auburn", "Wake Forest", "Tennessee", "Pitt", "Ole Miss", "Washington State", "Missouri", "Louisville", "Mississippi State", "Virginia Tech", "Iowa State", "Michigan State", "Buffalo", "North Carolina", "Boston College", "Northwestern", "Stanford", "South Carolina", "UCLA", "Baylor", "Arizona State", "Texas Tech", "Duke", "Maryland", "California", "Georgia Tech", "Virginia", "Indiana", "Colorado", "Syracuse", "Oregon State", "Nebraska", "Arkansas", "Illinois", "Arizona", "Vanderbilt", "Rutgers", "Kansas"
]

SAVE_DIR = "CFB_Rosters"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_roster(year):
    """Fetches all teams' rosters for a specific year."""
    params = {"year": year}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    print(f"Requesting {response.url}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error: Response is not in JSON format.")
            return None
    elif response.status_code == 401 or response.status_code == 403:
        print("Unauthorized! Check your API key.")
        return None
    elif response.status_code == 429:
        print(f"Rate limited! Waiting 15 seconds before retrying {year}...")
        time.sleep(15)
        return fetch_roster(year)  # Retry
    else:
        print(f"Error fetching roster for {year}: {response.status_code}")
        return None

# Dictionary to hold player data per team
temp_team_player_years = {}

for year in YEARS:
    roster = fetch_roster(year)
    if roster is None:
        continue
    for player in roster:
        team = player.get('team', 'Unknown')
        if team not in TEAMS:
            continue
        if team not in temp_team_player_years:
            temp_team_player_years[team] = {}
        first_name = player.get('firstName', 'Unknown')
        last_name = player.get('lastName', 'Unknown')
        name = f"{first_name} {last_name}".strip()
        home_city = player.get('homeCity', 'Unknown')
        home_state = player.get('homeState', 'Unknown')
        player_dict = temp_team_player_years[team]
        if name not in player_dict:
            player_dict[name] = {
                # "Start Year": year,
                # "End Year": year,
                "Home City": home_city,
                "Home State": home_state
            }
        else:
            # player_dict[name]["End Year"] = year
            pass
    print(f"Retrieved all rosters for {year}")
    time.sleep(2)

# Save Excel files per team
for team, player_years in temp_team_player_years.items():
    if player_years:
        df = pd.DataFrame.from_dict(player_years, orient="index").reset_index()
        df.rename(columns={"index": "Player"}, inplace=True)
        file_path = os.path.join(SAVE_DIR, f"{team.replace(' ', '_')}_Roster.xlsx")
        df.to_excel(file_path, index=False)
        print(f"Saved {team} roster to {file_path}")
    else:
        print(f"No data available for {team}")

print("All rosters downloaded successfully!")
