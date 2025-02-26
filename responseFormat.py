import json
import openai
from openai import OpenAI
import os

def process_message_with_openai(message):
    # Ensure API key is properly loaded
    client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))

    # Instruct the model to output a JSON object with exactly these keys.
    messages = [
        {
            "role": "system",
            "content": (
                "You are a highly intelligent and creative assistant. Analyze the provided message and extract key insights. "
                "Output a JSON object with exactly four keys: 'skills', 'reflections', 'food', and 'science'. "
                "For 'skills', extract any mention of a skill or something being learned (ensure the word 'learning' appears). "
                "For 'reflections', summarize any thoughtful reflection on yesterday's events. "
                "For 'food', extract any mention of a favorite food. "
                "For 'science', ignore the message and generate a random, interesting, and fun science fact. "
                "Do not include any extra text—only output the JSON object."
            )
        },
        {
            "role": "user",
            "content": (
                f"Analyze the following message and provide the information in JSON format as specified. "
                f"Message: '{message}'"
            )
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=350
        )

        raw_output = response.choices[0].message.content.strip()
        print(f"OpenAI raw response: {raw_output}")

        # Remove any markdown code block markers if present
        if raw_output.startswith("```") and raw_output.endswith("```"):
            raw_output = raw_output.strip("```").strip()

        # Attempt to parse the output as JSON
        processed_content = json.loads(raw_output)
        return processed_content

    except Exception as e:
        print(f"Error processing message with OpenAI: {e}")
        return {}