from rest_framework import serializers
from datetime import time, date, datetime

from ..models.turn_model import Turn
from ..models.state_turn_model import StateTurn

class TurnSerializer(serializers.ModelSerializer):
  
  def validate_request_turn(self,data):
    id = self.instance.id_turn
    turn = Turn.objects.get(id_turn=id)
    state_turn_initial = turn.state_turn.state_turn
    state_turn_final = StateTurn.objects.get(id_state_turn=data.get('state_turn')).state_turn
    
    errors = {}
    
    # Validar que el turno despues de actualizar sea ocupado
    if (state_turn_final != 'Ocupado'):
      errors.update({'state_turn':'El turno se debe cambiar a ocupado'})
    
    # Validar que el turno antes de actualizar este libre
    if (state_turn_initial != 'Libre'):
      errors.update({'state_turn':'El Turno seleccionado ya no esta disponible'})
    
    # Validar que la fecha del turno es futura
    if (turn.detail_calendar.date < date.today()):
      errors.update({'detail_calendar':'Seleccionar fecha actual o futura'})
    
    # Validar que la hora del turno es futura
    current_time = time.fromisoformat(datetime.today().strftime('%H:%M:%S'))
    if (turn.detail_calendar.date == date.today() and turn.start_time_turn < current_time):
      errors.update({'start_time_turn':'Seleccionar un turno futuro'})
    
    return errors
  
  
  def validate_cancel_turn(self,data):
    id = self.instance.id_turn
    turn = Turn.objects.get(id_turn=id)
    state_turn_initial = turn.state_turn.state_turn
    state_turn_final = StateTurn.objects.get(id_state_turn=data.get('state_turn')).state_turn
    
    errors = {}
    
    # Validar que el turno despues de actualizar sea libre
    if (state_turn_final != 'Libre'):
      errors.update({'state_turn':'El turno se debe cambiar a Libre'})
    
    # Validar que el turno antes de actualizar este ocupado
    if (state_turn_initial != 'Ocupado'):
      errors.update({'state_turn':'El Turno seleccionado no esta ocupado'})
    
    # Validar que la fecha del turno es futura
    if (turn.detail_calendar.date < date.today()):
      errors.update({'detail_calendar':'Seleccionar fecha actual o futura'})
    
    # Validar que la hora del turno es futura
    current_time = time.fromisoformat(datetime.today().strftime('%H:%M:%S'))
    if (turn.detail_calendar.date == date.today() and turn.start_time_turn < current_time):
      errors.update({'start_time_turn':'Seleccionar un turno futuro'})
    
    return errors
  
  class Meta:
    model = Turn
    fields = ['id_turn', 'start_time_turn','end_time_turn','state_turn','detail_calendar']
    read_only_fields = ('id_turn', 'start_time_turn','end_time_turn','detail_calendar')