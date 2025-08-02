import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment variables.")
genai.configure(api_key=api_key)

def analyze(subject ,email_content):
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are a highly intelligent data extraction agent. Your task is to analyze the following email and extract assignment details.
    The current date is {current_date_str}.

    Please extract the following information:
    1.  'title': A concise title for the assignment.
    2.  'due_date': The due date in strict YYYY-MM-DD format.
    3.  'description': A brief description of the assignment, suitable for a calendar event.
    4:   'message': a short message to be sent as a notification.

    If any information is missing, use a null value for that key. If no assignment is found at all, return a JSON object with null values for all keys.

    Respond ONLY with a valid JSON object. Do not include any other text or explanations.

    Here is the email content:
    ---
    Subject: {subject}
    Body: {email_content}
    ---
    """
    
    response = model.generate_content(prompt)
    # print(response.text)
    try:
        # Clean up the response to ensure it's valid JSON
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        # Parse the JSON string into a Python dictionary
        details = json.loads(cleaned_response)
        return details
    except (json.JSONDecodeError, AttributeError):
        # If Gemini fails to return valid JSON, return None
        print("Error: Could not parse a valid JSON response from the model.")
        return None