import json
import time
import argparse
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init


# Initialize colorama
def run():
    init(autoreset=True)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Transfer Spotify playlists to Fizy.')
    parser.add_argument('json_file', type=str, help='Path to the JSON file containing playlist data')
    args = parser.parse_args()

    json_file_path = args.json_file

    if not json_file_path:
        print(Fore.RED + "Error: JSON file path not provided.")
        sys.exit(1)

    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(Fore.RED + f"Error: {e}")
        sys.exit(1)

    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    driver.get('https://account.fizy.com/login')
    user_input = input(Fore.GREEN + "Press Enter to continue after completing the login process..." + Fore.RED + " If you want to exit, type 'esc' and press Enter: ")
    
    if user_input.lower() == 'esc':
        driver.quit()
        return

    isNewPlaylist = True
    isHeaderMusic = False
    isNoSearchResult = False
    for playlist in data['playlists']:
        driver.get('https://play.fizy.com/my-music/')
        time.sleep(2)
        playlist_name = playlist['name']
        view_exists_playlist = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/ui-view/my-music/div/div[3]/my-playlists/div/div[1]/playlist-card/list-card/div/div[2]/a[1]'))
        )
        playlist_value = view_exists_playlist.text.strip()
        time.sleep(2)
        print(Fore.RED + f"Playlist name: {playlist_name}" + Fore.GREEN + f" Your First Playlist value: {playlist_value}")

        if playlist_value == playlist_name:
            print(Fore.RED + f"Playlist already exists: {playlist_name}")
            isNewPlaylist = False
        else:
            print(Fore.GREEN + "Creating a new playlist: " + playlist['name'])
            isNewPlaylist = True

        driver.get('https://play.fizy.com/search')
        time.sleep(3)
        for item in playlist['items']:
            track = item['track']
            song_name = f"{track['artistName']} {track['trackName']}"
            time.sleep(3)
            if isNewPlaylist:
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/div/form/input'))
                )
                search_input.clear()
                search_input.send_keys(song_name)
                
                search_button = driver.find_element(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/div/form/button')
                search_button.click()
                time.sleep(3)
                no_search_result = driver.find_elements(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/no-search-result/img')
                if no_search_result:
                    print(Fore.RED + f"Track not found: {song_name}")
                    isNoSearchResult = True
                else:
                    isNoSearchResult = False

                if not isNoSearchResult: 
                    header_music_or_not = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/search-result/section[1]/div[1]/h2'))
                    )
                    if header_music_or_not.text.strip() in ["Şarkılar", "Songs", "Пісні", "Песни"]:
                        print(Fore.GREEN + "Header music found")
                        isHeaderMusic = True
                    else:
                        print(Fore.RED + "Header music not found passing to the next track")
                        isHeaderMusic = False
                time.sleep(3)
                if isHeaderMusic and not isNoSearchResult:
                    new_playlist_before_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/search-result/section[1]/div[2]/fizy-slider/div/div[2]/div/div/div[1]/div/div/track-list/track-list-item-album[1]/div/div[5]/span[4]'))
                    )
                    new_playlist_before_button.click()
                    time.sleep(3)
                    first_album_dot = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/ul/li[1]'))
                    )
                    first_album_dot.click()
                    time.sleep(1)
                    new_playlist_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/ul/li[1]/ul/li[1]'))
                    )
                    new_playlist_button.click()
                    time.sleep(3)
    
                    new_playlist_name_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/input'))
                    )
                    new_playlist_name_input.send_keys(playlist_name)
    
                    new_playlist_create_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/button[2]'))
                    )
                    new_playlist_create_button.click()
                    time.sleep(3)
                    isNewPlaylist = False
    
                    print(Fore.BLUE + f"Created a new playlist: {song_name}")
            else:
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/div/form/input'))
                )

                search_input.clear()
                search_input.send_keys(song_name)

                time.sleep(2)
                search_button = driver.find_element(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/div/form/button')
                search_button.click()
                time.sleep(3)
                no_search_result = driver.find_elements(By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/no-search-result/img')
                if no_search_result:
                    print(Fore.RED + f"Track not found: {song_name}")
                    isNoSearchResult = True
                else:
                    isNoSearchResult = False

                if not isNoSearchResult: 
                    header_music_or_not = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/search-result/section[1]/div[1]/h2'))
                    )
                    if header_music_or_not.text.strip() in ["Şarkılar", "Songs", "Пісні", "Песни"]:
                        print(Fore.GREEN + "Header music found")
                        isHeaderMusic = True
                    else:
                        print(Fore.RED + "Header music not found passing to the next track")
                        isHeaderMusic = False
                time.sleep(3)
                if isHeaderMusic and not isNoSearchResult:
                    first_album = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/ui-view/main/div/div[2]/div/ui-view/search/div/search-result/section[1]/div[2]/fizy-slider/div/div[2]/div/div/div[1]/div/div/track-list/track-list-item-album[1]/div/div[5]/span[4]'))
                    )
                    first_album.click()
                    time.sleep(2)
                    first_album_dot = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/ul/li[1]'))
                    )
                    first_album_dot.click()
                    time.sleep(1)
                    first_album_list = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/ul/li[1]/ul/li[2]'))
                    )
                    first_album_list.click()
                    time.sleep(1)
            if isHeaderMusic and not isNoSearchResult:
                print(Fore.YELLOW + f"Added {track['artistName']} - {track['trackName']} to the playlist to {playlist['name']}")      
            time.sleep(2)

    driver.quit()

run()