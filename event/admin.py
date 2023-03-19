from django.contrib import admin
from . models import Events
# Register your models here.

model_list = [Events]

admin.site.register(model_list)