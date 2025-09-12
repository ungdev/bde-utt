from django.urls import path
from . import views

urlpatterns = [
    path("", views.members, name="members"),
    path("board/", views.board, name="board"),
]
