from django.urls import path
from . import views
urlpatterns = [
    path('gettest/',views.TestAttendingView.as_view()),
    path('testing/',views.TestingView.as_view())
]
