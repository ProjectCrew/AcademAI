from flask import Flask, request, render_template
import os
import openai
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# Replace with your OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')	

# Replace with the path to your Google Calendar API credentials JSON file
google_calendar_credentials = os.getenv('GOOGLE_CALENDAR_CREDENTIALS')

def chat_with_gpt(input_text):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=input_text,
        max_tokens=500,
        api_key=api_key
    )
    return response.choices[0].text.strip()

def create_google_calendar_event(title, description, start_time, end_time, calendar_id, credentials, timezone):
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': timezone,
        },
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    
    event_id = event['id']
    event_link = f'https://calendar.google.com/calendar/r/event?eid={event_id}'
    
    return event_link

def create_and_share_public_calendar(credentials, learn, level, days, timezone):
    service = build('calendar', 'v3', credentials=credentials)
    
    calendar = {
        'summary': f'Personalized Schedule for Learning {learn}',
        'description': f'This calendar was created by a bot. It contains a personalized schedule for learning {learn} for {level} in {days} days.',
        'timeZone': timezone,
    }
    
    created_calendar = service.calendars().insert(body=calendar).execute()
    calendar_id = created_calendar['id']
    
    rule = {
        'scope': {
            'type': 'default',
        },
        'role': 'reader',
    }
    service.acl().insert(calendarId=calendar_id, body=rule).execute()
    
    return calendar_id

def generate_sample_schedule(learn, level, days, timezone):
    # Generate a simple schedule for demonstration
    schedule = []
    for day in range(1, int(days) + 1):
        title = f'Day {day} - Learn {learn}'
        task = f'Study {learn} at {level} level for the entire day.'
        schedule.append((title, task))
    return schedule

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        learn = request.form['learn']
        level = request.form['level']
        days = request.form['days']
        timezone = request.form['timezone']

        user_input = f"Make me a {days} day schedule for learning {learn} for someone who is already at an {level}. Do not combine 2 days together. Give me just the days and the title together and then the task (Only One Task a Day but explain in detail) to be performed that day as a single paragraph. Also, include a url on the task paragraph. Precede day with a # and the tasks with a *." \

        # Use GPT-3 to generate the schedule
        response = chat_with_gpt(user_input)

        # Initialize empty arrays for titles and tasks
        titles = []
        tasks = []

        # Your text data
        schedule_text = response

        # Split the text into lines
        lines = schedule_text.split('\n')

        # Iterate through the lines and extract titles and tasks
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                titles.append(line)
            elif line.startswith('*'):
                tasks.append(line)

        # Replace with your Google Calendar API credentials JSON file
        credentials = service_account.Credentials.from_service_account_file(google_calendar_credentials)

        # Calculate the start date for the schedule
        start_date = datetime.now()

        # Create and share a public calendar
        calendar_id = create_and_share_public_calendar(credentials, learn, level, days, timezone)

        schedule = generate_sample_schedule(learn, level, days, timezone)

        for i in range(len(titles)):
            title = titles[i].lstrip('#').strip()
            task = tasks[i].lstrip('*').strip()

            # Calculate start and end times for the event (whole day event starting from 00:00 and ending at 23:59)
            start_time = start_date.strftime('%Y-%m-%d') + 'T00:00:00'
            end_date = start_date + timedelta(days=1)
            end_time = end_date.strftime('%Y-%m-%d') + 'T23:59:59'

            # Create a Google Calendar event for each day's schedule in the shared calendar
            event_link = create_google_calendar_event(title, task, start_time, end_time, calendar_id, credentials, timezone)

            # Move to the next day
            start_date = end_date

        result = f"Google Calendar events have been created in the shared calendar. " \
                 f"You can find the calendar at this link: " \
                 
        message = f"https://calendar.google.com/calendar/r?cid={calendar_id}"



        return render_template('result.html', result=result, message=message)

    return render_template('input_form.html')

if __name__ == "__main__":
    app.run()
