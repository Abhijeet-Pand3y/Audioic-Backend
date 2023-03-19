from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from . models import Events
from . serializers import EventSerializers
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
# from datetime import date, datetime, time
# import pytz
# Create your views here.


api_view(["POST",])
@csrf_exempt
def addEvents(request):
    name = request.POST["name"]
    detail = request.POST["detail"]
    organizer = request.POST["organizer"]
    date = request.POST["date"]
    location = request.POST["location"]

    event_create = Events(name=name, detail=detail, organizer=organizer, date=date, location=location)
    event_create.save()
    return JsonResponse({"Success":"New event added"})


api_view(["GET",])
def getEvents(request):
    try:
        events = Events.objects.filter(is_completed = False)    
    except:
        return JsonResponse({"error": "Events are currently dormant"})

    serialized_narattors = EventSerializers(events, many=True)
    return JsonResponse({"event_list": serialized_narattors.data})


api_view(["GET",])
def isEventLive(request):
    try:
        events = Events.objects.filter(is_completed = False)
    except:
        return JsonResponse({"error": "Events are currently dormant"})

    for event in events:
        now = timezone.now()
        if event.date.date() == now.date():
            if event.date >= now:
                event.is_live = True
                event.save()

    return JsonResponse({"done":"done"})

def completedEvents(request):
    try:
        events = Events.objects.filter(is_completed = False)
    except:
        return JsonResponse({"error": "Events are currently dormant"})

    for event in events:
        now = timezone.now().date()
        if event.date.date() > now :
            event.is_live = False
            event.is_completed = True

    return JsonResponse({"done":"done"})


