
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import SuspiciousOperation
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
import uuid
import requests


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


class HomeView(APIView):
    def get(self, request):
        return Response([
            {
                'pk': test.pk,
                'name': test.name,
                'description': test.description
            }
            for test in Test.objects.all()])


class TestAttendingView(APIView):
    def get(self, request, pk):

        test = get_object_or_404(Test, pk=pk)
        return Response(

            {'pk': test.pk,
             'name': test.name,
             'questions': [
                 {
                     'id': question.pk,
                     'question': question.question,
                     'options': [option.option for option in question.options.all()],
                     'answer':question.correct_option


                 }
                 for question in test.question.all()

             ]



             })
