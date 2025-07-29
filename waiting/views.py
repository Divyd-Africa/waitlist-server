import time
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from waiting.serializers import WaitingSerializer
from django.core.validators import validate_email
import threading

# Create your views here.

class WaitlistView(APIView):
    def post(self, request):
        email = request.data.get('email')
        full_name = request.data.get('full_name')
        if not email or not full_name:
            return Response({'error': 'Please provide email and full name'}, status=400)
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email address'}, status=400)
        try:
            email = Waitlist.objects.get(email=email)
            return Response({
                "message": "You have already joined the waitlist"
            })
        except Waitlist.DoesNotExist:
            waitlist = Waitlist.objects.create(name=full_name, email=email)
            threading.Thread(
                target= send_confirmation_email,
                args = (full_name,email),
                daemon = True,
            ).start()
            return Response({
                "message": "You have joined the waitlist",
                "data":WaitingSerializer(waitlist).data
            })

    def get(self, request):
        return Response({
            "message": "You have reached the waitlist server. Now I believe this route is none of your business. Bye😘",
        })

class BroadcastView(APIView):
    def post(self, request):
        subject = request.data.get('subject')
        message = request.data.get('message')
        if not subject or not message:
            return Response({'error': 'Please provide subject and message'}, status=400)
        broadcast_email(subject, message)
        return Response({
            "message": "Thread has begun execution, mails are being sent. 👍🏾"
        })


def send_confirmation_email(name, email):
    try:
        subject = "🎉 You are on the waitlist for divyd africa!!"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [email]
        html_content = render_to_string("waiting/email_template.html", {"name":name})
        email_message = EmailMultiAlternatives(subject, "", from_email, to)
        email_message.attach_alternative(html_content, "text/html")
        email_message.send(fail_silently=False)
    except Exception as e:
        print(f"failed to send email to {email}. Error:{e}")

def broadcast_email(subject, body):
    def _broadcast():
        from_email = settings.DEFAULT_FROM_EMAIL
        waitlist = Waitlist.objects.all()

        for user in waitlist:
            try:
                print(f"sending to {user.email}")
                connection = get_connection()
                connection.open()
                context = {
                    "name": user.name,
                    "body": body
                }
                html_content = render_to_string("waiting/broadcast_template.html", context)
                msg = EmailMultiAlternatives(subject, "", from_email, [user.email], connection=connection)
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)

                time.sleep(4)
            except Exception as e:
                print(f"Failed to send email to {user.email}. Error: {e}")
        connection.close()
    threading.Thread(target=_broadcast, daemon=True).start()


