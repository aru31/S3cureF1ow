from django.shortcuts import render
from user.models import Identity
from django.views import generic

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'user/wallet.html'
    context_object_name = 'identity'

    def get_queryset(self):
        return Identity.objects.all()
