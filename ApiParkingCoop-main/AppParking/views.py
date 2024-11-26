from inspect import stack

from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Sum
from django.db.models import Count


from AppParking.serializers import *

# Create your views here.

class ParqueaderoView (viewsets.ModelViewSet):
    queryset = Parqueadero.objects.all()
    serializer_class = ParqueaderoSerializer
class UsuarioView (viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
class TarifaView (viewsets.ModelViewSet):
    queryset = Tarifa.objects.all()
    serializer_class = TarifaSerializer
class PropietarioView (viewsets.ModelViewSet):
    def get_queryset(self):
        an = self.request.query_params.get('an')
        edad = 2024 - int(an)
        queryset = Propietario.objects.filter(edad__gte=edad)
        return queryset
    serializer_class = PropietarioSerializer

class PropietarioByEdad(APIView):
    def post(self,request):
        try:
            data = request.data
            res = Propietario.objects.filter(edad__gte=int(data['edad']))
            respuesta = PropietarioSerializer(res,many=True)
            return Response(respuesta.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"mensaje":"Ocurrio un problema!!"+str(e)}, status=status.HTTP_502_BAD_GATEWAY)

class VehiculoView (viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
class EntradaSalidaView (viewsets.ModelViewSet):
    queryset = EntradaSalida.objects.all()
    serializer_class = EntradaSalidaSerializer
    
class EntradaSalidaView(viewsets.ModelViewSet):
    queryset = EntradaSalida.objects.all()
    serializer_class = EntradaSalidaSerializer
    
    @action(detail=False, methods=['post'], url_path='registrar-entrada')
    def registrar_entrada(self, request):
        """Registrar la entrada de un vehículo."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='registrar-salida')
    def registrar_salida(self, request, pk=None):
        """Registrar la salida de un vehículo."""
        try:
            entrada_salida = self.get_object()
            entrada_salida.hora_salida = datetime.now()
            entrada_salida.calcular_total()
            entrada_salida.save()
            return Response(self.get_serializer(entrada_salida).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='vehiculos-activos')
    def vehiculos_activos(self, request):
        """Obtener vehículos actualmente en el parqueadero."""
        activos = EntradaSalida.objects.filter(hora_salida__isnull=True)
        serializer = self.get_serializer(activos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='ingresos-generados')
    def ingresos_generados(self, request):
        """Calcular ingresos generados en un rango de fechas."""
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        ingresos = EntradaSalida.objects.filter(
            hora_salida__range=[fecha_inicio, fecha_fin]
        ).aggregate(Sum('total_a_pagar'))
        return Response({"ingresos_totales": ingresos['total_a_pagar__sum']}, status=status.HTTP_200_OK)
    
class AuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data =request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
class ReporteOcupacionView(APIView):
    def get(self, request, parqueadero_id):
        try:
            # Obtiene el parqueadero por ID
            parqueadero = Parqueadero.objects.get(id=parqueadero_id)
            
            # Contamos cuántos vehículos están estacionados en este parqueadero
            vehiculos_estacionados = Vehiculo.objects.filter(parqueadero=parqueadero).count()
            
            # Cálculo de los datos del reporte
            capacidad_total = parqueadero.capacidad_total
            espacios_libres = capacidad_total - vehiculos_estacionados
            porcentaje_ocupacion = (vehiculos_estacionados / capacidad_total) * 100 if capacidad_total > 0 else 0

            # Preparamos la respuesta
            data = {
                "capacidad_total": capacidad_total,
                "vehiculos_estacionados": vehiculos_estacionados,
                "espacios_libres": espacios_libres,
                "porcentaje_ocupacion": round(porcentaje_ocupacion, 2),
            }
            return Response(data, status=status.HTTP_200_OK)
        except Parqueadero.DoesNotExist:
            return Response({"error": "Parqueadero no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)