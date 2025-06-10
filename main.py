from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Tu token de bot y chat_id
BOT_TOKEN = os.getenv("BOT_TOKEN", "7633890350:AAF_OTp1j6zCJIQTmWHQnThzXlcnV5ElkvQ")
CHAT_ID = os.getenv("CHAT_ID", "8192921196")

# Endpoint de análisis de ChatGPT
GPT_ANALYSIS_ENDPOINT = "https://motor-ia.onrender.com/analizar"  # Este debe recibir la señal

@app.route('/forward-to-chatgpt', methods=['POST'])
def forward_to_chatgpt():
    data = request.json

    # 1. Enviar a Telegram
    try:
        message = f"""💹 Señal detectada:
📈 Símbolo: {data.get("symbol")}
📊 Acción: {data.get("action")}
🎯 Entrada: {data.get("entry")}
✅ TP: {data.get("tp")}
🛑 SL: {data.get("sl")}
📊 Confianza: {data.get("confidence")}%
"""
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print("❌ Error enviando a Telegram:", e)

    # 2. Reenviar a motor-ia para análisis de ChatGPT
    try:
        response = requests.post(GPT_ANALYSIS_ENDPOINT, json=data)
        print("✅ Reenvío al motor IA exitoso:", response.status_code)
    except Exception as e:
        print("❌ Error reenviando al motor IA:", e)

    return jsonify({"status": "ok", "data": data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

