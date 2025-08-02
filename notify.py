import requests

def sendNotification(topic: str, title: str, message: str):
    try:
        requests.post(
            f"https://ntfy.sh/{topic}",
            data=message.encode('utf-8'),
            headers={
                "Title": title,
                "Priority": "default", # Or "high" for urgent notifications
                "Tags": "calendar,robot" # Emojis work here! (e.g., "📅,🤖")
            }
        )
        print(f"notification send to topic: {topic}")

    except Exception as e:
        # If the notification fails, we don't want the whole script to crash.
        print(f"Error sending notification: {e}")
