from .models import AudioBooks
from rest_framework import serializers


class AudioBookSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudioBooks
        fields = ('audioBook',)
