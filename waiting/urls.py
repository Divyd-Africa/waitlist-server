from django.urls import path
from .views import *
urlpatterns = [
    path('join',WaitlistView.as_view(),name='join'),
    path('broadcast',BroadcastView.as_view(),name='broadcast'),
]