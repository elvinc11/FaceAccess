from django.contrib import admin
from .models import User, Detected, Website

# Register your models here.

admin.site.register(User)
admin.site.register(Detected)
admin.site.register(Website)