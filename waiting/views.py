from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from waiting.serializers import WaitingSerializer


# Create your views here.

class WaitlistView(APIView):
    def post(self, request):
        email = request.data.get('email')
        full_name = request.data.get('full_name')
        try:
            email = Waitlist.objects.get(email=email)
            return Response({
                "message": "You have already joined the waitlist"
            })
        except Waitlist.DoesNotExist:
            waitlist = Waitlist.objects.create(name=full_name, email=email)
            return Response({
                "message": "You have joined the waitlist",
                "data":WaitingSerializer(waitlist).data
            })