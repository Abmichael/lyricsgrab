from flask import Flask, jsonify
from grabber import Song
from sys import argv



app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/<query>")
def searcher(query):
	try:
		song = Song(query)
	except: 
		song = None

	if song:
		result = {'song_title':song.title,'artist':song.artist,'album':song.album,'album_art':song.album_art,'lyrics_url':song.song_url,'lyrics':song.lyrics}
		return jsonify(result)
	else:
		return "something went wrong, try again!!"

@app.route("/")
def home():
	return "up and running"

if __name__ == '__main__':
	app.debug=True
	app.run()