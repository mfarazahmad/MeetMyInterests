import os
import time
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re
from fuzzywuzzy import fuzz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Replace these with your own API key and Steam ID
API_KEY = os.environ.get('STEAM_API_KEY')
STEAM_ID = os.environ.get('STEAM_ID')

# Function to fetch owned games
def get_steam_library(api_key, steam_id):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        'key': api_key,
        'steamid': steam_id,
        'include_appinfo': True,  # Includes game names
        'include_played_free_games': True,  # Includes free games
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "response" in data and "games" in data["response"]:
            return [{"AppID": game["appid"], "Name": game["name"]} for game in data["response"]["games"]]
        else:
            print("No games found or API limit exceeded.")
            return []
    else:
        print(f"Error: {response.status_code}")
        return []

# Fetch game details from Steam Store API
def get_game_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and str(appid) in data and data[str(appid)]["success"]:
            game_data = data[str(appid)]["data"]
            genres = ", ".join(genre.get("description", "Unknown") for genre in game_data.get("genres", []))
            
            raw_date = game_data.get("release_date", {}).get("date", "Unknown")
            try:
                release_date = pd.to_datetime(raw_date, format='%b %d, %Y', errors='coerce')
            except Exception:
                release_date = None
            
            return {
                "Category": genres if genres else "Unknown",
                "Date": release_date if release_date else "Unknown",
                "Metacritic": game_data.get("metacritic", {}).get("score", "N/A")
                    }
    return {"Category": "Unknown", "Date": "Unknown", "Metacritic": "N/A"}

# Function to fetch GeForce Now games
def fetch_geforce_now_games():
    url = "https://www.nvidia.com/en-us/geforce-now/games/"

    # Set up Selenium WebDriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")

    # Automatically download and use the correct ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)

        # Wait for the main-container to load
        wait = WebDriverWait(driver, 15)
        main_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "main-container")))

        # Scroll down to load all content (if applicable)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "li")))

        # Extract game titles from the main-container
        games = []
        game_elements = main_container.find_elements(By.TAG_NAME, "li")
        for game_element in game_elements:
            game_name = game_element.text.strip()
            if game_name:
                games.append(game_name)

        return games
    finally:
        driver.quit()  # Ensure the WebDriver is closed



# Function to fetch Boosteroid games 
def fetch_boosteroid_games():
    url = "https://www.ytechb.com/boosteroid-cloud-gaming-the-complete-games-list/"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve Boosteroid games page")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    games = []
    for section in soup.find_all("li"):
        game_name = section.text.strip()
        if game_name:
            games.append(game_name)
    return games

# Common articles to exclude from matching
ARTICLES = {"the", "a", "an", "of", "and", "in", "on", "at", "to", "with", "for"}

def remove_articles(name):
    words = name.split()
    return " ".join(word for word in words if word.lower() not in ARTICLES)

def is_partial_match(game_name, target_list, threshold=90):
    processed_game_name = remove_articles(game_name)
    for target in target_list:
        processed_target = remove_articles(target) 
        if game_name == target:
            return True
        elif fuzz.partial_ratio(processed_game_name, processed_target) >= threshold:
            return True
    return False

def format_and_sort_games(games):
    if not games:
        print("Warning: The 'games' list is empty.")
        # Return an empty DataFrame with the expected columns
        return pd.DataFrame(columns=["Name", "Year"])

    # Ensure all entries have required keys
    cleaned_games = []
    for game in games:
        cleaned_game = {
            "Name": game.get("Name", "Unknown Title"),
            "Date": game.get("Date", "Unknown"),
            **{key: value for key, value in game.items() if key not in ["Name", "Date"]}  # Preserve other keys
        }
        cleaned_games.append(cleaned_game)
    
    # Convert to DataFrame
    df = pd.DataFrame(cleaned_games)
    
    # Process Year column
    df['Year'] = pd.to_datetime(
        df['Date'], errors='coerce'
    ).dt.year

    # Fill missing or invalid data
    df['Year'] = df['Year'].fillna("Unknown")
    df['Name'] = df['Name'].fillna("Unknown Title")
    
    # Sort by Year and Name
    df = df.sort_values(by=['Name', 'Year'], ascending=[True, True])

    # Drop the Date column if it exists
    if 'Date' in df.columns:
        df = df.drop(columns=['Date'])
    
    return df


