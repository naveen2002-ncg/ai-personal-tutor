import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase app only once
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_config.json")
        firebase_admin.initialize_app(cred)

def create_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        return str(e)

def verify_user(email):
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except Exception as e:
        return None
