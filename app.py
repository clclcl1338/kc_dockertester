import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
REALM_NAME = os.getenv("REALM_NAME")

def get_token():
    """Get access token from Keycloak."""
    try:
        response = requests.post(
            f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token",
            data={
                "client_id": CLIENT_ID,
                "username": USERNAME,
                "password": PASSWORD,
                "grant_type": "password",
                "client_secret": os.getenv("SECRET")
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting token: {e}")
        return None

@app.route("/auth", methods=["GET"])
def auth():
    """Authenticate with Keycloak and return a token."""
    token = get_token()
    if token:
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Authentication failed"}), 401

@app.route("/check", methods=["GET"])
def check():
    """Check if the provided token is valid."""
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        response = requests.get(
            f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/userinfo",
            headers={"Authorization": token},
        )
        response.raise_for_status()
        return jsonify({"message": "hello valid user"})
    except requests.exceptions.RequestException as e:
        print(f"Error checking token: {e}")
        return jsonify({"error": "unauthorize"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
