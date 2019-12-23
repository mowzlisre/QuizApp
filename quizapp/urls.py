from django.urls import path
from . import views
urlpatterns = [
  
    path('test/<int:pk>/',views.TestAttendingView.as_view()),
    path('home/',views.HomeView.as_view()),
]
