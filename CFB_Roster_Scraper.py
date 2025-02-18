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

# User input for teams
teams_input = input("Enter team names (comma-separated): ")
TEAMS = [team.strip() for team in teams_input.split(",")]

# User input for years
years_input = input("Enter years (comma-separated, e.g., 2016,2017,2020): ")
YEARS = [int(year.strip()) for year in years_input.split(",")]

SAVE_DIR = "CFB_Rosters"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_roster(team, year):
    """Fetches a single team's roster for a specific year."""
    params = {"team": team, "year": year}
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
        print(f"Rate limited! Waiting 15 seconds before retrying {team} {year}...")
        time.sleep(15)
        return fetch_roster(team, year)  # Retry
    else:
        print(f"Error fetching roster for {team} in {year}: {response.status_code}")
        return None

# Fetch and save rosters
for team in TEAMS:
    player_years = {}
    for year in YEARS:
        roster = fetch_roster(team, year)
        if roster is None:
            continue
        
        for player in roster:
            first_name = player.get('firstName', 'Unknown')
            last_name = player.get('lastName', 'Unknown')
            name = f"{first_name} {last_name}".strip()
            
            if name not in player_years:
                player_years[name] = {"Start Year": year, "End Year": year}
            else:
                player_years[name]["End Year"] = year
        
        print(f"Retrieved {team} roster for {year}")
        time.sleep(2)
    
    if player_years:
        df = pd.DataFrame.from_dict(player_years, orient="index").reset_index()
        df.rename(columns={"index": "Player"}, inplace=True)
        file_path = os.path.join(SAVE_DIR, f"{team.replace(' ', '_')}_Roster.xlsx")
        df.to_excel(file_path, index=False)
        print(f"Saved {team} roster to {file_path}")
    else:
        print(f"No data available for {team}")

print("All rosters downloaded successfully!")
