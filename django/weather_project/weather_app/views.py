import urllib.request
import json
from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

def index(request):
    api_key = 'IZIgNUa46hWzNoRcbfOyZX4hBd6X4dJPKWDrHMr8'
    url = f'https://newsapi.org/v2/top-headlines?category=weather&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        news_data = response.json()
        articles = news_data.get('articles', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        articles = []

    return render(request, 'weather_app/index.html', {'articles': articles})

def get_weather(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        api_key = '25ba1b12297eceffed26492ff739c8fc'
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}'

        try:
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()  # This will raise an HTTPError for bad responses
            weather_data = weather_response.json()

            forecast_response = requests.get(forecast_url)
            forecast_response.raise_for_status()  # This will raise an HTTPError for bad responses
            forecast_data = forecast_response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return JsonResponse({'error': 'Error fetching weather data'}, status=500)

        return JsonResponse({
            'weather': weather_data,
            'forecast': forecast_data,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        else:
            user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'weather_app/register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to 'index' after successful login
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'weather_app/home.html')

def home(request):
    return render(request, 'weather_app/home.html')

def index(request):
    return render(request, 'weather_app/index.html')

def about(request):
    return render(request, 'weather_app/about.html')

def distance_calculation(request):
    if request.method == "GET":
        from_location = request.GET.get('from')
        to_location = request.GET.get('to')
        api_key = 'AIzaSyAPKENEPsb0vIUscPAd2c4aYqcKfmxTz84'
        url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={from_location}&destinations={to_location}&key={api_key}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['rows'][0]['elements'][0]['status'] == 'OK':
                distance = data['rows'][0]['elements'][0]['distance']['text']
                duration = data['rows'][0]['elements'][0]['duration']['text']
                return JsonResponse({'distance': distance, 'duration': duration})
            else:
                return JsonResponse({'error': data['rows'][0]['elements'][0]['status']})
        else:
            return JsonResponse({'error': 'Error fetching data from Google Maps API'})
    return JsonResponse({'error': 'Invalid request method'})

def get_directions(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')

    if origin and destination:
        api_key = settings.GOOGLE_MAPS_API_KEY
        url = 'https://maps.googleapis.com/maps/api/directions/json'
        params = {
            'origin': origin,
            'destination': destination,
            'key': api_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data['status'] == 'OK':
            routes = data.get('routes', [])
            if routes:
                directions = routes[0].get('legs', [])[0].get('steps', [])
                return render(request, 'directions.html', {'directions': directions})
            else:
                return render(request, 'directions.html', {'error': 'No routes found'})
        else:
            return render(request, 'directions.html', {'error': data.get('error_message', 'Error fetching directions')})
    else:
        return render(request, 'directions.html', {'error': 'Origin and destination are required'})


def get_directions(request):
    from_location = request.GET.get('from')
    to_location = request.GET.get('to')

    # Ensure both locations are provided
    if not from_location or not to_location:
        return JsonResponse({'error': 'Both from and to locations are required.'}, status=400)

    # Construct the URL for Google Maps Directions API
    api_key = settings.GOOGLE_MAPS_API_KEY
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={from_location}&destination={to_location}&key={api_key}'

    # Fetch the data from Google Maps Directions API
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        routes = data.get('routes', [])
        if routes:
            route = routes[0]
            legs = route.get('legs', [])
            if legs:
                leg = legs[0]
                distance = leg.get('distance', {}).get('text', '')
                duration = leg.get('duration', {}).get('text', '')
                steps = leg.get('steps', [])
                instructions = [step.get('html_instructions', '') for step in steps]

                return JsonResponse({
                    'distance': distance,
                    'duration': duration,
                    'instructions': instructions
                })
        return JsonResponse({'error': 'No routes found.'}, status=404)

    return JsonResponse({'error': 'Failed to fetch directions.'}, status=500)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Send email
        send_mail(
            f"Contact Form Submission from {name}",
            message,
            email,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )

        return HttpResponseRedirect(reverse('contact'))

    return render(request, 'weather_app/contact.html')

def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'weather_app/profile_update.html', {'form': form})