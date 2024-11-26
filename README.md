Registro de Entrada y Salida de Vehículos
Funcionalidad: Se implementa un sistema para registrar las entradas y salidas de vehículos en el parqueadero, facilitando la gestión y control del flujo vehicular.
Descripción:
•
**Registro de entrada:**
•
Al momento de ingresar un vehículo, se asocia con una tarifa específica dependiendo del tamaño del vehículo y el parqueadero correspondiente.
•
También se registra el usuario encargado del ingreso, garantizando trazabilidad en la operación.
•
Registro de salida:
•
Se calcula el tiempo transcurrido desde el momento de la entrada.
•
Con base en la tarifa asignada, se genera el costo total del servicio de parqueo.
Reporte de Ingresos por Vehículo
Funcionalidad: Generación de reportes que detallan los ingresos obtenidos por un vehículo específico dentro de un período determinado.
Descripción:
•
Permite filtrar transacciones basadas en un vehículo en particular.
•
Suma los ingresos generados a partir de las salidas registradas para el vehículo.
•
Presenta el ingreso total acumulado dentro del rango de fechas especificado.
Búsqueda de Propietarios Mayores de Cierta Edad
Funcionalidad: Facilita la identificación de propietarios que cumplen con una condición de edad mínima.
Descripción:
•
Recibe un valor de edad como parámetro de entrada.
•
Filtra y devuelve una lista de propietarios cuya edad es igual o mayor al valor proporcionado.
Relación entre Parqueaderos y Tarifas
Funcionalidad: Cada parqueadero tiene tarifas específicas asignadas en función del tamaño de los vehículos, permitiendo una administración personalizada de los costos.
Descripción:
•
Permite asociar tarifas particulares a un parqueadero específico.
•
Define precios diferenciados según el tamaño del vehículo (motos, autos, camionetas, etc.).
•
Garantiza que los costos estén correctamente ajustados al parqueadero correspondiente.
Reporte de Ocupación de un Parqueadero
Funcionalidad General: Se incorpora una herramienta para generar un reporte de ocupación en tiempo real de un parqueadero.
Descripción: El reporte incluye:
•
La capacidad total del parqueadero.
•
El número actual de vehículos estacionados.
•
La cantidad de espacios disponibles.
•
El porcentaje de ocupación, calculado con base en la relación entre los vehículos presentes y la capacidad total.
