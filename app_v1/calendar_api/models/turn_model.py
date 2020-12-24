from django.db import models
from .detail_calendar_model import DetailCalendar
from .state_turn_model import StateTurn

class Turn(models.Model):
  id_turn = models.AutoField(primary_key=True)
  start_time_turn = models.TimeField()
  end_time_turn = models.TimeField()
  
  detail_calendar = models.ForeignKey(DetailCalendar, on_delete=models.PROTECT)
  state_turn = models.ForeignKey(StateTurn, on_delete=models.PROTECT)
  
  created = models.DateTimeField(auto_now_add=True)
  up_date = models.DateTimeField(auto_now=True)
  enabled = models.BooleanField(default=True)
  
  class Meta:
    verbose_name = "Turno"
    ordering = ['detail_calendar' , 'start_time_turn']
  
  def __str__(self):
    return f"{self.id_turn} - {self.detail_calendar} -> {self.start_time_turn} - {self.end_time_turn} -> {self.state_turn}"