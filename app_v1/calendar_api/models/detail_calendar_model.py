from django.db import models
from calendar_model import Calendar

class DetailCalendar(models.Model):
  id_detail_calendar = models.AutoField(primary_key=True)
  date = models.DateField()
  
  calendar = models.ForeignKey(Calendar, on_delete=models.PROTECT)
  
  created = models.DateTimeField(auto_now_add=True)
  up_date = models.DateTimeField(auto_now=True)
  enabled = models.BooleanField(default=True)
  
  class Meta:
    verbose_name = "Detalle Agenda"
    ordering = ['-created']
  
  def __str__(self):
    return self.date