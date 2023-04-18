"""
This is the base downloader class.
"""
import requests
from bs4 import BeautifulSoup
import webbrowser, time
import pyautogui

class GogoDownloader:
    def __init__(self, base_url, anime):
        self.base_url = base_url
        self.anime = anime
        self.anime_specific_url = self.base_url + f"category/{self.anime}"
        self.download_episode_link = self.anime_specific_url.replace('category/', '') + "-episode-"

    def get_page(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        return soup
    
    def get_total_eps_count(self, url):
        """gets the total episode count."""
        soup = self.get_page(url)
        pages = soup.find_all('div', attrs={'class':'anime_video_body'})
        eps_count = int(pages[0].find_all('li')[-1].text.strip().split('-')[-1])
        return eps_count
    
    def gui_magic(self):
        time.sleep(2)
        pyautogui.moveTo(1150, 451)
        pyautogui.click()
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.hotkey('command', 'w')

    def download_one_episode(self, eps_number):
        """download one single episode."""
        print(f"Downloading Episode: {eps_number}")
        download_url = self.download_episode_link + eps_number
        download_page = self.get_page(download_url)
        download_link = download_page.find_all('li', attrs={'class':'dowloads'})
        download_link = download_link[0].find_all('a', href=True)[0]['href']
        webbrowser.open(download_link)
        self.gui_magic()

    def download_all_episodes(self, total_eps):
        """downloads all episodes available to date (1 - n)."""
        print(f"Downloading all {total_eps} episodes.")
        for eps in range(1, total_eps+1):
            self.download_one_episode(str(eps))
            time.sleep(3)

    def download_specific_episodes(self, start, end):
        """download specific episodes given start episode number and end episode number."""
        print(f"Downloading episodes in range from {start} to {end}.")
        for eps in range(start, end+1):
            self.download_one_episode(str(eps))
            time.sleep(3)
            if eps % 10 == 0:
                # mimic human like behavior
                print(f"Waiting for 30 sec.")
                time.sleep(30)

    def caller(self, typ="all", start=None, end=None, eps_number=None):
        """main caller method."""
        print(f"Scrapping for {self.anime_specific_url}")
        total_episode_count = self.get_total_eps_count(self.anime_specific_url)
        print(f"Total Episodes for {self.anime} are {total_episode_count}")
        
        if typ == "all":
            self.download_all_episodes(total_episode_count)
        elif typ == "range":
            self.download_specific_episodes(start, end)
        else:
            self.download_one_episode(str(eps_number))

g = GogoDownloader("https://gogoanime.cl/", "one-piece-dub")
g.caller(typ="range", start=336, end=400)