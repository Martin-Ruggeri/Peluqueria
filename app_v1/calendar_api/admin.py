from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Day)
admin.site.register(Schedule)
admin.site.register(Calendar)
admin.site.register(DetailCalendar)
admin.site.register(Turn)
admin.site.register(StateTurn)