from datetime import datetime

def create_calendar_event(calendar_service, details):
    """Creates a Google Calendar event from the details extracted by Gemini."""
    
    # The due date is just a date, so we'll make the event last 1 hour on that day
    # Let's set the due time to 5 PM on the due date.
    due_date = datetime.strptime(details['due_date'], "%Y-%m-%d")
    start_time = due_date.replace(hour=16, minute=0) # 4:00 PM
    end_time = due_date.replace(hour=17, minute=0)   # 5:00 PM

    # Get the local timezone
    local_timezone = datetime.now().astimezone().tzname()

    event = {
        'summary': details['title'],
        'description': details.get('description', 'No description provided.'),
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': local_timezone,
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': local_timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 120}, # 2-hour popup reminder
                {'method': 'email', 'minutes': 1440}, # 1-day email reminder
            ],
        },
    }

    try:
        created_event = calendar_service.events().insert(calendarId='primary', body=event).execute()
        print(f"✅ Event created: '{created_event['summary']}'")
        print(f"   Link: {created_event['htmlLink']}")
    except HttpError as error:
        print(f"❌ An error occurred creating the calendar event: {error}")