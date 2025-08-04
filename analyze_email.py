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
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
     You are an intelligent data extraction agent specializing in parsing communications from Google Classroom.

    ## CONTEXT
    - The current date is {current_date_str}. The user's timezone is Asia/Kolkata.
    - The email is from Google Classroom. It could be a new assignment, an announcement, a comment, or a grade notification. Your first job is to figure out which it is.

    ## PRIMARY TASK
    First, determine if the email describes a **new task, quiz, or material submission that requires action**. Do not treat comments on old posts, grade updates, or general announcements as new assignments.
    and if a task, submission, assignments, or quizzes does not have a due date, add a due day of 6 days from the current date.

    ## OUTPUT SCHEMA
    Based on your analysis, respond ONLY with a single, valid JSON object. The JSON must have the following keys:
    {{
      "is_assignment": boolean,
      "title": "string or null",
      "due_date": "string in YYYY-MM-DD format or null",
      "description": "string or null",
      "message": "string or null"
    }}

    ## FIELD INSTRUCTIONS
    - **is_assignment**: Set to `true` ONLY if the email describes a new task to be completed. Otherwise, set to `false`.
    - **title**: If `is_assignment` is true, extract the assignment's official title.
    - **due_date**: If a due date is present, extract it in strict YYYY-MM-DD format. If no due date is mentioned, use `null`.
    - **description**: A brief summary of the assignment's instructions, suitable for a calendar event description.
    - **message**: If `is_assignment` is true, create a very short (1-5 word) summary for a push notification, like "New AI Assignment".

    ## FINAL RULES
    - If `is_assignment` is `false`, all other keys in the JSON object must be `null`.
    - Analyze the entire email context (subject and body) carefully before making a decision.

    ## EMAIL FOR ANALYSIS
    ---
    Subject: {subject}
    Body: {email_content}
    ---
    """

    response = model.generate_content(prompt)
    print(response.text)
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