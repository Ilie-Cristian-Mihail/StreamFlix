from flask import Flask, render_template, send_from_directory, jsonify, request
import os

app = Flask(__name__)
MOVIES_FOLDER = os.path.join(app.static_folder, 'movies')
SUBTITLES_FOLDER = os.path.join(MOVIES_FOLDER, 'subtitles')

@app.route('/')
def index():
    movies = [f for f in os.listdir(MOVIES_FOLDER) if f.endswith(('.mp4', '.mkv'))]
    return render_template('index.html', movies=movies)

@app.route('/movies/<path:filename>')
def movie(filename):
    return send_from_directory(MOVIES_FOLDER, filename)

@app.route('/subtitles/<path:filename>')
def subtitle(filename):
    return send_from_directory(SUBTITLES_FOLDER, filename)

@app.route('/get_subtitles')
def get_subtitles():
    movie_base = request.args.get('movie')
    if not movie_base:
        return jsonify([])

    subtitles = [
        os.path.join('subtitles', f) for f in os.listdir(SUBTITLES_FOLDER)
        if f.startswith(movie_base) and f.endswith('.vtt')
    ]
    
    return jsonify(subtitles)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
