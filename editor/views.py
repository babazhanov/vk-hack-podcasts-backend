import os
import wave
import sox
import uuid
import numpy as np

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from editor.models import Sound


def index(request):
    return render(request, "editor/index.html", {"sounds": Sound.objects.all()})


def set_defaults(request, ignore_none=False):
    if request.session["last_file"] is None or ignore_none:
        sound_ids = Sound.objects.all().values_list('id', flat=True)
        pk = min(sound_ids)
        request.session["last_file"] = os.path.join('media/', Sound.objects.get(id=pk).filename)
        request.session['current_file'] = request.session["last_file"]


def play(request):
    set_defaults(request)
    with open(request.session['current_file'], 'rb') as f:
        data = f.read()

    return HttpResponse(data, content_type='audio/mpeg')


def get_sounds(request):
    return JsonResponse(list(Sound.objects.all().values()), safe=False)


def get_file_info(filename):
    tfm = sox.Transformer()
    tmpfile = os.path.join('media/', str(uuid.uuid4()) + '.wav')
    tfm.build(filename, tmpfile)
    spf = wave.open(tmpfile, "r")

    n_samples = spf.getnframes()
    sample_rate = spf.getframerate()

    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, "Int16")
    wave_form = np.max(np.abs(signal.reshape(-1, sample_rate)), axis=1)

    return {
        "length": int(n_samples / sample_rate * 1000),
        "wave": wave_form.tolist()
    }


def get_track(request):
    if request.method == "POST":
        pk = request.POST.get("id")
        sound_ids = Sound.objects.all().values_list('id', flat=True)
        if pk not in sound_ids:
            set_defaults(request, True)
        else:
            request.session["last_file"] = os.path.join('media/', Sound.objects.get(id=pk).filename)
            request.session['current_file'] = request.session["last_file"]

        return JsonResponse(get_file_info(request.session['current_file']))


def cut(request):
    if request.method == "POST":
        set_defaults(request)

        start = request.POST.get("start")
        end = request.POST.get("end")

        request.session["last_file"] = request.session['current_file']
        request.session['current_file'] = os.path.join('media/', str(uuid.uuid4()) + '.mp3')

        tfm = sox.Transformer()
        tfm.trim(start / 1000, end / 1000)
        tfm.build(request.session['last_file'], request.session['current_file'])

        return JsonResponse(get_file_info(request.session['current_file']))
