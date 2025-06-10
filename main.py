from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/forward-to-chatgpt', methods=['POST'])
def forward():
    try:
        data = request.json
        print("Datos recibidos:", data)  # Esto es solo para testeo
        return jsonify({"status": "ok", "message": "Datos recibidos correctamente por webhook"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()