def main():
    owned_games = get_steam_library(API_KEY, STEAM_ID)
    geforce_now_games = fetch_geforce_now_games()
    boosteroid_games = fetch_boosteroid_games()

    if not (owned_games and geforce_now_games and boosteroid_games):
        print("Failed to fetch all data.")
        return

    # Enhance library with additional details
    enhanced_library = [
        {**game, **get_game_details(game["AppID"])} for game in owned_games
    ]

    # Categorize games
    not_in_geforce_now = [
        game for game in enhanced_library
        if not is_partial_match(game["Name"], geforce_now_games)
    ]
    not_in_boosteroid = [
        game for game in enhanced_library
        if not is_partial_match(game["Name"], boosteroid_games)
    ]
    in_geforce_now = [
        game for game in enhanced_library
        if is_partial_match(game["Name"], geforce_now_games)
    ]
    in_boosteroid = [
        game for game in enhanced_library
        if is_partial_match(game["Name"], boosteroid_games)
    ]

    not_in_either = [
        game for game in enhanced_library
        if not is_partial_match(game["Name"], geforce_now_games) and not is_partial_match(game["Name"], boosteroid_games)
    ]

    # Format and sort DataFrames
    not_in_geforce_now_df = format_and_sort_games(not_in_geforce_now)
    not_in_boosteroid_df = format_and_sort_games(not_in_boosteroid)
    in_geforce_now_df = format_and_sort_games(in_geforce_now)
    in_boosteroid_df = format_and_sort_games(in_boosteroid)
    not_in_either_df = format_and_sort_games(not_in_either)

    # Calculate percentages
    total_games = len(enhanced_library)
    stats = {
        "not_in_geforce_now_percentage": (len(not_in_geforce_now) / total_games) * 100,
        "not_in_boosteroid_percentage": (len(not_in_boosteroid) / total_games) * 100,
        "in_geforce_now_percentage": (len(in_geforce_now) / total_games) * 100,
        "in_boosteroid_percentage": (len(in_boosteroid) / total_games) * 100,
        "not_in_either_percentage": (len(not_in_either) / total_games) * 100,
    }

    # Add summary rows
    for df, key, summary_key in [
        (not_in_geforce_now_df, "not_in_geforce_now_percentage", "Percentage Not In GeForce Now"),
        (not_in_boosteroid_df, "not_in_boosteroid_percentage", "Percentage Not In Boosteroid"),
        (in_geforce_now_df, "in_geforce_now_percentage", "Percentage In GeForce Now"),
        (in_boosteroid_df, "in_boosteroid_percentage", "Percentage In Boosteroid"),
        (not_in_either_df, "not_in_either_percentage", "Percentage Not In Either"),
    ]:
        summary_row = {
            "Name": "Summary",
            "Year": "N/A",
            summary_key: stats[key]
        }
        df.loc[len(df)] = summary_row

    # Save CSVs
    save_stats_to_csv(not_in_geforce_now_df, "not_in_geforce_now.csv")
    save_stats_to_csv(not_in_boosteroid_df, "not_in_boosteroid.csv")
    #save_stats_to_csv(in_geforce_now_df, "in_geforce_now.csv")
    #save_stats_to_csv(in_boosteroid_df, "in_boosteroid.csv")
    save_stats_to_csv(not_in_either_df, "not_in_either.csv")


def save_stats_to_csv(df, filename):
    output_path = f"./stats/{filename}"
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()

