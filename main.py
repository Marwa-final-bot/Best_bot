
import requests
from flask import Flask, request
import os

app = Flask(__name__)

BOT_TOKEN = '7323523378:AAFX3USqaXZXN8xcpsdgzu02cN9HG1wNCZk'
CHAT_ID = '7975116093'
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://best-bot-essj.onrender.com/webhook')

def send_prediction_to_telegram(prediction):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': prediction
    }
    response = requests.post(url, data=payload)
    return response.ok

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if data and 'message' in data and 'text' in data['message']:
        text = data['message']['text']
        chat_id = data['message']['chat']['id']
        if text == '/predict':
            prediction = 'Next Aviator prediction: x2.10 (sample)'
            send_prediction_to_telegram(prediction)
        elif text == '/start':
            welcome = '✅ Welcome to Aviator Predictor Bot! Send /predict to get started.'
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                          data={'chat_id': chat_id, 'text': welcome})
    return 'OK'

@app.before_first_request
def set_webhook():
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
