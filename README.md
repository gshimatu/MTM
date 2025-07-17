# 🎵 Convertisseur MP4 vers MP3

## Introduction

Ce projet est une application de bureau Windows permettant de convertir des fichiers vidéo MP4 en fichiers audio MP3, directement depuis votre navigateur. L’objectif est de rendre la conversion accessible à tous, sans installation complexe, sans dépendance à Python ou Flask, et sans publicité.

---

## Mise en contexte

De nombreux utilisateurs souhaitent extraire la piste audio de vidéos (cours, podcasts, conférences, musiques, etc.) pour les écouter sur leur téléphone ou lecteur MP3. Les solutions en ligne sont souvent limitées, peu sécurisées ou truffées de publicités. Ce projet propose une alternative locale, rapide et respectueuse de la vie privée.

---

## Problématique

- Extraire facilement l’audio d’une vidéo MP4 sans connaissances techniques.
- Éviter les outils en ligne peu fiables ou limités.
- Offrir une interface moderne, simple et agréable à utiliser.
- Permettre une utilisation **sans rien installer** (application portable).

---

## Technologies utilisées

- **Python 3** (pour le développement, mais pas nécessaire côté utilisateur)
- **Flask** (serveur web intégré dans l’exécutable)
- **FFmpeg** (conversion audio/vidéo, inclus dans le package)
- **Tkinter** (lanceur graphique Windows)
- **HTML5 / CSS3 / JavaScript** (frontend moderne)
- **PyInstaller** (création des exécutables Windows)
- **FontAwesome** (icônes)

---

## Fonctionnalités

- Application Windows **autonome** : fonctionne sur n’importe quel PC Windows, sans installer Python, Flask ou autre.
- Lancement automatique du serveur Flask via le lanceur graphique (`Mtm.exe`).
- Fenêtre du lanceur centrée à l’écran.
- Upload de fichiers MP4 via glisser-déposer ou sélection classique.
- Conversion rapide en MP3 grâce à FFmpeg.
- Téléchargement automatique du fichier MP3 converti.
- Gestion intelligente des doublons : si un fichier existe déjà, le nouveau sera nommé `nom (1).mp3`, `nom (2).mp3`, etc.
- Animation de chargement pendant la conversion.
- Interface responsive et agréable.
- Arrêt automatique du serveur Flask à la fermeture de l’application.

---

## Structure du projet

```
mp4ToMp3/
│
├── app.py                # Application Flask principale
├── launcher.py           # Lanceur graphique Windows (Tkinter)
├── requirements.txt      # Dépendances Python (pour développement)
├── bin/
│   └── ffmpeg.exe        # Binaire FFmpeg Windows
├── static/
│   ├── css/
│   │   └── style.css     # Feuilles de style 
│   ├── js/
│   │   └── script.js     
│   └── images/
│       └── logo.png      # Logo de l’application
├── templates/
│   └── index.html        # Page principale Flask
├── final/
│   ├── Mtm.exe           # Lanceur graphique autonome
│   └── app.exe           # Serveur Flask autonome
└── README.md             # Ce fichier
```

---

## Fonctionnement

### 1. **Lancement**

- Double-cliquez sur `Mtm.exe` (dans le dossier `final`).
- La fenêtre du lanceur s’ouvre, centrée à l’écran.
- Cliquez sur "Lancer l'application".
- L’application s’ouvre automatiquement dans votre navigateur par défaut.

### 2. **Conversion**

- Glissez-déposez ou sélectionnez un fichier MP4.
- Cliquez sur **Convertir en MP3**.
- Patientez pendant la conversion (animation visible).
- Le téléchargement du MP3 démarre automatiquement.
- Si vous convertissez plusieurs fois le même fichier, le nom sera incrémenté (`nom (1).mp3`, etc.).

### 3. **Fermeture**

- Fermez la fenêtre du lanceur pour arrêter automatiquement le serveur Flask.

---

## Distribution

Pour utiliser l’application sur un autre PC :
- Copiez simplement le contenu du dossier `final` (au minimum : `Mtm.exe` et `app.exe`).
- **Aucune installation de Python, Flask ou autre n’est nécessaire.**
- L’application fonctionne sur n’importe quel PC Windows récent.

---

## Démo

### Interface principale

![Interface principale](static/images/demo/demo1.PNG)

### Conversion

![Animation de conversion](static/images/demo/demo2.PNG)

---

## Fonctionnalités futures possibles

- Conversion de plusieurs fichiers en lot.
- Support d’autres formats vidéo (avi, mov, mkv…).
- Choix du format de sortie (wav, ogg…).
- Extraction d’un extrait audio (début/fin).
- Interface multilingue.
- Version portable multiplateforme (Linux/Mac).

---

## Contribution

Les contributions sont les bienvenues !  
N’hésitez pas à ouvrir une issue ou une pull request pour proposer des améliorations, corriger des bugs ou ajouter des fonctionnalités.

---

## Auteur

Projet réalisé par **@Gauthier Shimatu** (le Shimatologue)  
Merci d’utiliser ce convertisseur et bon courage pour vos projets !

---