from django.urls import path, include

from .views import *

urlpatterns = [
    path('cars', CarView.as_view()),
    path('car-makes', CarMakesView.as_view()),
    path('car-models', CarModelsView.as_view()),
    path('car', CarView.as_view()),
]