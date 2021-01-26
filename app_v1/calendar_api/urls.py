from django.urls import path, register_converter
from datetime import date, datetime, timedelta

from .views import schedule_views, turn_views

class DateConverter:
    regex = '\d{2}-\d{2}-\d{4}'
    
    def to_python(self, value):
        return datetime.strptime(value, '%d-%m-%Y')
    
    def to_url(self, value):
        return value

register_converter(DateConverter, 'fecha')

urlpatterns = [
    
    # SCHEDULE
    path('schedule', schedule_views.ScheduleList.as_view()),
    path('scheule/<int:pk>', schedule_views.ScheduleDetail.as_view()),
    
    # TURN
    path('turn/<fecha:date>', turn_views.TurnList.as_view()),           # Lista de turnos disponibles en la fecha pasada por URL
    path('turn/<int:pk>', turn_views.TurnDetail.as_view()),             # Detalle del turno pasado por URL
    path('request-turn/<int:pk>', turn_views.TurnRequest.as_view()),    # Solicitar turno (Cambia de estado Libre a Ocupado)
    path('cancel-turn/<int:pk>', turn_views.TurnCancel.as_view()),      # Cancelar turno (Cambia de estado Ocupado a Libre)
]