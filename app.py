from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import tempfile
import subprocess
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(tempfile.gettempdir(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 Mo
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Définissez le chemin complet vers ffmpeg.exe
# REMPLACEZ CE CHEMIN par le chemin réel où vous avez ffmpeg.exe sur votre système
# Exemple: FFMPEG_EXE_PATH = "C:\\ffmpeg\\ffmpeg.exe"
# Assurez-vous que les doubles barres obliques inverses sont utilisées pour les chemins Windows
# Si vous êtes ABSOLUMENT SÛR que 'ffmpeg' est dans le PATH de l'environnement où Flask est exécuté,
# vous pouvez laisser FFMPEG_EXE_PATH = "ffmpeg"
FFMPEG_EXE_PATH = "C:\\ffmpeg\\bin\\ffmpeg.exe" # <-- Correction ici : doubles barres obliques inverses

def get_unique_filename(folder, base_name, ext):
    i = 1
    candidate = f"{base_name}{ext}"
    while os.path.exists(os.path.join(folder, candidate)):
        candidate = f"{base_name} ({i}){ext}"
        i += 1
    return candidate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'video_file' not in request.files:
        return "Aucun fichier n'a été soumis.", 400

    file = request.files['video_file']
    if file.filename == '':
        return "Nom de fichier vide.", 400

    if file:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
            except PermissionError:
                pass

        file.save(video_path)
        file.stream.close()

        base_name = os.path.splitext(file.filename)[0]
        output_mp3_name = get_unique_filename(app.config['UPLOAD_FOLDER'], base_name, ".mp3")
        output_mp3_path = os.path.join(app.config['UPLOAD_FOLDER'], output_mp3_name)

        try:
            command = [
                FFMPEG_EXE_PATH,
                "-i", video_path,
                "-vn",
                "-acodec", "libmp3lame",
                "-q:a", "2",
                output_mp3_path
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)

            for _ in range(20):
                try:
                    os.remove(video_path)
                    break
                except PermissionError:
                    time.sleep(0.1)

            return redirect(url_for('download_file', filename=output_mp3_name))

        except subprocess.CalledProcessError as e:
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(output_mp3_path):
                os.remove(output_mp3_path)
            return "Erreur lors de la conversion vidéo.", 500

        except FileNotFoundError:
            return "Erreur serveur: FFmpeg n'a pas été trouvé.", 500

        except Exception:
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(output_mp3_path):
                os.remove(output_mp3_path)
            return "Une erreur inattendue est survenue lors de la conversion.", 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
