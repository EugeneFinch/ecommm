import os
import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if user_message:
        try:
            # Call OpenAI API to generate a response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            ai_response = response.choices[0].message.content.strip()
            return jsonify({"ai_response": ai_response})

        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return jsonify({"error": "Failed to get response from AI"}), 500
    else:
        return jsonify({"error": "No message sent"}), 400

if __name__ == '__main__':
    app.run(debug=True)
