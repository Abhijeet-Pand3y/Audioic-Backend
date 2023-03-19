from pyexpat import model
from rest_framework import serializers
from .models import NarratedBooks, Narrator

class NarratorSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Narrator
        fields = ('id','first_name','last_name','middle_name','description','facebook_id','instagram_id','twitter_id')


class NarratedBooksSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NarratedBooks
        fields = ('narrator','booksNarated')
        # TODO requires checking what we get 