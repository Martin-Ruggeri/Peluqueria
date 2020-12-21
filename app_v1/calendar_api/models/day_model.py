from django.db import models

class Day(models.Model):
  id_day = models.AutoField(primary_key=True)
  name_day = models.CharField(max_length=10, unique=True)
  
  created = models.DateTimeField(auto_now_add=True)
  up_date = models.DateTimeField(auto_now=True)
  enabled = models.BooleanField(default=True)
  
  class Meta:
    verbose_name = "Dia"
    ordering = ['-created']
  
  def __str__(self):
    return self.name_day