from django.contrib import admin
from .models import Cuisine, Menu, Restaurant


admin.site.register(Cuisine)
admin.site.register(Menu)
admin.site.register(Restaurant)