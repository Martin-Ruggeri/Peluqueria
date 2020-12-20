from rest_framework import serializers
from datetime import datetime
from ..models.schedule_model import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
  
  def validate(self, data):
    start_time = datetime.strptime(self.initial_data.get('start_time_schedule'), '%H:%M')
    end_time = datetime.strptime(self.initial_data.get('end_time_schedule'), '%H:%M')
    interval_turn = int(self.initial_data.get('interval_turn'))
    
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
    fields = ['id_schedule', 'start_time_schedule', 'end_time_schedule', 'interval_turn', 'calendar']