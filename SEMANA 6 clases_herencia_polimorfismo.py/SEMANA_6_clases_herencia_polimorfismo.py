import time
import random

class Sensor:
    """
    Clase que representa un sensor de datos, demostrando el uso de constructores y destructores.
    El constructor inicializa el sensor y el destructor simula su desactivación/liberación de recursos.
    """

    def __init__(self, id_sensor, tipo, unidad, valor_inicial=0.0):
        """
        Constructor de la clase Sensor.
        Este método se llama automáticamente cuando se crea una nueva instancia de Sensor.
        Su propósito es inicializar los atributos del objeto y ponerlo en un estado válido.

        Args:
            id_sensor (int o str): Un identificador único para el sensor.
            tipo (str): El tipo de sensor (ej. "Temperatura", "Humedad").
            unidad (str): La unidad de medida del sensor (ej. "°C", "% HR").
            valor_inicial (float, opcional): El valor inicial del sensor. Por defecto es 0.0.

        Raises:
            ValueError: Si alguno de los parámetros de entrada es inválido.
        """
        # --- Inicialización y Validación de Atributos ---
        # Es CRÍTICO inicializar todos los atributos que se usarán en __del__
        # ANTES de cualquier lógica que pueda fallar o lanzar una excepción.
        self.id_sensor = None # Inicializar a None o un valor seguro
        self.tipo = None
        self.unidad = None
        self.valor_actual = 0.0
        self.activo = False # Inicializar a False por seguridad

        try:
            # Validar el ID del sensor
            if not isinstance(id_sensor, (int, str)) or not id_sensor:
                raise ValueError("El ID del sensor debe ser un número o una cadena no vacía.")
            self.id_sensor = id_sensor

            # Validar el tipo de sensor
            if not isinstance(tipo, str) or not tipo.strip():
                raise ValueError("El tipo de sensor no puede estar vacío.")
            self.tipo = tipo.strip()

            # Validar la unidad de medida
            if not isinstance(unidad, str) or not unidad.strip():
                raise ValueError("La unidad de medida no puede estar vacía.")
            self.unidad = unidad.strip()

            # Validar el valor inicial
            if not isinstance(valor_inicial, (int, float)):
                raise ValueError("El valor inicial debe ser un número.")
            self.valor_actual = float(valor_inicial)

            self.activo = True # Si todo va bien, el sensor se activa

            # Mensaje del constructor para demostrar su activación
            print(f"\n[CONSTRUCTOR] Sensor '{self.id_sensor}' ({self.tipo} en {self.unidad}) inicializado. Valor inicial: {self.valor_actual:.2f}{self.unidad}")

        except ValueError as e:
            # Si hay un error en la inicialización, es mejor dejar 'activo' en False
            # y tal vez loggear el error o relanzarlo después de un mensaje claro.
            print(f"\n[CONSTRUCTOR ERROR] No se pudo inicializar el sensor: {e}")
            self.activo = False # Asegurarse de que el sensor no se marque como activo si falla
            self.id_sensor = id_sensor # Mantener el ID para el destructor si es posible, si no, se queda en None
            # No relanzar la excepción aquí si se quiere que el programa continúe,
            # pero el objeto quedará en un estado no completamente inicializado.
            # En la demostración principal, se captura el ValueError.

    def leer_valor(self):
        """
        Simula la lectura del valor actual del sensor.
        Solo permite la lectura si el sensor está activo.
        """
        if self.activo:
            # Simulación de una lectura real: pequeño retraso y variación aleatoria
            time.sleep(0.05)
            delta = (random.random() - 0.5) * 0.5
            self.valor_actual = round(self.valor_actual + delta, 2)
            print(f"[*] Sensor '{self.id_sensor}' ({self.tipo}): Leyendo valor -> {self.valor_actual:.2f}{self.unidad}")
            return self.valor_actual
        else:
            print(f"[!] Sensor '{self.id_sensor}' está inactivo. No se puede leer el valor.")
            return None

    def actualizar_valor(self, nuevo_valor):
        """
        Actualiza el valor del sensor a un nuevo valor específico de forma manual.
        Solo permite la actualización si el sensor está activo.
        """
        if self.activo:
            if not isinstance(nuevo_valor, (int, float)):
                print(f"[!] Valor inválido para actualizar el sensor '{self.id_sensor}'.")
                return
            self.valor_actual = float(nuevo_valor)
            print(f"[*] Sensor '{self.id_sensor}' ({self.tipo}): Valor actualizado manualmente a {self.valor_actual:.2f}{self.unidad}")
        else:
            print(f"[!] Sensor '{self.id_sensor}' está inactivo. No se puede actualizar el valor.")

    def desactivar(self):
        """
        Método público para desactivar el sensor manualmente (simulando un apagado).
        Esto es diferente de la llamada automática al destructor.
        """
        if self.activo:
            self.activo = False
            print(f"[ACCIÓN MANUAL] Sensor '{self.id_sensor}' ({self.tipo}) ha sido DESACTIVADO manualmente.")
        else:
            print(f"[ACCIÓN MANUAL] Sensor '{self.id_sensor}' ({self.tipo}) ya está inactivo.")

    def __del__(self):
        """
        Destructor de la clase Sensor.
        Este método se invoca cuando no quedan referencias al objeto Sensor y el recolector de basura
        de Python está a punto de eliminarlo de la memoria. Su propósito es realizar cualquier
        "limpieza" o liberación de recursos asociados al objeto.

        En este caso, simula la desconexión o desactivación final del sensor.
        Se usa hasattr() para verificar la existencia de atributos antes de acceder a ellos,
        previniendo AttributeErrors durante la fase de cierre del programa.
        """
        # Es crucial usar hasattr() en __del__ porque los atributos pueden ya no existir
        # si el objeto se está destruyendo durante el cierre del intérprete o si __init__ falló.
        if hasattr(self, 'activo') and self.activo:
            self.activo = False
            # Intentar acceder a otros atributos como self.id_sensor o self.tipo también
            # debería ser protegido con hasattr() si hay riesgo de que no existan.
            # Sin embargo, id_sensor y tipo se inicializan a None al principio del constructor,
            # lo que ayuda a mitigar ese riesgo.
            sensor_id_msg = getattr(self, 'id_sensor', 'ID desconocido')
            sensor_tipo_msg = getattr(self, 'tipo', 'Tipo desconocido')
            print(f"[DESTRUCTOR] Sensor '{sensor_id_msg}' ({sensor_tipo_msg}) ha sido DESACTIVADO y sus recursos liberados.")
        elif hasattr(self, 'id_sensor'): # Si no estaba activo pero tiene ID, dar un mensaje alternativo
            sensor_id_msg = getattr(self, 'id_sensor', 'ID desconocido')
            sensor_tipo_msg = getattr(self, 'tipo', 'Tipo desconocido')
            print(f"[DESTRUCTOR] Sensor '{sensor_id_msg}' ({sensor_tipo_msg}) ya estaba inactivo o no pudo ser inicializado.")
        else: # Si ni siquiera tiene ID (muy raro, indica fallo grave en init)
            print("[DESTRUCTOR] Un objeto Sensor incompleto ha sido destruido.")

