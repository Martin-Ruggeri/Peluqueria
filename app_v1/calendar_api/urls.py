from django.urls import path

from .views import schedule_views, turn_views


urlpatterns = [
    
    # SCHEDULE
    path('prueba', schedule_views.ScheduleList.as_view()),
    path('prueba/<int:pk>', schedule_views.ScheduleDetail.as_view()),
    
    # TURN
]