import openai
from openai import OpenAI
import os

def process_message_with_openai(message):
    # Ensure API key is properly loaded
    client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))

    # Define the conversation context and user message
    messages = [
        {"role": "system", "content": "Talk in first person as the person who sent the message. You should organize and extract the information. Make the informal text into a nice looking chunk of words. "},
        {"role": "user", "content": f"Please analyze the following message and provide structured responses for each of these queries:\n\nMessage: '{message.body}'\n\n1. Identify any skill being learned from the message and make sure to include the word learning.\n2. Provide a reflection on yesterday based on the message and make sure to include \"reflecting on yesterday\" \n3. Note any favorite food mentioned in the message and make sure to include \"My favorite food from yesterday was\" Additioanlly, say a random science fun fact and make it the 4th bullet point (but dont include any intro such as: \"Here's a fun science fact:\"). 4."}
    ]

    # Call to OpenAI's Chat API
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Confirm the correct model identifier
            messages=messages,
            max_tokens=350
        )

        # Assuming the response is formatted as expected
        text = response.choices[0].message.content
        lines = text.split('\n\n')
        processed_content = {}
    
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            text = response.choices[0].message.content
            lines = text.split('\n\n')
            processed_content = {}
        

            for line in lines:
                # Normalize space and remove any leading or trailing whitespace
                line = line.strip()
                # Determine the content category by presence of specific keywords
                if line.startswith('1.'):
                    # Extracts everything after the number and period which typically follows the format number.
                    processed_content['skills'] = line[3:].strip()
                elif line.startswith('2.'):
                    processed_content['reflections'] = line[3:].strip()
                elif line.startswith('3.'):
                    processed_content['food'] = line[3:].strip()
                elif line.startswith('4.'):
                    processed_content['science'] = line[3:].strip()
            return processed_content
        else:
            print("No valid response in choices")
            return {}


    except Exception as e:
        print(f"Error processing message with OpenAI: {e}")
        return {}