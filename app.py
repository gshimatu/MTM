from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import tempfile
import subprocess
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(tempfile.gettempdir(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 Mo
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

FFMPEG_EXE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', 'ffmpeg.exe')

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
        # Supprime le fichier existant s'il y en a un pour éviter les conflits
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
            except PermissionError:
                # Si le fichier est en cours d'utilisation, on passe, Flask gérera l'écrasement
                pass

        file.save(video_path)
        file.stream.close() # Important pour libérer le fichier

        base_name = os.path.splitext(file.filename)[0]
        output_mp3_name = get_unique_filename(app.config['UPLOAD_FOLDER'], base_name, ".mp3")
        output_mp3_path = os.path.join(app.config['UPLOAD_FOLDER'], output_mp3_name)

        try:
            command = [
                FFMPEG_EXE_PATH, # Utilise le chemin relatif de ffmpeg.exe
                "-i", video_path,
                "-vn",
                "-acodec", "libmp3lame",
                "-q:a", "2",
                output_mp3_path
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)

            # Tente de supprimer le fichier vidéo temporaire après la conversion
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
            return f"Erreur lors de la conversion vidéo. Détails: {e.stderr}", 500

        except FileNotFoundError:
            # Cette erreur est spécifique si FFMPEG_EXE_PATH est incorrect ou ffmpeg.exe n'est pas trouvé
            return "Erreur serveur: FFmpeg n'a pas été trouvé. Veuillez vérifier l'installation de FFmpeg.", 500

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
    app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5000)
