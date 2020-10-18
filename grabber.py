import re
import requests

from urllib.parse import urlencode
from bs4 import BeautifulSoup

APIKEY = "AIzaSyCClw6FEK-Wukrklg5psA2hOqR1pskdzWg"
ENGINEID = "015117108339957557193:wzr7fdpk6ii"
root_url = "https://www.googleapis.com/customsearch/v1/siterestrict?"

class Song:
    def __init__(self,query):
        """The Query used to find the song, best in [ARTIST + SONG_TITLE] form"""
        self.query = query
        if (y:=self._get_link()) is not None:
            self.song_url,self.album_art = y
            self.song = requests.get(self.song_url,timeout=30)
            self.lyrics,self.artist,self.title,self.album = self.get_metadata()
        else:
            return None

    def _get_link(self):
        params = {"q":self.query,"key":APIKEY,"cx":ENGINEID}
        path = requests.get(root_url+urlencode(params),timeout=10).json()
        try:
            link = path['items'][0]['link']
            album_art = path['items'][0]['pagemap']['cse_image'][0]['src']
        except:
            link = None
            album_art = None
        return link,album_art

    def get_metadata(self):
        html = BeautifulSoup(self.song.text,"html.parser")
        lyrics = html.find('div',class_='lyrics').get_text().strip("\n")
        chunk = html.find("div",{"class":"header_with_cover_art-primary_info"}).findChildren(recursive=False)
        artist,title = chunk[1].get_text().strip('\n'),chunk[0].get_text()
        album = chunk[4].get_text().strip("\n").split("\n")[1]
        # lyrics_new = html.find('div',class_='SongPageGrid-sc-1vi6xda-0 DGVcp Lyrics__Root-sc-1ynbvzw-0 jvlKWy').get_text().strip("\n")
        if lyrics:
            return (lyrics,artist,title,album)
        # elif lyrics_new:
        #     return (lyrics_new,artist,title,album)
        else:
            return None
            
    def __str__(self):
        return self.lyrics