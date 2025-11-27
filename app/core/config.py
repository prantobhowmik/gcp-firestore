import firebase_admin
from firebase_admin import credentials


def init_firestore():
    """Initialize Firebase app once."""
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            "storageBucket": "learn-gcp-567d4.firebasestorage.app"
        })
