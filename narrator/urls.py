from django.urls import path
from .views import getAllNarrator, getNarrator, insertInNarrator, deleteNarrator

urlpatterns = [
    path('getAllNarrator/', getAllNarrator, name="GetAllNarrator"),
    path('getNarrator/', getNarrator, name="GetNarrator"),
    path('insertNarrator/', insertInNarrator, name="InsertNarrator"),
    path('deleteNarrator/', deleteNarrator, name="DeleteNarrator"),
]
