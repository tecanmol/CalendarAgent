# 📅 CalendarAgent

> Automatically extract assignment details from Gmail using AI and create Google Calendar events — with notifications!

---

## 🚀 Overview

**CalendarAgent** is an intelligent automation tool that:
- Connects to your Gmail inbox
- Reads recent unread assignment emails (like from Google Classroom)
- Uses Google's Gemini AI to extract structured data (like title, due date, and description)
- Automatically creates Google Calendar events
- Sends push notifications using [ntfy.sh](https://ntfy.sh)

This project is designed for students or educators who want to streamline their assignment tracking workflow using Python, Google APIs, and generative AI.

---

## 🗂️ Project Structure

```

tecanmol-calendaragent/
├── main.py                 # Entry point: fetch emails, analyze, and create events
├── analyze\_email.py        # Uses Gemini API to parse email content into structured JSON
├── addTocalendar.py        # Creates Google Calendar events using extracted data
├── notify.py               # Sends notifications using ntfy.sh
├── requirements.txt        # All required Python dependencies
├── .github/workflows/
│   └── run.yml             # GitHub Actions workflow (runs daily at 8 AM IST)
└── README.md               # This file

````

---

## 🧠 How It Works

1. `main.py` connects to Gmail and fetches unread assignment emails.
2. The email subject and body are sent to Gemini (`analyze_email.py`) to extract assignment details.
3. If a valid `due_date` is found, `addTocalendar.py` schedules a 1-hour calendar event on that date.
4. `notify.py` sends a notification to your preferred topic on ntfy.sh.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/tecanmol-calendaragent.git
cd tecanmol-calendaragent
````

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Google API Access

* Create a project in [Google Cloud Console](https://console.cloud.google.com/)
* Enable **Gmail API** and **Google Calendar API**
* Create OAuth 2.0 credentials and download `credentials.json` to the project root
* The first run will trigger a browser prompt to authenticate; it will store `token.json` for future use

### 4. Set Up Environment Variables

Create a `.env` file with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

---

## 🔔 Notification Setup (Optional)

This project uses [ntfy.sh](https://ntfy.sh) for push notifications.

You can customize the topic in `main.py`:

```python
topic = "cal-ai-agent-alerts-u4xqz"
```

Then subscribe to your topic using any ntfy client or app.

---

## 🧪 Running the Agent

### Locally

```bash
python main.py
```

### On a Schedule (GitHub Actions)

The repo includes a scheduled workflow (`run.yml`) that runs daily at **8 AM IST**:

```yaml
on:
  schedule:
    - cron: "30 2 * * *"  # UTC = 8:00 AM IST
```

To enable it:

* Add `GEMINI_API_KEY`, `TOKEN_JSON`, and `CREDENTIALS_JSON` as [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* Secrets must be **Base64-encoded** versions of the respective files

---

## ✅ Example Output

* 📥 Reads emails like:

  ```
  Subject: Assignment 4 - Machine Learning
  Due: August 10th
  ```

* 🧠 Extracts:

  ```json
  {
    "title": "Assignment 4",
    "due_date": "2025-08-10",
    "description": "Machine Learning homework due on August 10th.",
    "message": "Don't forget Assignment 4 due tomorrow!"
  }
  ```

* 📅 Creates event in your Google Calendar

* 🔔 Sends notification via ntfy

---

## 📌 Requirements

* Python 3.10+
* Google Cloud project with Gmail & Calendar APIs enabled
* Gemini API key (via Google AI Studio or console)

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to change.

---

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)

---

## ✨ Acknowledgements

* [Google Generative AI](https://makersuite.google.com/)
* [Google APIs](https://developers.google.com/)
* [ntfy.sh](https://ntfy.sh)

---

*Keep your calendar smart and stress-free!*

---

## 💬 Contact [me](https://anmol.is-a.dev/)