from django.contrib import admin
from .models import *


@admin.register(Sound)
class SoundAdmin(admin.ModelAdmin):
    pass