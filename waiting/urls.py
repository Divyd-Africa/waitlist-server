from django.urls import path
from .views import *
urlpatterns = [
    path('join',WaitlistView.as_view(),name='join'),
]