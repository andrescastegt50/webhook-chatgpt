from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/forward-to-chatgpt', methods=['POST'])
def forward():
    try:
        data = request.json
        print("Datos recibidos:", data)  # Solo para verificación
        return jsonify({"status": "ok", "message": "Datos recibidos correctamente por webhook"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
