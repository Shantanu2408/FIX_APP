import os
from flask import Flask, request, jsonify
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# Azure OpenAI API configuration
endpoint = "https://shant-mjjz4han-eastus2.cognitiveservices.azure.com/openai/v1"
deployment_name = "gpt-4o-standard"  # Make sure this is correct for your setup
api_key = os.environ.get('API_KEY') # Replace with your actual API key

# OpenAI client
client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

# Home route
@app.route('/')
def home():
    return "Welcome to the Flask OpenAI Chat Service!"

# Chat route (fixed to handle response properly)
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get user input from the request
        user_input = request.json.get('message')

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Create the chat completion request
        completion = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )

        # Access the 'choices' field correctly (dot notation)
        if completion.choices:
            # Use dot notation to access the content
            response_content = completion.choices[0].message.content
            return jsonify({"response": response_content})
        else:
            return jsonify({"error": "No valid response from the model."}), 500

    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
