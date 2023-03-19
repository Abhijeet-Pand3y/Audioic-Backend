from django.urls import path
from . views import getEvents, isEventLive, completedEvents, addEvents

urlpatterns = [
    path('addEvents/', addEvents, name="AddEvents"),
	path('getEvents/', getEvents, name="GetEvents"),
	path('isEventLive/', isEventLive, name="isEventLive"),
	path('completedEvents/', completedEvents, name="completedEvents"),

]