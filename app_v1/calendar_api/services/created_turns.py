from datetime import time, date, datetime, timedelta

from ..models.schedule_model import Schedule
from ..models.day_model import Day
from ..models.detail_calendar_model import DetailCalendar
from ..models.turn_model import Turn
from ..models.state_turn_model import StateTurn

import logger
log = logger.logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------
# -- Es necesario aplicar un sistema de reportes, como logger, el cual se pueda revisar desde un archivo PDF --
# -------------------------------------------------------------------------------------------------------------


def switch_dia(dia):
  sw = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miercoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sabado',
    'Sunday': 'Domingo',
  }
  return sw.get(dia)


# time_delta: suma a una variable del tipo ´time´ un ´timedelta´.
# EJ: time: 08:00:00 timedelta: 00:05:15 => time_delta: 08:05:15
def time_delta(time: time, timedelta: timedelta) -> time:
  start = datetime(
    2000, 1, 1,
    hour=time.hour, minute=time.minute, second=time.second)
  end = start + timedelta
  return end.time()


def save_turns(turns):
  turns_save = []
  for turn in turns:
    try:
      turn.save()
      turns_save.append(turn)
      log.debug(f'turn {turn.id_turn}. {turn}: Se ha creado correctamente')
    except Exception as ex:
      # Imprimir un registro con todos los datos del turno que no se puede guardar en BD
      log.error(f'turn {turn}: Error al llamar save() ; {ex}')
  return turns_save


def validate_created_turn(schedule: Schedule, detail_calendar: DetailCalendar) -> bool:
  log.debug(f'Inicio metodo validate_created_turn() -> schedule: {schedule} -> detail_calendar: {detail_calendar}')
  
  # Validar que existe schedule en BD
  try:
    Schedule.objects.get(pk = schedule.id_schedule)
  except:
    log.warning(f'detail calendar {detail_calendar.date} y schedule {schedule}: No existe schedule en BD')
    return False
  
  # Validar que existe detail_calendar en BD
  try:
    DetailCalendar.objects.get(pk = detail_calendar.id_detail_calendar)
  except:
    log.warning(f'detail calendar {detail_calendar.date} y schedule {schedule}: No existe detail calendar en BD')
    return False
  
  # Validar que el dia sea futuro (actual)
  if (detail_calendar.date < date.today()):
    log.warning(f'detail calendar {detail_calendar.id_detail_calendar}. {detail_calendar.date} y schedule {schedule.id_schedule}. {schedule}: El dia {detail_calendar.date} es pasado')
    return False
  
  # Validar si el dia esta incluido en al menos uno de los dias del schedule
  make_detail_calendar = False
  day_str = switch_dia(detail_calendar.date.strftime('%A')) 
  for day in schedule.days.all():
    if(day_str == day.name_day):
      make_detail_calendar = True
      break
  if (not make_detail_calendar):
    # Devolver un logger indicando que no se ejecuta el script de created_turns
    log.warning(f'detail calendar {detail_calendar.id_detail_calendar}. {detail_calendar.date} y schedule {schedule.id_schedule}. {schedule}: Schedule no posee configurado el dia {day_str}')
    return False
  
  # Validar que no existen turnos creados para el schedule en el dia indicado
  turns = Turn.objects.filter(enabled = True, detail_calendar = detail_calendar, start_time_turn__range = (schedule.start_time_schedule, schedule.end_time_schedule))
  if (len(turns) > 0):
    log.warning(f'detail calendar {detail_calendar.id_detail_calendar}. {detail_calendar.date} y schedule {schedule.id_schedule}. {schedule}: Existe al menos 1 turno creado con anterioridad')
    return False
  
  return True


# Crea todos los turnos (en estado libre) para un horario (schedule) y un dia (detail_calendar) especifico
def created_turns(schedule: Schedule, detail_calendar: DetailCalendar):
  try:
    log.info(f'Inicio metodo created_turns() -> schedule: {schedule} -> detail_calendar: {detail_calendar}')
    
    # Validar que se pueden crear los turnos
    if (not validate_created_turn(schedule, detail_calendar)):
      return None
    
    # Turnos maximos en un horario (numero entero). EJ: horario: 08:00 a 09:10 con turno de 20 minutos => turns_max = 3
    start_time_int: int = schedule.start_time_schedule.hour * 60 + schedule.start_time_schedule.minute
    end_time_int: int = schedule.end_time_schedule.hour * 60 + schedule.end_time_schedule.minute
    turns_max: int = (end_time_int - start_time_int) // schedule.interval_turn
    
    # Variables
    turns = []
    interval_turn = timedelta(minutes= schedule.interval_turn)
    start_time: time = schedule.start_time_schedule
    state_libre: StateTurn = StateTurn.objects.get(enabled=True, state_turn = 'Libre')
    for i in range(turns_max):
      end_time: time = time_delta(start_time, interval_turn)
      # Validar si el turno a crear no se pasa de la hora fin del horario
      if (end_time > schedule.end_time_schedule):
        break
      
      # Crear el turno
      turn: Turn = Turn(
        start_time_turn = start_time,
        end_time_turn = end_time,
        state_turn = state_libre,
        detail_calendar = detail_calendar
      )
      
      turns.append(turn)
      start_time = end_time
    
    return save_turns(turns)
  except Exception as ex:
    log.error(f'Error al llamar created_turns() -> schedule: {schedule} -> detail_calendar: {detail_calendar} ; {ex}')