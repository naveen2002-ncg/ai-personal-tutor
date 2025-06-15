import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful tutor."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content
