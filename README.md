# Personalized Learning Schedule Generator

This project is a personalized learning schedule generator that utilizes OpenAI's GPT-3 to create a custom learning schedule for a specific learning goal, skill level, and duration. It also integrates with Google Calendar to automatically create and share a public calendar with the generated schedule.


## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [License](#license)

## Features

- Generate personalized learning schedules for specific learning goals.
- Consider skill level and the number of days for the schedule.
- Create daily tasks with detailed explanations and provide URLs for each task.
- Automatically generate Google Calendar events for the schedule.
- Share a public Google Calendar with the generated schedule.

## Demo
### Webpage
A live demo of this project is available at [Demo Link](https://arnitsinha.pythonanywhere.com).
### Webpage Showcase
![alt-text](hackrpi-demo.gif)
### Executable Showcase
![alt-text](Hackrpi-Demo-Exe.gif)

## Getting Started

### Web Server

To run this project locally or deploy it on your server, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

3. Set up your environment variables:

   Obtain an OpenAI API key and set it as an environment variable OPENAI_API_KEY.
   Provide the path to your Google Calendar API credentials JSON file as an environment variable GOOGLE_CALENDAR_CREDENTIALS.

4. Run the Flask application:

   ```bash
   python app.py

5. Access the application in your web browser at http://localhost:5000.

### GUI

In addition to the command-line version, we also offer a user-friendly Graphical User Interface (GUI) for creating personalized learning schedules. The GUI version makes it even easier to generate schedules and manage your calendar events.

To access the GUI version:

1. Download the CodeGUI.exe file.
2. Set up your environment variables:
   Obtain an OpenAI API key and set it as an environment variable OPENAI_API_KEY.
   Provide the path to your Google Calendar API credentials JSON file as an environment variable GOOGLE_CALENDAR_CREDENTIALS.
3. Run it and enjoy!

## Usage
Fill out the input form on the application's homepage with the following details:

Learning goal (e.g., "Python programming").
Skill level (e.g., "Intermediate").
Number of days for the learning schedule.
Your timezone.
Click the "Generate Schedule" button.

The application will use GPT-3 to generate a personalized learning schedule based on your input.

Google Calendar events will be automatically created in a shared public calendar.

You will receive a link to the shared calendar to access your generated schedule.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