# --- Bloque Principal de Demostración ---
if __name__ == "__main__":
    print("--- INICIO DE LA DEMOSTRACIÓN DE CONSTRUCTORES Y DESTRUCTORES DE SENSORES ---")
    print("----------------------------------------------------------------------")

    # --- DEMOSTRACIÓN 1: Creación y uso normal de un sensor de Temperatura ---
    print("\n[DEMOSTRACIÓN 1] Sensor de Temperatura (Destructor implícito al final del programa):")
    try:
        temp_sensor_01 = Sensor(id_sensor="T_001", tipo="Temperatura", unidad="°C", valor_inicial=22.8)
        if temp_sensor_01.activo: # Solo operar si el constructor fue exitoso
            temp_sensor_01.leer_valor()
            temp_sensor_01.actualizar_valor(23.5)
            temp_sensor_01.leer_valor()
    except ValueError as e:
        print(f"ERROR: No se pudo crear el sensor de temperatura: {e}")

    # --- DEMOSTRACIÓN 2: Sensor de Humedad con eliminación explícita ---
    print("\n\n[DEMOSTRACIÓN 2] Sensor de Humedad (Destructor explícito con 'del'):")
    try:
        hum_sensor_01 = Sensor("H_002", "Humedad", "% HR", 65.0)
        if hum_sensor_01.activo: # Solo operar si el constructor fue exitoso
            hum_sensor_01.leer_valor()
            hum_sensor_01.leer_valor()
            print("\n--> Eliminando explícitamente el objeto 'hum_sensor_01' usando 'del'...")
            del hum_sensor_01
            print("--> Objeto 'hum_sensor_01' eliminado. Observa el mensaje del destructor arriba.")
    except ValueError as e:
        print(f"ERROR: No se pudo crear el sensor de humedad: {e}")

    # --- DEMOSTRACIÓN 3: Sensor con error en el constructor (validación) ---
    print("\n\n[DEMOSTRACIÓN 3] Intentando crear un sensor con ID inválido (manejo de errores):")
    error_sensor = None # Inicializar a None para evitar NameError si falla la creación
    try:
        error_sensor = Sensor(id_sensor="", tipo="Presión", unidad="hPa") # ID vacío
        if error_sensor.activo: # Si sorprendentemente se crea, intentar usarlo
            error_sensor.leer_valor()
    except ValueError as e:
        print(f"ERROR ESPERADO: No se pudo crear el sensor debido a un error de validación: {e}")
        # En este punto, 'error_sensor' puede ser un objeto parcial si la excepción se lanzó después
        # de que algunos atributos fueran definidos. El destructor lo manejará.

    # --- DEMOSTRACIÓN 4: Sensor desactivado manualmente antes de la destrucción ---
    print("\n\n[DEMOSTRACIÓN 4] Sensor de Luz (desactivado manualmente):")
    try:
        light_sensor_01 = Sensor("L_003", "Luz", "Lux", 500.0)
        if light_sensor_01.activo: # Solo operar si el constructor fue exitoso
            light_sensor_01.leer_valor()
            light_sensor_01.desactivar()
            light_sensor_01.leer_valor() # Intentamos leer un sensor inactivo
            print("\n--> El programa está a punto de finalizar. El destructor de 'light_sensor_01' se llamará, pero notará que ya estaba inactivo.")
    except ValueError as e:
        print(f"ERROR: No se pudo crear el sensor de luz: {e}")

    print("\n----------------------------------------------------------------------")
    print("--- FIN DE LA DEMOSTRACIÓN ---")

    time.sleep(0.5)