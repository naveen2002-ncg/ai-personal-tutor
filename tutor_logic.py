import json
import random

def load_questions(path='data/questions.json'):
    with open(path, 'r') as f:
        return json.load(f)

def get_random_question(questions):
    return random.choice(questions)

def evaluate_answer(user_answer, correct_answer):
    return user_answer.strip().lower() == correct_answer.strip().lower()
