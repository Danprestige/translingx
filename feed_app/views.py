# feed_app/views.py
from django.http import HttpResponse

def feed_home(request):
    return HttpResponse("Feed app is working!")