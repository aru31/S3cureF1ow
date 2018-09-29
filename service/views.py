from django.shortcuts import render
from service.forms import *

# Create your views here.

def index(request):
    return render(request, 'service/index.html', {'domain': request.META['HTTP_HOST']+'/data/' })

def data(request):
    form = DataForm()
    return render(request, 'service/data.html', {'form': form})
