from django.urls import path

from . import views
from .views import home, exit, delete_vote, disable_poll

app_name = "polls"
urlpatterns = [
    path("", home, name="home"),#127.0.0.1:8000/  #cambiar a clase cuando pueda
    path("polls/", views.IndexView.as_view(), name="index"),#127.0.0.1:8000/polls/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),#127.0.0.1:8000/polls/1/detail/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),#127.0.0.1:8000/polls/1/results/
    path("<int:question_id>/vote/", views.vote, name="vote"),#127.0.0.1:8000/1/polls
    path("<int:question_id>/delete_vote/", delete_vote, name="delete_vote"), #cambiar a clase cuando pueda
    path("<int:question_id>/disable_poll/", disable_poll, name="disable_poll"),#cambiar a clase cuando pueda
    path('logout/', exit, name="exit"),#127.0.0.1:8000/account/logout/ 
]