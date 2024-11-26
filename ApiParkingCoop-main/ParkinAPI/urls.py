from django.urls import path, include
from rest_framework import routers
from AppParking.views import *

router = routers.DefaultRouter()
router.register('parqueadero',ParqueaderoView)
router.register('usuario',UsuarioView)
router.register('tarifa',TarifaView)
router.register('propietario',PropietarioView,basename='propietario')
router.register('vehiculo',VehiculoView)
router.register('entradasalida',EntradaSalidaView)
router.register(r'entradas-salidas', EntradaSalidaView, basename='entradas-salidas')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', AuthTokenView.as_view() ),
    path('parqueaderos/<int:parqueadero_id>/reporte-ocupacion/', ReporteOcupacionView.as_view(), name='reporte-ocupacion'),
    path('propietariobyedad', PropietarioByEdad.as_view())
]
