# CFB Roster Scraper

A Python script to retrieve NCAA football rosters for a specific list of schools from 2016-2024 using the College Football Data API.

## Features
- Fetches rosters for a pre-defined list of schools (see script) and years (2016-2024).
- Saves player information (name, home city, home state) to an Excel file per team.
- Handles API rate limits and retries automatically.
- Uses environment variables for secure API key storage.
- No user input required; just run the script.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CFB_Roster_Scraper.git
   cd CFB_Roster_Scraper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get an API Key from [College Football Data API](https://collegefootballdata.com/).
4. Create a `.env` file in the project directory and add your API key:
   ```
   CFB_API_KEY=your_api_key_here
   ```

## Usage

Just run the script:
```bash
python CFB_Roster_Scraper.py
```

- The script will automatically fetch and save rosters for the specified schools and years.
- Results will be saved in the `CFB_Rosters/` folder (which is ignored by git).

## Example Output
- `CFB_Rosters/Wisconsin_Roster.xlsx`
- `CFB_Rosters/Oregon_Roster.xlsx`

## Notes
- The `CFB_Rosters/` directory is ignored by git (see `.gitignore`).
- Only the specified list of schools will be processed. To change the list, edit the `TEAMS` variable in the script.

## Contributing

Pull requests are welcome! Open an issue for bug reports or feature requests.
