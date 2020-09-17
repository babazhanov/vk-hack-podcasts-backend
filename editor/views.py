from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from editor.models import Sound


def index(request):
    return render(request, "editor/index.html", {"sounds": Sound.objects.all()})


def play(request):
    with open('media/Nauchno-tehnicheskij_Rep_-_Ariya_testirovcshika_PO.mp3', 'rb') as f:
        data = f.read()

    return HttpResponse(data, content_type='audio/mpeg')


def get_sounds(request):
    return JsonResponse(list(Sound.objects.all().values()), safe=False)


def get_sounds(request):
    return JsonResponse(list(Sound.objects.all().values()), safe=False)
