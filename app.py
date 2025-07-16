from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import tempfile
import subprocess 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(tempfile.gettempdir(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'video_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['video_file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Sauvegarde temporaire du fichier vidéo uploadé
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(video_path)
        
        # Nom du fichier MP3 de sortie
        output_mp3_name = os.path.splitext(file.filename)[0] + ".mp3"
        output_mp3_path = os.path.join(app.config['UPLOAD_FOLDER'], output_mp3_name)

        try:
            # --- Logique de conversion MP4 vers MP3 (Utilisation de FFmpeg via subprocess) ---
            # IMPORTANT: Assurez-vous que 'ffmpeg' est dans le PATH de l'environnement où Flask est exécuté.
            # Sinon, remplacez "ffmpeg" par le chemin complet de votre ffmpeg.exe
            command = [
                "ffmpeg",
                "-i", video_path,
                "-vn", # Ne pas inclure de vidéo
                "-acodec", "libmp3lame", # Codec audio pour MP3
                "-q:a", "2", # Qualité audio (2 est une bonne qualité)
                output_mp3_path
            ]
            
            # Exécution de la commande FFmpeg
            subprocess.run(command, check=True, capture_output=True, text=True)
            
            # --- Nettoyage des fichiers temporaires ---
            os.remove(video_path) # Supprime la vidéo uploadée
            
            # Redirection vers une route de téléchargement ou affichage direct
            return redirect(url_for('download_file', filename=output_mp3_name))

        except subprocess.CalledProcessError as e:
            # Gérer les erreurs de FFmpeg
            print(f"FFmpeg Error: {e.stderr}")
            os.remove(video_path)
            if os.path.exists(output_mp3_path):
                os.remove(output_mp3_path)
            return "Erreur lors de la conversion vidéo. Veuillez réessayer."
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            os.remove(video_path)
            if os.path.exists(output_mp3_path):
                os.remove(output_mp3_path)
            return "Une erreur inattendue est survenue."

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)