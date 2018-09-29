from django.urls import path

from service import views

app_name = 'service'

urlpatterns = [
    path('qr/', views.index, name='index'),
    path('data/', views.data, name='data'),
]
