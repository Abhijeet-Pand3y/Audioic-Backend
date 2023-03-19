from .models import NarratedBooks, Narrator
from .serializers import NarratedBooksSerializers, NarratorSerializers
from django.http import JsonResponse
from rest_framework.decorators import api_view 
from audiobooks.models import AudioBooks
from rest_framework.response import Response
import json
from audiobooks.models import AudioBooks
from audiobooks.serializers import AudioBooksSerializers



@api_view(["GET",])
def getAllNarrator(request):
    try:
        narrators = Narrator.objects.all()
        serialized_narattors = NarratorSerializers(narrators, many=True)
    
    except:
        return JsonResponse({"error": "Narrators are currently dormant"})
    return JsonResponse({"narrator_list": serialized_narattors.data})


@api_view(["GET",])
def getNarrator(request):

    id = request.GET["id"]
    my_dict = {}
    audio_book_list=[]
    my_list = []
    narr_obj = Narrator.objects.get(id=id)
    narrator_serializer = NarratorSerializers(narr_obj)
    my_dict.update(dict(narrator_serializer.data))

    audio_book = request.GET.get('audio_book','None')
    try:
        NarratedBookModel = NarratedBooks.objects.get(booksNarated = audio_book)
    except:
        return JsonResponse({'error':'No narrator found for given audio book'})
    
    narrator_for_the_book = NarratedBookModel.narrator
    try:
        NarratorModel = Narrator.objects.filter(narrator = narrator_for_the_book)
        image = NarratorModel.photo.url
    except:
        pass
    return JsonResponse({'url': image})

@api_view(['POST',])
def insertInNarrator(request):

    
    body = json.loads(request.body)
    
    first_name = body["first_name"]
    last_name = body["last_name"]
    middle_name = body["middle_name"]
    audiobook  = body["audiobook"]
    description = body["description"]
    facebook_id = body["facebook_id"]
    instagram_id = body["instagram_id"]
    twitter_id = body["twitter_id"]
    photo = body["photo"]
    
    instance = Narrator(first_name=first_name, last_name=last_name,middle_name=middle_name, description=description, facebook_id=facebook_id, instagram_id=instagram_id, twitter_id=twitter_id, photo=photo)
    instance.save()
    
    audiobook_instance = AudioBooks(audioBook = audiobook)
    audiobook_instance.save()

    narrated_books_instance = NarratedBooks(narrator = instance, booksNarated = audiobook_instance)
    narrated_books_instance.save()
    
    
    return JsonResponse({'success':'Narrator added'})

@api_view(["GET",])
def deleteNarrator(request):
    id = request.GET["id"]

    narr_obj = Narrator.objects.get(id=id)
    narr_obj.delete()
    return JsonResponse({"success":"deleted"})
    