from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/api/get-advice', methods=['POST'])
def get_advice():
    try:
        # Get user input from the form
        symptoms = request.form.get("symptoms")  # Handle form data submission

        # Validation: Ensure 'symptoms' are provided
        if not symptoms or not symptoms.strip():
            return jsonify({"error": "The 'symptoms' field is required and cannot be empty."}), 400

        # Log input for debugging
        print(f"Received symptoms: {symptoms}")

        # Correct OpenAI API call for openai>=1.0.0
        response = openai.Chat.Completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a highly knowledgeable and polite doctor named Dr. Ali that diagnoses symptoms, gives advice on treatment, lifestyle changes, what food and nutrients to avoid and what food and nutrients to consume, and OTC medications."},
                {"role": "user", "content": symptoms}
            ]
        )

        # Extract the AI response
        result = response.choices[0].message.content
        print(f"AI Response: {result}")

        return jsonify({"response": result})

    except openai.OpenAIError as e:
        print("OpenAI API Error:", e)
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        print("Server Error:", e)
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)