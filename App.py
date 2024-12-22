from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")  # Serve the index.html file

@app.route('/api/get-advice', methods=['POST'])
def get_advice():
    try:
        # Handle both JSON and form data submissions
        if request.content_type == 'application/json':
            data = request.json
            symptoms = data.get("symptoms")
            language = data.get("language", "auto")  # Default to "auto"
        elif request.content_type == 'application/x-www-form-urlencoded':
            symptoms = request.form.get("symptoms")
            language = request.form.get("language", "auto")  # Default to "auto"
        else:
            return jsonify({"error": "Unsupported Media Type"}), 415

        # Validation: Ensure 'symptoms' are provided
        if not symptoms or not symptoms.strip():
            return jsonify({"error": "The 'symptoms' field is required."}), 400

        # Log inputs for debugging
        print(f"Received symptoms: {symptoms}")
        print(f"Requested language: {language}")

        # Prepare the language-specific instruction
        if language == "auto":
            language_instruction = "Detect the language automatically and respond accordingly."
        else:
            language_instruction = f"Respond in {language}, regardless of the input language."

        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a knowledgeable, helpful, and polite Dr. Ali. You provide medical advice, lifestyle suggestions, what foods to consume and avoid, OTC medications, and respond in the language requested: {language_instruction}."},
                {"role": "user", "content": symptoms}
            ]
        )

        # Extract the AI response
        result = response.choices[0].message.content
        print(f"AI Response: {result}")

        # If form submission, display the response on a new page
        if request.content_type == 'application/x-www-form-urlencoded':
            return f"""
            <h1>Dr. Ali's Response</h1>
            <p>{result}</p>
            <a href="/">Back to Home</a>
            """

        # If JSON submission, return the response as JSON
        return jsonify({"response": result})

    except openai.OpenAIError as e:
        print("OpenAI API Error:", e)
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        print("Server Error:", e)
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)