from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='main'),
    path('keygen/', views.KeyView, name='keygen'),
    path('verify/', views.SerializerView.as_view(), name='api'),
]
