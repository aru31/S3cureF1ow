from django.shortcuts import render
from service.forms import *

# Create your views here.

def index(request):
    return render(request, 'service/index.html', {})

def data(request):
    form = DataForm()
    return render(request, 'service/data.html', {'form': form})
