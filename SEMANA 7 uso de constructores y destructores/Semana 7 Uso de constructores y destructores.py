#  TEMA Manejo de Sensores de Datos

# manejo del ciclo de vida de objetos usando sensores de datos
# la función de este codigo es demostrar de manera clara y prácticamente cómo funcionan
# los constructores (__init__) y los destructores (__del__) en Python

import time  # Importa el módulo 'time' para usar time.sleep() y simular pausas en las lecturas del sensor.
import random  # Importa el módulo 'random' para generar valores aleatorios para la simulación de las lecturas.

# Define la clase Sensor. Representa un dispositivo de sensor de datos.
# Esta clase demuestra los conceptos de constructores y destructores en Python.
class Sensor:

    # Define el método constructor. Se ejecuta automáticamente al crear un nuevo objeto Sensor.
    # Su objetivo es inicializar todos los atributos del sensor y asegurar un estado válido.
    def __init__(self, id_sensor, tipo, unidad, valor_inicial=0.0):
        # Inicializa atributos críticos antes de la validación. Esto asegura que existan para el destructor,
        # incluso si la inicialización falla.
        self.id_sensor = None
        self.tipo = None
        self.unidad = None
        self.valor_actual = 0.0
        self.activo = False  # El sensor se considera inactivo hasta que la inicialización sea exitosa.

        try:
            # Validación del ID del sensor. Debe ser un número o una cadena no vacía.
            if not isinstance(id_sensor, (int, str)) or not id_sensor:
                raise ValueError("Error: ID de sensor inválido. Debe ser un número o una cadena no vacía.")
            self.id_sensor = id_sensor  # Asigna el ID validado al atributo del objeto.

            # Validación del tipo de sensor. No puede ser una cadena vacía.
            if not isinstance(tipo, str) or not tipo.strip():
                raise ValueError("Error: El tipo de sensor no puede estar vacío.")
            self.tipo = tipo.strip()  # Asigna el tipo validado, eliminando espacios en blanco extra.

            # Validación de la unidad de medida. No puede ser una cadena vacía.
            if not isinstance(unidad, str) or not unidad.strip():
                raise ValueError("Error: La unidad de medida no puede estar vacía.")
            self.unidad = unidad.strip()  # Asigna la unidad validada.

            # Validación del valor inicial. Debe ser un número (entero o flotante).
            if not isinstance(valor_inicial, (int, float)):
                raise ValueError("Error: El valor inicial debe ser numérico.")
            self.valor_actual = float(valor_inicial)  # Asigna y convierte el valor a flotante.

            self.activo = True  # Si todas las validaciones pasan, el sensor se marca como activo.

            # Imprime un mensaje indicando que el constructor se ha ejecutado exitosamente.
            print(
                f"\n[CONSTRUCTOR] Sensor '{self.id_sensor}' ({self.tipo}) inicializado. Valor: {self.valor_actual:.2f}{self.unidad}")

        except ValueError as e:
            # Captura cualquier ValueError lanzado durante la validación del constructor.
            print(f"\n[CONSTRUCTOR ERROR] Fallo al inicializar sensor '{id_sensor}': {e}")
            self.activo = False  # Asegura que el sensor no se marque como activo si la inicialización falla.
            self.id_sensor = id_sensor  # Intenta mantener el ID para el mensaje del destructor si es posible.

    # Define el método para leer el valor del sensor.
    # Simula una lectura real y devuelve el valor actual.
    def leer_valor(self):
        # Solo permite leer si el sensor está marcado como activo.
        if self.activo:
            time.sleep(0.05)  # Simula un pequeño retardo en la lectura.
            # Genera una pequeña variación aleatoria para simular fluctuaciones en la lectura.
            self.valor_actual = round(self.valor_actual + (random.random() - 0.5) * 0.5, 2)
            # Imprime el valor leído por el sensor.
            print(f"[*] Sensor '{self.id_sensor}' ({self.tipo}): Lectura -> {self.valor_actual:.2f}{self.unidad}")
            return self.valor_actual  # Devuelve el valor actual del sensor.
        else:
            # Mensaje si se intenta leer un sensor inactivo.
            print(f"[!] Sensor '{self.id_sensor}' inactivo. No se puede leer.")
            return None  # Devuelve None si el sensor no está activo.

    # Define el método para actualizar manualmente el valor del sensor.
    # Útil para establecer un valor específico para pruebas o configuraciones.
    def actualizar_valor(self, nuevo_valor):
        # Solo permite actualizar si el sensor está activo.
        if self.activo:
            # Valida que el nuevo valor sea numérico.
            if not isinstance(nuevo_valor, (int, float)):
                print(f"[!] Valor de actualización inválido. Debe ser numérico.")
                return
            self.valor_actual = float(nuevo_valor)  # Asigna el nuevo valor.
            # Imprime un mensaje confirmando la actualización.
            print(
                f"[*] Sensor '{self.id_sensor}' ({self.tipo}): Valor actualizado a {self.valor_actual:.2f}{self.unidad}")
        else:
            # Mensaje si se intenta actualizar un sensor inactivo.
            print(f"[!] Sensor '{self.id_sensor}' inactivo. No se puede actualizar.")

    # Define el método para desactivar el sensor manualmente.
    # Esto es una acción intencional del usuario, diferente de la destrucción automática.
    def desactivar(self):
        # Solo desactiva si el sensor ya estaba activo.
        if self.activo:
            self.activo = False  # Cambia el estado del sensor a inactivo.
            print(f"[ACCIÓN MANUAL] Sensor '{self.id_sensor}' ({self.tipo}) DESACTIVADO.")
        else:
            # Mensaje si se intenta desactivar un sensor ya inactivo.
            print(f"[ACCIÓN MANUAL] Sensor '{self.id_sensor}' ({self.tipo}) ya inactivo.")

    # Define el método destructor. Se ejecuta cuando el objeto Sensor es eliminado de la memoria.
    # Esto ocurre cuando no quedan referencias al objeto y el recolector de basura de Python lo procesa.
    # Su función es realizar cualquier tarea de limpieza final o liberar recursos.
    def __del__(self):
        # Es crucial usar 'hasattr()' para verificar la existencia de atributos.
        # Esto previene AttributeErrors si el objeto está incompleto (ej. el constructor falló)
        # o durante la fase de cierre del programa donde los atributos pueden ser limpiados prematuramente.

        # Si el atributo 'activo' existe Y el sensor estaba en estado activo.
        if hasattr(self, 'activo') and self.activo:
            self.activo = False  # Marca el sensor como inactivo como parte de la limpieza.
            # En una aplicación real, aquí se cerrarían conexiones de hardware, archivos, liberarían memoria, etc.
            # Usa 'getattr' para obtener el ID y tipo de forma segura, con valores por defecto si no existen.
            sensor_id_msg = getattr(self, 'id_sensor', 'ID desconocido')
            sensor_tipo_msg = getattr(self, 'tipo', 'Tipo desconocido')
            print(f"[DESTRUCTOR] Sensor '{sensor_id_msg}' ({sensor_tipo_msg}) DESACTIVADO y recursos liberados.")
        # Si el atributo 'activo' no existe o el sensor ya estaba inactivo, pero el 'id_sensor' existe.
        elif hasattr(self, 'id_sensor'):
            sensor_id_msg = getattr(self, 'id_sensor', 'ID desconocido')
            sensor_tipo_msg = getattr(self, 'tipo', 'Tipo desconocido')
            print(f"[DESTRUCTOR] Sensor '{sensor_id_msg}' ({sensor_tipo_msg}) ya estaba inactivo o incompleto.")
        # Si el objeto es tan incompleto que ni siquiera tiene un 'id_sensor'.
        else:
            print("[DESTRUCTOR] Objeto Sensor incompleto destruido (sin ID conocido).")


