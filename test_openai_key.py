import openai

# Replace with your actual OpenAI API key
openai.api_key = "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"

try:
    # Test API call with the correct syntax for openai>=1.0.0
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )

    # Extract and print the assistant's response
    result = response.choices[0].message.content
    print("API Key is valid!")
    print("Response:", result)

except openai.OpenAIError as e:
    print("OpenAI API error:", e)
except Exception as e:
    print("Error:", e)