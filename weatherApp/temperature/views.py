from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def home(request):
    appid = 'your_api_key' #the previous one has been deactivated
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()

    form = CityForm()

    cities = City.objects.all()

    weatherData = []

    for city in cities:
        response = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon']
        }
        weatherData.append(city_weather)

    context = {'weather_data': weatherData, 'form': form}
    return render(request, 'base.html', context)