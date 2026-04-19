from flask import Flask, request, jsonify

app = Flask(__name__)

# A simple dictionary to simulate a database
# In production, use a real DB or a JSON file
VALID_LICENSES = {
    "USER_KEY_123": "MACHINE_ID_XYZ",
}

@app.route('/verify', methods=['POST'])
def verify_license():
    data = request.json
    key = data.get("key")
    hwid = data.get("hwid")

    if key in VALID_LICENSES:
        if VALID_LICENSES[key] == hwid:
            return jsonify({"status": "authorized"}), 200
        else:
            return jsonify({"status": "wrong_hardware"}), 403
    
    return jsonify({"status": "invalid_key"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
