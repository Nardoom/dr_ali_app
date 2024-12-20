import openai

# Set your OpenAI API key (hardcoded for testing purposes)
openai.api_key = "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"

# Test the OpenAI API
try:
    # Correct API call for your setup
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ]
    )
    # Print the full response for debugging
    print("Full Response:", response)

    # Correctly access the AI response
    message = response.choices[0].message.content
    print("Extracted Message:", message)
except Exception as e:
    print("Error:", e)