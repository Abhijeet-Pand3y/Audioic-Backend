from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from .serializers import AudioBookSerializers
from .models import AudioBooks
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.conf import settings
import os




# @api_view(['GET'])
# def stream_audio(request):
#     id = request.headers.get('id',5)
#     Audio = AudioBooks.objects.filter(id=id).get()
#     audio_file = Audio.audio_file
#     audio_file_path = audio_file.path
#     range_header = request.headers.get('Range')
#     if range_header:
#         # Get the byte range from the range header
#         start, end = range_header.split('-')
#         start = int(start)
#         if end:
#             end = int(end)
#         else:
#             end = audio_file.size - 1
#         # Create a StreamingHttpResponse with the appropriate chunk size
#         response = HttpResponse(
#             audio_file,
#             content_type='audio/mp4',
#             #chunked = 'True',
#         )
#         # Set the Content-Range header with the correct byte range
#         response['Content-Range'] = f'bytes {start}-{end}/{audio_file.size}'
#     else:
#         # Create a normal StreamingHttpResponse
#         response = HttpResponse(
#             open(audio_file_path, 'rb'),
#             content_type='audio/mp4',
#             #chunked = 'True',
#         )
#     # Set the Content-Length header with the size of the audio file
#     response.chunked = 'True'
#     #response['Content-Length'] = 52951632
#     #response['Transfer-Encoding'] = 'chunked'
#     return response


@api_view(['GET'])
def stream_audio(request):
    id = request.GET.get('id',6)
    start = request.GET.get('start',0)
    end = request.GET.get('end',100000000)
    Audio = AudioBooks.objects.filter(id=id).get()
    file = Audio.audio_file
    file_path = file.path
    # Check if the start and end range are valid
    if start == None or end == None:
        return HttpResponseBadRequest('Invalid range')
    try:
        start = int(start)
        end = int(end)
    except ValueError:
        return HttpResponseBadRequest('Invalid range')

    # Check if the file exists
    if not os.path.exists(file_path):
        return HttpResponseNotFound('File not found')

    # Open the file in binary mode
    audio_file = open(file_path, 'rb')

    # Seek to the start of the range
    audio_file.seek(start)

    # Read the range of bytes from the file
    chunk = audio_file.read(end - start + 1)

    # Create an HTTP response with the range of bytes
    response = HttpResponse(chunk, content_type='audio/m4a')

    # Set the Content-Range header
    response['Content-Range'] = 'bytes {}-{}/{}'.format(start, end, file.size)

    # Set the status code to 206 (Partial Content)
    response.status_code = 206

    return response


@api_view(['POST'])
def insertAudioBook(request):
    file = request.FILES['audio_file']
    name = request.POST['audio_name']

    instance = AudioBooks(audioBook=name, audio_file=file)
    instance.save()
    return JsonResponse({"sucess":"File added successfully",})


# @api_view(['GET'])
# def stream_audio(request):
#     id = request.GET.get('id',4)

#     Audio = AudioBooks.objects.filter(id=id).get()
#     audio_file = Audio.audio_file.path
#     response = StreamingHttpResponse(open(audio_file, 'rb'))
#     response['Content-Type'] = 'audio/mp4'
#     return response
