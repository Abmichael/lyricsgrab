import re
import requests

from urllib.parse import urlencode
from bs4 import BeautifulSoup


class Song:
    def __init__(self,query):
        """The Query used to find the song, best in [ARTIST + SONG_TITLE] form"""
        self.query = query
        if (y:=self._get_path()) is not None:
            self.full_title,self.album_art,x = y
            self.song_url = "https://genius.com"+x
            self.song = requests.get(self.song_url,timeout=30)
            self.lyrics=self.find_lyrics()
        else:
            return None

    def _get_path(self):
        params = {"q":self.query,"per_page":1}
        path = requests.get("https://genius.com/api/search/multi?"+urlencode(params),timeout=10).json()
        try:
            path=(path['response']['sections'][0]['hits'][0]['result']['full_title'],
            path['response']['sections'][0]['hits'][0]['result']['header_image_url'],
            path['response']['sections'][0]['hits'][0]['result']['path'])
        except:
            pass
        return path

    def find_lyrics(self):
        html = BeautifulSoup(self.song.text,"html.parser")
        lyrics = html.find('div',class_='lyrics')
        lyrics_new = html.find('div',class_='SongPageGrid-sc-1vi6xda-0 DGVcp Lyrics__Root-sc-1ynbvzw-0 jvlKWy')
        if lyrics:
            return lyrics.get_text().strip("\n")
        elif lyrics_new:
            return lyrics_new.get_text().strip("\n")
        else:
            return None
    def __str__(self):
        return self.lyrics
