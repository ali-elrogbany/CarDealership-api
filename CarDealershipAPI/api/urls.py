from django.urls import path, include

from .views import *

urlpatterns = [
    path('cars', CarView.as_view()),
]