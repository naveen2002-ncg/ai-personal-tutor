import random

def generate_question(subject):
    question_bank = {
        "Math": [("What is 5 + 3?", "8"), ("What is 12 / 4?", "3")],
        "Science": [("What planet is known as the Red Planet?", "Mars"), ("What gas do plants absorb?", "Carbon dioxide")],
        "Python Basics": [("What is a list in Python?", "A collection of items enclosed in square brackets"), ("What is the keyword for function in Python?", "def")]
    }

    question, answer = random.choice(question_bank.get(subject, [("No question available", "N/A")]))
    return question, answer
