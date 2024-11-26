from rest_framework import serializers
from AppParking.models import *


class ParqueaderoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parqueadero
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    parqueadero = ParqueaderoSerializer(read_only=True)
    parqueadero_id = serializers.PrimaryKeyRelatedField(write_only=True,allow_null=True,queryset=Parqueadero.objects.all(),source='parqueadero')
    class Meta:
        model = Usuario
        fields = '__all__'
    def create(self, validated_data):
        user = Usuario(
            email=validated_data['email'],
            username=validated_data['username'],
            parqueadero=validated_data['parqueadero'],
            direccion=validated_data['direccion'],
            telefono=validated_data['telefono'],
            is_staff=validated_data['is_staff'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return  user

class TarifaSerializer(serializers.ModelSerializer):
    parqueadero = ParqueaderoSerializer(read_only=True)
    parqueadero_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Parqueadero.objects.all(),source='parqueadero')
    class Meta:
        model = Tarifa
        fields = '__all__'

class PropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propietario
        fields = ['id','identificacion']

class VehiculoSerializer(serializers.ModelSerializer):
    parqueadero = ParqueaderoSerializer(read_only=True)
    parqueadero_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Parqueadero.objects.all(),source='parqueadero')
    propietario = PropietarioSerializer(read_only=True)
    propietario_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Propietario.objects.all(),source='propietario')
    class Meta:
        model = Vehiculo
        fields = '__all__'

class EntradaSalidaSerializer(serializers.ModelSerializer):
    tarifa = TarifaSerializer(read_only=True)
    tarifa_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Tarifa.objects.all(),
                                                        source='tarifa')
    vehiculo = VehiculoSerializer(read_only=True)
    vehiculo_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Vehiculo.objects.all(),
                                                        source='vehiculo')
    usuario = UsuarioSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Usuario.objects.all(),
                                                        source='usuario')
    class Meta:
        model = EntradaSalida
        fields = '__all__'

class EntradaSalidaSerializer(serializers.ModelSerializer):
    tarifa = TarifaSerializer(read_only=True)
    tarifa_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Tarifa.objects.all(), source='tarifa')
    vehiculo = VehiculoSerializer(read_only=True)
    vehiculo_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Vehiculo.objects.all(), source='vehiculo')
    usuario = UsuarioSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Usuario.objects.all(), source='usuario')

class Meta:
        model = EntradaSalida
        fields = '__all__'

def create(self, validated_data):
        entrada_salida = EntradaSalida(**validated_data)
        entrada_salida.clean()  # Ejecutar las validaciones del modelo
        entrada_salida.save()
        return entrada_salida

def update(self, instance, validated_data):
        # Permitir solo la actualización de la hora de salida y el cálculo del total
        instance.hora_salida = validated_data.get('hora_salida', instance.hora_salida)
        instance.calcular_total()
        instance.save()
        return instance
    
class ReporteOcupacionSerializer(serializers.Serializer):
    capacidad_total = serializers.IntegerField()
    vehiculos_estacionados = serializers.IntegerField()
    espacios_libres = serializers.IntegerField()
    porcentaje_ocupacion = serializers.FloatField()