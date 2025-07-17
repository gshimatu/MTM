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
        # Trouver le répertoire de base
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        # Chemin vers l'exécutable Flask (app.exe)
        flask_exe = os.path.join(base_dir, "app.exe")

        if not os.path.exists(flask_exe):
            messagebox.showerror("Erreur", f"Impossible de trouver {flask_exe}")
            return

        flask_process = subprocess.Popen(
            [flask_exe],
            cwd=base_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # Attendre que le serveur démarre
        time.sleep(3)
        webbrowser.open_new_tab(FLASK_URL)
        messagebox.showinfo("Application lancée", f"Le convertisseur MP4 vers MP3 est lancé dans votre navigateur à : {FLASK_URL}")

    except Exception as e:
        messagebox.showerror("Erreur de lancement", f"Impossible de démarrer l'application Flask: {e}")

def stop_flask_app():
    """Arrête le processus Flask si il est en cours d'exécution."""
    global flask_process
    if flask_process:
        flask_process.terminate()
        flask_process.wait(timeout=5)
        if flask_process.poll() is None:
            flask_process.kill()
        flask_process = None

def on_closing():
    """Gère la fermeture de la fenêtre GUI."""
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application et arrêter le serveur ?"):
        stop_flask_app()
        root.destroy()

# --- Centrage de la fenêtre ---
def center_window(win, width=400, height=200):
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# --- Interface graphique ---
root = tk.Tk()
root.title("Lanceur MP4 to MP3")
center_window(root, 400, 200)
root.resizable(False, False)
root.configure(bg="#03333c")

frame = tk.Frame(root, bg="#03333c")
frame.pack(expand=True)

label = tk.Label(frame, text="Convertisseur MP4 vers MP3", font=("Inter", 16, "bold"), fg="#3fd3ca", bg="#03333c")
label.pack(pady=10)

# Message d'accueil au-dessus du bouton, centré et sur plusieurs lignes
welcome_label = tk.Label(frame, text="Bienvenue dans l'application de conversion MP4 vers MP3 !", font=("Inter", 12), fg="#ffffff", bg="#03333c", wraplength=360, justify="center")
welcome_label.pack(pady=(0, 10))

launch_button = tk.Button(frame, text="Lancer l'application", command=start_flask_app,
                          font=("Inter", 12, "bold"), bg="#3fd3ca", fg="#03333c",
                          activebackground="#02262d", activeforeground="#3fd3ca",
                          padx=20, pady=10, relief="raised", bd=3)
launch_button.pack(pady=20)

# Frame pour le footer (auteur/version) en bas de la fenêtre
footer_frame = tk.Frame(root, bg="#03333c")
footer_frame.pack(side="bottom", fill="x")
footer_label = tk.Label(footer_frame, text="Par Gauthier Shimatu (le Shimatologue)  |  Version 1.1", font=("Inter", 10), fg="#3fd3ca", bg="#03333c")
footer_label.pack(pady=(0, 8))

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
