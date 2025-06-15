def give_feedback(user_input, correct_answer):
    if user_input.strip().lower() == correct_answer.strip().lower():
        return "✅ Correct! Well done!"
    else:
        return f"❌ That's not quite right. Correct answer: {correct_answer}"
