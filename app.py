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

STATIC_SUBTITLES_URL = '/static/subtitles'  # URL pentru accesarea subtitrărilor

def convert_srt_to_vtt(srt_file):
    vtt_file = srt_file.replace('.srt', '.vtt')
    with open(srt_file, 'r', encoding='utf-8') as srt, open(vtt_file, 'w', encoding='utf-8') as vtt:
        vtt.write("WEBVTT\n\n")
        for line in srt:
            if '-->' in line:
                vtt.write(line.replace(',', '.'))
            else:
                vtt.write(line)

    # După conversie, șterge fișierul .srt
    os.remove(srt_file)
    return vtt_file

@app.route('/get_subtitles')
def get_subtitles():
    movie_base = request.args.get('movie')
    if not movie_base:
        return jsonify([])

    subtitles = []

    for f in os.listdir(SUBTITLES_FOLDER):
        if f.startswith(movie_base):
            file_path = os.path.join(SUBTITLES_FOLDER, f)
            if f.endswith('.vtt'):
                subtitles.append(os.path.join(STATIC_SUBTITLES_URL, f))
            elif f.endswith('.srt'):
                vtt_file = convert_srt_to_vtt(file_path)
                subtitles.append(os.path.join(STATIC_SUBTITLES_URL, os.path.basename(vtt_file)))

    return jsonify(subtitles)

# Servește fișierele de subtitrare din directorul "subtitles"
@app.route(STATIC_SUBTITLES_URL + '/<path:filename>')
def serve_subtitle(filename):
    return send_from_directory(SUBTITLES_FOLDER, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
