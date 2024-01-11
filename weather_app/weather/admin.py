from django.contrib import admin

from weather.models import Coordinate


@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    search_fields = ('name',)
