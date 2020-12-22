from rest_framework.response import Response
from rest_framework import status, generics

from ..models.schedule_model import Schedule
from ..serializers.schedule_serializer import ScheduleSerializer


class ScheduleList(generics.ListCreateAPIView):
    queryset = Schedule.objects.filter(enabled = True)
    serializer_class = ScheduleSerializer
    http_method_names = ['get', 'post']


class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.filter(enabled = True)
    serializer_class = ScheduleSerializer
    http_method_names = ['get', 'delete']
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Validar que se puede eliminar en caso contrario lanza errores
        serializer = self.get_serializer(instance)
        serializer.validate_delete(instance)
        instance.enabled = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)