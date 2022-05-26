from django.shortcuts import render
from . import SimpleExample

# Create your views here.

###
# trips/views.py

from datetime import datetime
from django.shortcuts import render


def hello_world(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),

    })

def SimpleExample(request, filedname):
    return render(request, 'SimpleExample.html')