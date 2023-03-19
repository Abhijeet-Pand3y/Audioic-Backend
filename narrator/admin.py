from django.contrib import admin
from .models import NarratedBooks, Narrator
# Register your models here.
model_list = [NarratedBooks, Narrator]
admin.site.register(model_list)

