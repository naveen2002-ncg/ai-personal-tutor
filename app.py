import streamlit as st
import os
import re
from utils.auth import initialize_firebase
from utils.firestore import save_user_response
import firebase_admin
from firebase_admin import auth
from groq import Groq  # ✅ Updated to use Groq SDK

# 🔐 Initialize Firebase
initialize_firebase()

# 🎯 Setup Groq client
client = Groq(api_key="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")  # Replace with your real key

# 🎓 App Title
st.set_page_config(page_title="AI Tutor", layout="wide")
st.title("📚 AI-Powered Personal Tutor")

# 🔐 Session State for Auth
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# 🔐 Authentication (Email/Password)
def login_ui():
    st.subheader("🔐 Login / Signup")
    choice = st.radio("Choose", ["Login", "Signup"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        try:
            if choice == "Signup":
                user = auth.create_user(email=email, password=password)
                st.success("Signup successful. You can now log in.")
            else:
                # Firebase Admin SDK can't verify password directly
                st.warning("Admin SDK can't validate passwords. For real auth, use Firebase client SDK.")
                st.session_state.user_email = email
                st.success(f"Logged in as {email}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# 🧠 Ask Groq & Evaluate
def get_gpt_feedback(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful tutor. Ask a question to test the student's knowledge, evaluate their answer, give feedback, and assign a score between 0-10."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq Error: {e}"

# 🎓 Tutor UI with Language + Next Question
def tutor_interface():
    st.subheader("🤖 AI Tutor Interaction")

    # 🌐 Language selection
    language = st.selectbox("Choose language", ["English", "Hindi", "Kannada", "Telugu"])
    topic = st.text_input("Enter topic (e.g., Python loops, OOP, etc.)")

    if st.button("🧠 Generate Question"):
        prompt = f"Ask a question about {topic} in {language}."
        question = get_gpt_feedback(prompt)
        st.session_state['current_question'] = question
        st.session_state['current_topic'] = topic
        st.session_state['current_language'] = language

    if 'current_question' in st.session_state:
        st.markdown(f"**Question:** {st.session_state['current_question']}")
        answer = st.text_area("Your Answer")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("📩 Submit Answer"):
                prompt = (
                    f"You are a tutor evaluating a student's answer in {st.session_state['current_language']}.\n\n"
                    f"Question: {st.session_state['current_question']}\n"
                    f"Student's Answer: {answer}\n"
                    f"Please evaluate the answer, provide feedback, and assign a score between 0 and 10."
                )
                evaluation = get_gpt_feedback(prompt)
                st.success("✅ Feedback Generated")
                st.markdown(f"**Feedback:**\n{evaluation}")

                # 🧮 Extract score
                score_match = re.search(r"[Ss]core:\s*(\d{1,2})/10", evaluation)
                if score_match:
                    score = int(score_match.group(1))
                else:   
                    score = 0

                save_user_response(
                    st.session_state.user_email,
                    st.session_state['current_question'],
                    answer,
                    score,
                    evaluation
                )
                st.info(f"Score saved: {score}/10")

        with col2:
            if st.button("🔁 Next Question"):
               prompt = f"Ask another question about {st.session_state['current_topic']} in {st.session_state['current_language']}."
               next_q = get_gpt_feedback(prompt)
               st.session_state['current_question'] = next_q
               st.rerun()  # ✅ updated for Streamlit v1.31+

# 🌐 App Logic
if st.session_state.user_email:
    st.success(f"Welcome, {st.session_state.user_email}!")
    tutor_interface()
else:
    login_ui()
