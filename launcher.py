import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import webbrowser
import os
import sys
import time

# Définir le port de l'application Flask
FLASK_PORT = 5000
FLASK_URL = f"http://127.0.0.1:{FLASK_PORT}"

flask_process = None # Variable globale pour stocker le processus Flask

def start_flask_app():
    """Démarre l'application Flask dans un processus séparé."""
    global flask_process
    try:
        # Définir le chemin vers l'interpréteur Python qui va exécuter Flask
        # Dans un bundle PyInstaller, c'est l'exécutable lui-même.
        python_executable = sys.executable
        
        # Trouver le répertoire de base de l'application (où se trouvent app.py, static, templates)
        # Lorsque PyInstaller crée un bundle (--onefile), sys._MEIPASS est le chemin du répertoire temporaire
        # où les fichiers sont extraits.
        if getattr(sys, 'frozen', False): # Si l'application est "gelée" par PyInstaller
            base_dir = sys._MEIPASS
        else:
            # Si l'application n'est pas gelée (en mode développement)
            base_dir = os.path.dirname(os.path.abspath(__file__))
 
        flask_app_module_name = 'app.py' 

        # Définir la variable d'environnement FLASK_APP
        # Flask a besoin de savoir quel fichier est l'application.
        flask_env = os.environ.copy()
        flask_env['FLASK_APP'] = flask_app_module_name # Utilise juste le nom du module

        # Lancer Flask en tant que module
        # Nous utilisons 'flask run' car c'est la manière standard de lancer une application Flask
        flask_process = subprocess.Popen(
            [python_executable, "app.py"],
            cwd=base_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Donner un peu de temps au serveur pour démarrer
        time.sleep(3) 

        webbrowser.open_new_tab(FLASK_URL)
        messagebox.showinfo("Application lancée", f"Le convertisseur MP4 vers MP3 est lancé dans votre navigateur à : {FLASK_URL}")

    except Exception as e:
        messagebox.showerror("Erreur de lancement", f"Impossible de démarrer l'application Flask: {e}")

def stop_flask_app():
    """Arrête le processus Flask si il est en cours d'exécution."""
    global flask_process
    if flask_process:
        messagebox.showinfo("Arrêt de l'application", "Arrêt du serveur Flask...")
        flask_process.terminate() # Tente d'arrêter le processus
        flask_process.wait(timeout=5) # Attend la fin du processus (max 5 secondes)
        if flask_process.poll() is None: # Si le processus n'est pas terminé
            flask_process.kill() # Force l'arrêt
        flask_process = None
        
def on_closing():
    """Gère la fermeture de la fenêtre GUI."""
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application et arrêter le serveur ?"):
        stop_flask_app()
        root.destroy() # Ferme la fenêtre Tkinter

# Configuration de l'interface graphique Tkinter
root = tk.Tk()
root.title("Lanceur MP4 to MP3")
root.geometry("400x200")
root.resizable(False, False) # Empêche le redimensionnement


# Style
root.configure(bg="#03333c") # primary-color

frame = tk.Frame(root, bg="#03333c")
frame.pack(expand=True)

label = tk.Label(frame, text="Convertisseur MP4 vers MP3", font=("Inter", 16, "bold"), fg="#3fd3ca", bg="#03333c") # secondary-color
label.pack(pady=10)

launch_button = tk.Button(frame, text="Lancer l'application", command=start_flask_app,
                          font=("Inter", 12, "bold"), bg="#3fd3ca", fg="#03333c", # secondary-color
                          activebackground="#02262d", activeforeground="#3fd3ca",
                          padx=20, pady=10, relief="raised", bd=3)
launch_button.pack(pady=20)

# Gérer la fermeture de la fenêtre
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
