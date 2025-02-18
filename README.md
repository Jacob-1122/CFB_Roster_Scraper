# CFB Roster Scraper

A Python script to retrieve NCAA football rosters from 2016-2024 using the College Football Data API.

## Features
- Fetches rosters for user-specified teams and years.
- Saves player information, including first and last appearances, to an Excel file.
- Handles API rate limits and retries automatically.
- Uses environment variables for secure API key storage.

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

Run the script and provide teams and years when prompted:
```bash
python CFB_Roster_Scraper.py
```

Results will be saved in the `CFB_Rosters/` folder.

## Example Output
- `Wisconsin_Roster.xlsx`
- `Oregon_Roster.xlsx`

## Contributing

Pull requests are welcome! Open an issue for bug reports or feature requests.
