import firebase_admin
from firebase_admin import firestore

db = firestore.client()

def log_interaction(user_id, question, answer, score):
    doc_ref = db.collection("users").document(user_id).collection("history").document()
    doc_ref.set({
        "question": question,
        "answer": answer,
        "score": score
    })

def get_history(user_id):
    docs = db.collection("users").document(user_id).collection("history").stream()
    return [{"question": d.get("question"), "answer": d.get("answer"), "score": d.get("score")} for d in docs]
