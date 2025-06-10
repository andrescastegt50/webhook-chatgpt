from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Reemplaza con tu token real y chat ID
TELEGRAM_TOKEN = "7633890350:AAF_OTp1j6zCJIQTmWHQnThzXlcnV5ElkvQ"
CHAT_ID = "8192921196"

def enviar_a_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=data)
        print("📤 Intentando enviar a Telegram...")
        print("➡️ Payload:", data)
        print("↩️ Response:", response.status_code, response.text)
        if response.status_code == 200:
            print("✅ Mensaje enviado con éxito a Telegram.")
        else:
            print("❌ Error al enviar mensaje:", response.status_code, response.text)
    except Exception as e:
        print("❌ Excepción al enviar a Telegram:", e)

@app.route("/forward-to-chatgpt", methods=["POST"])
def recibir_datos():
    try:
        contenido = request.get_json()
        print("📩 Datos recibidos:", contenido)

        if not contenido:
            return jsonify({"status": "error", "message": "JSON vacío"}), 400

        # Si se envía una lista de señales, itéralas
        if isinstance(contenido, list):
            for señal in contenido:
                mensaje = formatear_mensaje(señal)
                enviar_a_telegram(mensaje)
        else:
            mensaje = formatear_mensaje(contenido)
            enviar_a_telegram(mensaje)

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("❌ Error general:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

def formatear_mensaje(señal):
    try:
        symbol = señal.get("symbol", "UNKNOWN")
        action = señal.get("action", "NO_ACTION")
        entry = señal.get("entry", "-")
        tp = señal.get("tp", "-")
        sl = señal.get("sl", "-")
        confidence = señal.get("confidence", "-")
        return f"📈 *{symbol}* | *{action}*\n🎯 Entry: {entry}\n📊 TP: {tp} | 🛑 SL: {sl}\n🧠 Confianza: {confidence}%"
    except Exception as e:
        print("❌ Error formateando el mensaje:", e)
        return "⚠️ Error al formatear señal recibida."

@app.route("/")
def inicio():
    return "✅ Webhook ChatGPT activo"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
