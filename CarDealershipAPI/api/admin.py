from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Color)
admin.site.register(Condition)
admin.site.register(EngineType)
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Car)