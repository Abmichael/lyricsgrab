from flask import Flask, jsonify
from grabber import Song
from sys import argv


app = Flask(__name__)

@app.route("/<query>")
def searcher(query):
	try:
		song = Song(query)

	except: song = None

	if song:
		result = {"song_title":song.full_title,"album_art":song.album_art,"lyrics_url":song.song_url,"Lyrics":song.lyrics}
		return jsonify(result)
	else:
		return "something went wrong, try again!!"

@app.route("/")
def home():
	return "up and running"
if __name__ == '__main__':
	app.debug=True
	app.run()