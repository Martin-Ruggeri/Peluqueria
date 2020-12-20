from rest_framework.response import Response
from rest_framework import status, generics

from ..models.schedule_model import Schedule
from ..serializers.schedule_serializer import ScheduleSerializer


class ScheduleList(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    http_method_names = ['get', 'post']


class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.enabled = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)