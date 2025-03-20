from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Créer un dossier "downloads" si ce n'est pas déjà fait
os.makedirs('downloads', exist_ok=True)

@app.route('/download', methods=['POST'])
def download_video():
    # Récupérer les données envoyées par le frontend
    video_url = request.json.get('video_url')
    video_format = request.json.get('format')  # Nouveau paramètre pour le format

    if not video_url:
        return jsonify({"message": "No video URL provided"}), 400

    # Ajouter les options de format et de progression
    progress = {"status": "downloading", "progress": 0}

    def progress_hook(d):
        if d['status'] == 'downloading':
            progress['progress'] = d['_percent_str']
        elif d['status'] == 'finished':
            progress['status'] = 'finished'

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': video_format if video_format else 'best',  # Utiliser le format choisi ou 'best' par défaut
        'progress_hooks': [progress_hook],  # Ajouter le hook de progression
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return jsonify({"message": "Video downloaded successfully", "progress": 100}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)