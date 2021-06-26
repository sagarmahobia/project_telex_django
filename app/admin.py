from django.contrib import admin

from .models import Entity, Category, Icon

admin.site.register((Entity, Category, Icon))
