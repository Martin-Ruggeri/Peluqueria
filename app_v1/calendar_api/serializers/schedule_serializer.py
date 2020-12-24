from rest_framework import serializers
from datetime import date, timedelta
from ..models.schedule_model import Schedule
from ..models.detail_calendar_model import DetailCalendar
from ..models.turn_model import Turn

class ScheduleSerializer(serializers.ModelSerializer):
  
  def validate(self, data):
    start_time = data.get('start_time_schedule')
    end_time = data.get('end_time_schedule')
    interval_turn = data.get('interval_turn')
    
    errors = {}
    
    # Validar que hora inicio > hora fin
    if (start_time >= end_time):
      errors.update({'end_time_schedule': 'La hora fin debe ser mayor a la hora inicio'})
    
    # Validar que los turnos sean de al menos 15 minutos
    if (interval_turn < 14):
      errors.update({'interval_turn': 'El intervalo de cada turno debe ser al menos de 15 minutos'})  
    
    # Validar si existe otro horario con el que se interponga
    errors.update(validate_interposed_schedule(self,data))
    
    if (len(errors) > 0):
      trows_error(errors)
    
    return data
  
  
  def validate_delete(self,instance):
    data = {}      
    data['start_time_schedule'] = instance.start_time_schedule
    data['end_time_schedule'] = instance.end_time_schedule
    data['interval_turn'] = instance.interval_turn
    data['calendar'] = instance.calendar
    data['days'] = instance.days.all()
    
    errors = {}
    
    errors.update(validate_turn_busy(self, data))
    
    if (len(errors) > 0):
      trows_error(errors)
  
  
  class Meta:
    model = Schedule
    fields = ['id_turn', 'start_time_turn', 'end_time_turn', 'interval_turn', 'calendar', 'days']


def validate_turn_busy(self,data):
  id = self.instance.id_schedule
  start_time = data.get('start_time_schedule')
  end_time = data.get('end_time_schedule')
  days = data.get('days')
  calendar = data.get('calendar')
  
  errors = {}
  
  start_date = date.today()                       # fecha inicio = hoy dia
  end_date = date.today() + timedelta(days = 50)  # fecha fin    = hoy dia + x dias
  details_calendar = DetailCalendar.objects.filter(enabled = True, calendar=calendar, date__range = (start_date, end_date) )
  # Si el detail_calendar coincide en algun dia se verifica sino continua con el siguiente
  for detail_calendar in details_calendar:
    make_detail_calendar = False
    for day in days:
      if(switch_dia(detail_calendar.date.strftime('%A')) == day.name_day):
        make_detail_calendar = True
        break
    if (not make_detail_calendar):
      continue
    # Se valida que no existan turnos futuros ocupados
    turns = Turn.objects.filter(enabled=True, detail_calendar = detail_calendar, end_time_turn__range = (start_time, end_time) )
    for turn in turns:
      if (turn.state_turn.state_turn == 'Ocupado'):
        errors.update({f'turn {turn.id_turn}':f'Para poder continuar debe reprogramar el turno {turn.start_time_turn} - {turn.end_time_turn}'}) 
  return errors


def validate_interposed_schedule(self,data):
  id = self.instance.id_schedule
  start_time = data.get('start_time_schedule')
  end_time = data.get('end_time_schedule')
  days = data.get('days')
  calendar = data.get('calendar')
  
  errors = {}
  
  schedules = Schedule.objects.filter(enabled = True, calendar = calendar).exclude(id_schedule = id)
  for schedule in schedules:
    # Si el schedule coincide en algun dia se verifica sino continua con el siguiente
    make_schedule = False
    for day in schedule.days.all():
      if (day in days):
        make_schedule = True
        break
    if (not make_schedule):
      continue
    # Validar que los horarios no se interponen
    if ((start_time == schedule.start_time_schedule) or (start_time < schedule.start_time_schedule and end_time > schedule.start_time_schedule) or (start_time > schedule.start_time_schedule and start_time < schedule.end_time_schedule)):
      errors.update({f'schedule {schedule.id_schedule}':f'Se interpone con el horario {schedule.start_time_schedule} - {schedule.end_time_schedule}'})
  return errors


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


def trows_error(errors):
  raise serializers.ValidationError(errors)