# --- Bloque Principal de Demostración ---
# Este código se ejecuta solo cuando el script se corre directamente (no cuando es importado).
if __name__ == "__main__":
    print("--- INICIO DEMOSTRACIÓN SENSORES ---")
    print("------------------------------------")

    # DEMO 1: Creación y uso normal de un sensor de Temperatura.
    # El destructor de 'temp_sensor_01' se ejecutará automáticamente cuando el programa finalice.
    print("\n[DEMO 1] Creación de Sensor de Temperatura:")
    try:
        # Crea una instancia de Sensor con ID, tipo, unidad y valor inicial.
        temp_sensor_01 = Sensor(id_sensor="T_001", tipo="Temperatura", unidad="°C", valor_inicial=22.8)
        # Solo opera con el sensor si su constructor fue exitoso y está activo.
        if temp_sensor_01.activo:
            temp_sensor_01.leer_valor()  # Llama al método para leer el valor del sensor.
            temp_sensor_01.actualizar_valor(23.5)  # Llama al método para actualizar su valor.
            temp_sensor_01.leer_valor()  # Lee el valor de nuevo para ver el cambio.
    except ValueError as e:
        # Captura y muestra errores específicos durante la creación del sensor.
        print(f"ERROR: Fallo al crear sensor de temperatura: {e}")

    # DEMO 2: Creación de un sensor de Humedad y su eliminación explícita.
    # Se usa 'del' para forzar que el destructor se active antes del fin del programa.
    print("\n\n[DEMO 2] Sensor de Humedad con Eliminación Explícita:")
    try:
        hum_sensor_01 = Sensor("H_002", "Humedad", "% HR", 65.0)
        if hum_sensor_01.activo:
            hum_sensor_01.leer_valor()  # Lee el valor del sensor de humedad.
            print("\n--> Eliminando explícitamente 'hum_sensor_01' usando 'del'...")
            del hum_sensor_01  # Reduce a cero las referencias al objeto, lo que puede disparar el __del__.
            print("--> Objeto 'hum_sensor_01' eliminado. Observa el mensaje del destructor arriba.")
            # Intentar acceder a 'hum_sensor_01' aquí causaría un NameError porque ya no existe.
    except ValueError as e:
        print(f"ERROR: Fallo al crear sensor de humedad: {e}")

    # DEMO 3: Intento de crear un sensor con un ID inválido.
    # Esto demuestra la validación de entrada del constructor y cómo maneja los errores.
    print("\n\n[DEMO 3] Creando Sensor con ID Inválido (falla en constructor):")
    error_sensor = None  # Inicializa la variable a None para evitar NameError si la creación falla.
    try:
        # Este intento de creación fallará debido a que el ID es una cadena vacía.
        error_sensor = Sensor(id_sensor="", tipo="Presión", unidad="hPa")
        # Si, por alguna razón, se creara y estuviera activo, intentaría usarlo.
        if error_sensor and error_sensor.activo:
            error_sensor.leer_valor()
    except ValueError as e:
        print(f"ERROR ESPERADO: {e}")
        # El destructor para 'error_sensor' (si se creó parcialmente) se ejecutará
        # de forma segura gracias a la protección con 'hasattr()'.

    # DEMO 4: Sensor desactivado manualmente antes de su destrucción.
    # Muestra cómo el destructor se comporta cuando el sensor ya ha sido puesto en estado inactivo.
    print("\n\n[DEMO 4] Sensor de Luz (desactivado manualmente):")
    try:
        light_sensor_01 = Sensor("L_003", "Luz", "Lux", 500.0)
        if light_sensor_01.activo:
            light_sensor_01.leer_valor()  # Lee el valor mientras está activo.
            light_sensor_01.desactivar()  # Desactiva el sensor usando el método definido.
            light_sensor_01.leer_valor()  # Intenta leer de nuevo; ahora debería indicar que está inactivo.
            print(
                "\n--> Programa a punto de finalizar. El destructor de 'light_sensor_01' se ejecutará, pero notará que ya fue desactivado manualmente.")
    except ValueError as e:
        print(f"ERROR: Fallo al crear sensor de luz: {e}")

    print("\n------------------------------------")
    print("--- FIN DEMOSTRACIÓN ---")

    time.sleep(0.5)  # Pequeña pausa para asegurar que todos los mensajes de la consola sean visibles antes de cerrar.