from rest_framework import serializers
from datetime import datetime
from ..models.schedule_model import Schedule
from ..models.calendar_model import Calendar
    
class ScheduleSerializer(serializers.ModelSerializer):
  
  def validate(self, data):
    start_time = data.get('start_time_schedule')
    end_time = data.get('end_time_schedule')
    interval_turn = data.get('interval_turn')
    
    validate_interposed_schedule(self,data)
    
    # Validar que hora inicio > hora fin
    if (start_time >= end_time):
      raise ValueError('La hora fin debe ser mayor a la hora inicio')
    
    # Validar que los turnos sean de al menos 15 minutos
    if (interval_turn < 14):
      raise ValueError('El intervalo de cada turno debe ser al menos de 15 minutos')
    
    if (self.context.get('request').method == 'POST'):
      # validate POST
      print ('POST')  
    
    if (self.context.get('request').method in ['PUT', 'PATCH']):
      # validate put o patch
      print ('PUT o PATCH')
    
    return data
  
  class Meta:
    model = Schedule
    fields = ['id_schedule', 'start_time_schedule', 'end_time_schedule', 'interval_turn', 'calendar', 'days']
    
    
  
def validate_turn_busy(self,data):
  print ('Val')
  
def validate_interposed_schedule(self,data):
  start_time = data.get('start_time_schedule')
  end_time = data.get('end_time_schedule')
  days = data.get('days')
  calendar = data.get('calendar')
  
  schedules = Schedule.objects.filter(calendar = calendar).exclude(start_time_schedule = start_time, end_time_schedule = end_time)
  for schedule in schedules:
    # Si el schedule coincide en algun dia se verifica sino continua con el siguiente
    make_schedule = False
    for day_2 in schedule.days.all():
      if (day_2 in days):
        make_schedule = True
        break
    if (not make_schedule):
      continue
    
    # Validar que los horarios no se interponen
    if ((start_time == schedule.start_time_schedule) or (start_time < schedule.start_time_schedule and end_time > schedule.start_time_schedule) or (start_time > schedule.start_time_schedule and start_time < schedule.end_time_schedule)):
      raise Exception(f'Se interpone con el horario {schedule.start_time_schedule} - {schedule.end_time_schedule}')