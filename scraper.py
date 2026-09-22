import os
import json
import requests
from datetime import datetime

DATA_FILE = "data.json"

def load_database():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_database(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def run_scraper():
    database = load_database()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # OFFICIAL WEB REPOSITORY SOURCE STREAM
    LIVE_API_URL = "https://githubusercontent.com"
    
    print("Fetching official historical draws from the live database network...")
    try:
        response = requests.get(LIVE_API_URL, timeout=20)
        if response.status_code == 200:
            incoming_data = response.json()
            
            # Merge verified live data records from 2024 to present day
            synced_count = 0
            for date_key, draws in incoming_data.items():
                if date_key >= "2024-01-01":
                    database[date_key] = draws
                    synced_count += 1
            print(f"Successfully synchronized {synced_count} real official draw dates.")
        else:
            print(f"Data host mirror responded with an error code status: {response.status_code}")
    except Exception as e:
        print(f"Network request timed out. Retaining local backup layer. Error: {str(e)}")

    # COMPREHENSIVE DAY OBJECT LOOKUP FOR AWAITING PROFILE MODES
    # Generates a clean template fallback layout structure covering ALL PCSO categories smoothly
    if today_str not in database:
        database[today_str] = [
            # Major Jackpot Games
            { "game": "Ultra Lotto 6/58", "numbers": ["Awaiting", "Draw", "--", "--", "--", "--"], "jackpot": "9:00 PM Broadcast" },
            { "game": "Grand Lotto 6/55", "numbers": ["Awaiting", "Draw", "--", "--", "--", "--"], "jackpot": "9:00 PM Broadcast" },
            { "game": "Super Lotto 6/49", "numbers": ["Awaiting", "Draw", "--", "--", "--", "--"], "jackpot": "9:00 PM Broadcast" },
            { "game": "Mega Lotto 6/45", "numbers": ["Awaiting", "Draw", "--", "--", "--", "--"], "jackpot": "9:00 PM Broadcast" },
            { "game": "Lotto 6/42", "numbers": ["Awaiting", "Draw", "--", "--", "--", "--"], "jackpot": "9:00 PM Broadcast" },
            # Fixed Digit Games
            { "game": "6D Lotto", "numbers": ["--", "--", "--", "--", "--", "--"], "jackpot": "9:00 PM Broadcast" },
            { "game": "4D Lotto", "numbers": ["--", "--", "--", "--"], "jackpot": "9:00 PM Broadcast" },
            { "game": "3D Lotto", "numbers": ["--", "--", "--"], "jackpot": "2PM - 5PM - 9PM Draws" },
            { "game": "2D Lotto", "numbers": ["--", "--"], "jackpot": "2PM - 5PM - 9PM Draws" }
        ]

    save_database(database)
    print("Database sync process complete.")

if __name__ == "__main__":
    run_scraper()
