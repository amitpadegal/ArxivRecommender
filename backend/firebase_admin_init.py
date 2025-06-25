import firebase_admin
from firebase_admin import credentials, auth
import os

# Load credentials from JSON key file
cred = credentials.Certificate("service_key.json")
firebase_admin.initialize_app(cred)

def verify_token_and_get_uid(id_token: str):
    decoded = auth.verify_id_token(id_token)
    return decoded["uid"]
