from rest_framework.response import Response
from rest_framework import status, generics
from datetime import date, timedelta

from app_v1.response import response
from ..models.turn_model import Turn
from ..models.state_turn_model import StateTurn
from ..models.detail_calendar_model import DetailCalendar
from ..serializers.turn_serializer import TurnSerializer


class TurnList(generics.ListAPIView):
    queryset = Turn.objects.filter(enabled = True)
    serializer_class = TurnSerializer
    http_method_names = ['get']
    
    def get(self, request, *args, **kwargs):
        errors = {}
        try:
            detail_calendar = DetailCalendar.objects.get(date=kwargs["date"])
            state = StateTurn.objects.get(state_turn='Libre')
            self.queryset = Turn.objects.filter(enabled = True, state_turn = state, detail_calendar = detail_calendar)
            resultado = self.list(request, *args, **kwargs)
            return Response(status=status.HTTP_200_OK, data = response(result = resultado.data))
        except DetailCalendar.DoesNotExist:     
            # Entrará aqui cuando no exista ningun elemento que coincida con la busqueda
            return Response(status=status.HTTP_200_OK, data = response(result = []))
        except DetailCalendar.MultipleObjectsReturned:
            # Entrará aqui cuando se haya encontrado más de un objeto que coincida
            errors.update({f'system':f'Existe mas de un detalle para el dia {kwargs["date"].strftime("%d-%m-%Y")}'})
            return Response(status=status.HTTP_409_CONFLICT, data = response(error = errors))


class TurnDetail(generics.RetrieveUpdateAPIView):
    queryset = Turn.objects.filter(enabled = True)
    serializer_class = TurnSerializer
    http_method_names = ['get']
    
    def get(self, request, *args, **kwargs):
        resultado = self.retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data = response(result = resultado.data))


class TurnRequest(generics.RetrieveUpdateAPIView):
    queryset = Turn.objects.filter(enabled = True)
    serializer_class = TurnSerializer
    http_method_names = ['put']
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        errors = serializer.validate_request_turn(request.data)
        if (len(errors) > 0):
            return Response(status=status.HTTP_400_BAD_REQUEST, data = response(error = errors))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        
        return Response(status=status.HTTP_200_OK, data = response(result = serializer.data))


class TurnCancel(generics.RetrieveUpdateAPIView):
    queryset = Turn.objects.filter(enabled = True)
    serializer_class = TurnSerializer
    http_method_names = ['put']
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        errors = serializer.validate_cancel_turn(request.data)
        if (len(errors) > 0):
            return Response(status=status.HTTP_400_BAD_REQUEST, data = response(error = errors))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        
        return Response(status=status.HTTP_200_OK, data = response(result = serializer.data))
