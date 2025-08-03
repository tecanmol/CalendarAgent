import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from analyze_email import analyze
from addTocalendar import create_calendar_event
from notify import sendNotification
import time

# Define the permissions your script needs.
# If you change these, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/calendar"]

topic = "cal-ai-agent-alerts-u4xqz"

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    # It's created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Build the Gmail API service
        gmail_service = build("gmail", "v1", credentials=creds)
        calendar_service = build("calendar", "v3", credentials=creds)

        # Fetch a list of messages.
        # 'q' is the query to filter messages. Here we get unread, non-promotional emails.
        results = (
            gmail_service.users()
            .messages()
            .list(userId="me", q="is:unread from:classroom.google.com subject:assignment", maxResults=5)
            .execute()
        )
        messages = results.get("messages", [])

        if not messages:
            print("No new unread emails found.")
            sendNotification(
                topic,
                "No New Assignments",
                "There are no new as of yesterday. Please check your Google Classroom for updates."
            )
            return

        print("Found new emails:\n")
        for message in messages:
            msg = (
                gmail_service.users()
                .messages()
                .get(userId="me", id=message["id"], format="full")
                .execute()
            )
            
            payload = msg.get("payload", {})
            headers = payload.get("headers", [])
            
            # Extract the subject from the headers
            subject = "No Subject"
            for header in headers:
                if header["name"] == "Subject":
                    subject = header["value"]
                    break

            # Get the email body
            parts = payload.get("parts", [])
            body_data = ""
            if parts:
                # Get the first text/plain part of the email
                part = parts[0]
                body = part.get("body", {})
                body_data = body.get("data", "")
            else:
                # If no parts, the body is in the main payload
                body_data = payload.get("body", {}).get("data", "")

            # Decode the Base64url body
            if body_data:
                decoded_body = base64.urlsafe_b64decode(body_data).decode("utf-8")
                details = analyze(subject, decoded_body)
                if details and details.get("due_date"):
                    create_calendar_event(calendar_service, details)
                    sendNotification(
                        topic,
                        details.get("title", "New Assignment"),
                        details.get("message", "You have a new assignment.")
                    )
                    time.sleep(1) # To avoid hitting API rate limits
                # Print a snippet of the body to keep the output clean
                snippet = (decoded_body[:250] + '...') if len(decoded_body) > 250 else decoded_body
            else:
                snippet = "No text content found."


            # print(f"--- Subject: {subject} ---")
            # print(snippet)
            # print("-" * (len(subject) + 20) + "\n")


    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()