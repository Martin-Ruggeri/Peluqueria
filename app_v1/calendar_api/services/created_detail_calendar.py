from datetime import date, timedelta

from .created_turns import created_turns

from ..models.calendar_model import Calendar
from ..models.schedule_model import Schedule
from ..models.detail_calendar_model import DetailCalendar

import logger
log = logger.logging.getLogger(__name__)


def created_detail_calendar():
  days_extra: int = 2
  day = date.today() + timedelta(days= days_extra)
  
  try:
    log.info(f'Inicio metodo created_detail_calendar() para el dia {day.strftime("%d/%m/%Y")}')
    
    calendars = Calendar.objects.filter(enabled=True)
    for calendar in calendars:
      # Si ya existe un detail calendar continua al proximo calendar
      if (DetailCalendar.objects.filter(enabled = True, calendar = calendar, date = day).count() > 0):
        log.warning(f'calendar {calendar.id_calendar}. {calendar}: Ya existe detail calendar {day}')
        continue
      
      # Crear detail calendar
      detail_calendar: DetailCalendar = DetailCalendar(
        date = day,
        calendar = calendar,
      )
      
      # No me parece correcto guardar el calendar tan precipitadamente (Revisar como modificar para guardar al final)
      detail_calendar.save()
      
      # Crea los turnos por cada schedule
      schedules = Schedule.objects.filter(enabled = True, calendar = calendar)
      for schedule in schedules:
        created_turns(schedule, detail_calendar)
    
  except Exception as ex:
    log.critical(f'Error al llamar created_detail_calendar() para el dia {day.strftime("%d/%m/%Y")}; {ex}')