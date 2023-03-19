from rest_framework import serializers
from .models import Author, AuthoredBooks


class AuthorSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'description', 'facebook_id', 'instagram_id', 'twitter_id')


class AuthoredBooksSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AuthoredBooks
        fields = ('author', 'books_authored')