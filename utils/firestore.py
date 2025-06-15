import firebase_admin
from firebase_admin import firestore

def get_firestore_client():
    if not firebase_admin._apps:
        raise Exception("Firebase not initialized. Call initialize_firebase() first.")
    return firestore.client()

def save_user_response(email, question, answer, score, feedback):
    db = get_firestore_client()
    db.collection("user_data").add({
        "email": email,
        "question": question,
        "answer": answer,
        "score": score,
        "feedback": feedback
    })
