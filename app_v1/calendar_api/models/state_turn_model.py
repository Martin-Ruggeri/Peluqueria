from django.db import models

class StateTurn(models.Model):
  id_state_turn = models.AutoField(primary_key=True)
  state_turn = models.CharField(max_length=100)
  
  created = models.DateTimeField(auto_now_add=True)
  up_date = models.DateTimeField(auto_now=True)
  enabled = models.BooleanField(default=True)
  
  class Meta:
    verbose_name = "Estado Turno"
    ordering = ['-created']
  
  def __str__(self):
    return self.state_turn