from rest_framework import serializers
from .models import Events

class EventSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Events
        fields = ('name','detail','organizer','location','date','is_live')