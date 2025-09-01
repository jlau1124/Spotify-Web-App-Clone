# Spotify Web App Clone

A web-based Spotify clone built with **Flask** and **Tailwind CSS**.  
This project demonstrates a basic music player interface with playlists, albums, and song playback functionality.

## Features

- Browse and view albums and songs
- Create and manage playlists
- Play, pause, skip, and loop songs
- Dynamic UI updates using JavaScript and Flask
- Responsive design with Tailwind CSS

## Tech Stack

- **Backend:** Flask
- **Frontend:** HTML, CSS (Tailwind), JavaScript
- **Data:** In-memory storage (for playlists and songs)
- **Environment Management:** Python virtual environment, dotenv for configuration

## Installation

1. Clone this repository:

```bash
git clone https://github.com/jlau1124/Spotify-Web-App-Clone.git
cd Spotify-Web-App-Clone

2. Create and activate a virtual environment:
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure environment variables by creating a .env file:
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret

5. Usage
Run the Flask app:

python spotify.py

older Structure
spotify-clone-clean/
│
├── static/             # CSS, JS, and assets
├── templates/          # HTML templates
├── spotify.py          # Main Flask app
├── requirements.txt    # Python dependencies
├── tailwind.config.js  # Tailwind CSS configuration
└── .gitignore          # Ignored files and folders
