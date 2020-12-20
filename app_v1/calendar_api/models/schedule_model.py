from django.db import models
from .calendar_model import Calendar

class Schedule(models.Model):
  id_schedule = models.AutoField(primary_key=True)
  start_time_schedule = models.TimeField()
  end_time_schedule = models.TimeField()
  interval_turn = models.IntegerField()
  
  calendar = models.ForeignKey(Calendar, on_delete=models.PROTECT)
  
  created = models.DateTimeField(auto_now_add=True)
  up_date = models.DateTimeField(auto_now=True)
  enabled = models.BooleanField(default=True)

    
  class Meta:
    verbose_name = "Horario"
    ordering = ['-created']
  
  def __str__(self):
    return f"{self.start_time_schedule} - {self.end_time_schedule}"