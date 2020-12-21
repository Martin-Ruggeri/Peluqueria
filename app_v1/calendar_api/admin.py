from django.contrib import admin

from .models.day_model import Day
from .models.schedule_model import Schedule
from .models.calendar_model import Calendar
from .models.detail_calendar_model import DetailCalendar
from .models.turn_model import Turn
from .models.state_turn_model import StateTurn

# Register your models here.
admin.site.register(Day)
admin.site.register(Schedule)
admin.site.register(Calendar)
admin.site.register(DetailCalendar)
admin.site.register(Turn)
admin.site.register(StateTurn)