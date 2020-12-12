from django.db import models

class Calendar(models.Model):
  id_calendar = models.AutoField(primary_key=True)
  name_calendar = models.CharField(max_length=100, unique=True)
  
  created = models.DateTimeField(auto_now_add=True)
  up_date = models.DateTimeField(auto_now=True)
  enabled = models.BooleanField(default=True)
  
  class Meta:
    verbose_name = "Agenda"
    ordering = ['-created']
  
  def __str__(self):
    return self.name_calendar