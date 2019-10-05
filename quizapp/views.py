
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from io import BytesIO
from django.core import files
from django.http import HttpResponse
from django.core.exceptions import SuspiciousOperation
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
import uuid
import requests
from twilio.twiml.messaging_response import MessagingResponse, Message


class UserCreateView(APIView):
    def post(self, request):
        if User.objects.filter(email=request.POST.get('email')).exists():
            user = User.objects.get(email=request.POST.get('email'))
            return Response({"status": 301, "id": user.unique_id})
        else:
            user = User()
            user.unique_id = uuid.uuid4()
            user.email = request.POST.get('email')
            user.name = request.POST.get('name')
            user.save()
            return Response({"status": 200, "id": user.unique_id})


class TestAttendingView(APIView):
    def get(self, request):
        return Response({
            "data": [
                {'pk': test.pk,
                    'name': test.name,
                    'questiondata': [
                        {
                            'question': question.question,
                            'options': [option.option for option in question.options.all()],
                            'correct_option':question.correct_option


                        }
                        for question in test.question.all()

                    ]

                 }
                for test in Test.objects.all()]
        })


def create_message(msg):

    response = MessagingResponse()
    response.message(msg)
    return str(response)


class TestingView(APIView):
    def post(self, request):
        # Name:john doe,Location:chennai,Email:a@gmail.com
        print(request.POST)
        num = request.POST.get('From').split(':')[1]
        if 'Body' in request.POST:
            if request.POST.get("Body") == "Hi":

                person, created = Person.objects.get_or_create(num=num)
                print(person.num)
                return HttpResponse(create_message("Hey"))
            elif 'lost'.lower() in request.POST.get("Body").lower():
                person = get_object_or_404(Person, num=num)
                person.lost = True
                person.save()
                return HttpResponse(create_message("Cool !! Where did you lost your child give his name in the format Name:"))
            elif 'found'.lower() in request.POST.get("Body").lower():
                person = get_object_or_404(Person, num=num)
                person.found = True
                person.save()

                return HttpResponse(create_message("Cool !! Where did you lost your child give his name in the format Name:"))
            elif "Name:" in request.POST.get('Body'):
                person = get_object_or_404(Person, num=num)
                data = request.POST.get('Body').replace('\n', ':').split(':')
                person.name = data[1]
                person.location = data[3]
                person.save()
                print(person.location)
                return HttpResponse(create_message(f"The thing you entered is {request.POST.get('Body')} send the Image of the child"))
            elif 'MediaUrl0' in request.POST:
                person = get_object_or_404(Person, num=num)
                resp = requests.get(request.POST.get('MediaUrl0'))
                fp = BytesIO()
                fp.write(resp.content)
                person.img.save(f'{uuid.uuid4()}.jpeg', files.File(fp))

                return HttpResponse(create_message("Ohoo!! It works"))
            else:
                return HttpResponse(create_message("You already said HI"))

        return Response()
