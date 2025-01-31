 Weather Application Documentation

Project Overview
The Weather Application is a web-based platform that provides real-time weather updates, forecasts, and additional features such as a to-do list, alarm functionality, and a distance calculator. It is built using Python Django framework, HTML, CSS, and JavaScript.

 Features
1. Weather Updates - Users can search for a city to get real-time weather conditions.
2. Weather Tips & Fun Facts - Displays useful weather-related tips and interesting fun facts.
3. tailed Forecast - Provides a multi-day weather forecast.
4. Severe Weather Alerts - Shows alerts about extreme weather conditions.
5. To-Do List - Users can add and remove tasks.
6. Alarm Functionality - Users can set an alarm with a custom message and an alert sound.
7. Distance Calculator - Calculates the distance and estimated travel time between two locations.

Technologies Used
- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Libraries: Font Awesome, Ionicons, Fetch API

File Structure
- `index.html` - Main HTML structure and UI elements.
- `mans.css` - Styles for the weather app.
- `script.js` - JavaScript functionalities including weather API calls, to-do list, and alarm handling.
- `views.py` - Django views handling user requests.
- `urls.py` - URL routing for different pages.
- `models.py` - Database models (if applicable).

Functionalities and Implementation
 1. Weather Search
- Users enter a city name in the search bar.
- JavaScript fetches weather data (mock API in this version).
- UI updates with temperature, condition, and forecast.

2. To-Do List
- Users can add tasks which get displayed in a list.
- Tasks can be removed dynamically.

 3. Alarm System
- Users set an alarm time and optional message.
- An alert is triggered when the time matches the system time.

4.Distance Calculator
- Users enter "From" and "To" locations.
- Fetch request is sent to Django backend to calculate distance and duration.
- Response is displayed dynamically.

 Deployment Instructions
1. Install Django and dependencies:
   
   pip install django
   
2. Run the server:
  
   python manage.py runserver
  
3. Open the browser and navigate to `http://127.0.0.1:8000/`.

Future Improvements
- Integrate real API for weather data.
- User authentication and profile management.
- Improved UI design and responsiveness.

Author
PEACE NKHWAZI(2024)
