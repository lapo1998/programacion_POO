# sistema básico de gestión universitaria.
#  este codigo mostramos o tratamos de informar:
# Definir qué es una Persona, un Estudiante, un Profesor y una Materia.
# Mostrar cómo los estudiantes y profesores heredan características de una Persona.
# Demostrar cómo diferentes tipos de usuarios (estudiantes, profesores) pueden mostrar
# su información de manera única, aunque se les pida hacerlo con el mismo comando.

# --- Clases: Planos para objetos ---

class Persona:
    # Base para individuos.
    def __init__(self, nombre, apellido, cedula):
        self._nombre = nombre  # Atributo protegido.
        self._apellido = apellido
        self._cedula = cedula

    # Obtiene nombre completo.
    def obtener_nombre_completo(self):
        return f"{self._nombre} {self._apellido}"

    # Info general. Será especializado (polimorfismo).
    def mostrar_datos(self):
        return f"Cédula: {self._cedula}, Nombre: {self.obtener_nombre_completo()}"


class Materia:
    # Clase de asignatura.
    def __init__(self, nombre, codigo, creditos):
        self._nombre = nombre
        self._codigo = codigo
        self._creditos = creditos
        self._docente_asignado = None # Asignado por método (encapsulación).

    # Nombre de materia.
    def obtener_nombre(self):
        return self._nombre

    # Código de materia.
    def obtener_codigo(self):
        return self._codigo

    # Créditos de materia.
    def obtener_creditos(self):
        return self._creditos

    # Asigna docente (encapsulación).
    def asignar_docente(self, docente):
        if isinstance(docente, Profesor):
            self._docente_asignado = docente
        else:
            print("ERROR: Solo objeto Profesor válido.")

    # Representación en texto.
    def __str__(self):
        return f"{self._nombre} ({self._codigo})"


class Estudiante(Persona):
    # Estudiante (hereda de Persona).
    def __init__(self, nombre, apellido, cedula, carrera):
        super().__init__(nombre, apellido, cedula) # Herencia.
        self._carrera = carrera
        self._materias_matriculadas = [] # Materias inscritas (encapsulación).
        self._calificaciones_por_materia = {} # Calificaciones (encapsulación).
        self._promedio_general = 0.0 # Calculado internamente (encapsulación).

    # Obtiene carrera.
    def obtener_carrera(self):
        return self._carrera

    # Obtiene promedio.
    def obtener_promedio_general(self):
        return self._promedio_general

    # Matricula materia (encapsulación).
    def matricular_materia(self, materia):
        if not isinstance(materia, Materia):
            print("ERROR: Solo se pueden matricular objetos de tipo Materia.")
            return

        if materia not in self._materias_matriculadas:
            self._materias_matriculadas.append(materia)
            self._calificaciones_por_materia[materia.obtener_codigo()] = []
            print(f"INFO: {self.obtener_nombre_completo()} matriculado en {materia.obtener_nombre()}.")
        else:
            print(f"INFO: {self.obtener_nombre_completo()} ya está matriculado en {materia.obtener_nombre()}.")

    # Registra calificación (encapsulación y actualización).
    def registrar_calificacion(self, codigo_materia, calificacion):
        if 0 <= calificacion <= 100:
            if codigo_materia in self._calificaciones_por_materia:
                self._calificaciones_por_materia[codigo_materia].append(calificacion)
                self._calcular_promedio_general() # Recalcula el promedio.
                print(f"INFO: Calificación {calificacion} registrada en {codigo_materia}.")
            else:
                print(f"ERROR: Estudiante no matriculado en {codigo_materia}.")
        else:
            print("ERROR: Calificación fuera de rango (0-100).")

    # Polimorfismo: Personaliza 'mostrar_datos'.
    def mostrar_datos(self):
        datos_base = super().mostrar_datos()
        materias_nombres = [m.obtener_nombre() for m in self._materias_matriculadas]
        materias_str = ", ".join(materias_nombres) if materias_nombres else "Ninguna"
        return (f"{datos_base}, Tipo: Estudiante, Carrera: {self._carrera}, "
                f"Materias: [{materias_str}], Promedio: {self.obtener_promedio_general():.2f}")

    # Método interno: Calcula promedio (encapsulación).
    def _calcular_promedio_general(self):
        total_puntos = 0
        total_creditos = 0
        for materia in self._materias_matriculadas:
            codigo = materia.obtener_codigo()
            creditos = materia.obtener_creditos()
            notas = self._calificaciones_por_materia.get(codigo, [])
            if notas:
                promedio_materia = sum(notas) / len(notas)
                total_puntos += promedio_materia * creditos
                total_creditos += creditos

        if total_creditos > 0:
            self._promedio_general = total_puntos / total_creditos
        else:
            self._promedio_general = 0.0


class Profesor(Persona):
    # Profesor (hereda de Persona).
    def __init__(self, nombre, apellido, cedula, departamento):
        super().__init__(nombre, apellido, cedula) # Herencia.
        self._departamento = departamento
        self._materias_impartidas = [] # Materias a cargo (encapsulación).

    # Obtiene departamento.
    def obtener_departamento(self):
        return self._departamento

    # Asigna materia a impartir (encapsulación).
    def impartir_materia(self, materia):
        if not isinstance(materia, Materia):
            print("ERROR: Solo objeto Materia válido.")
            return
        if materia not in self._materias_impartidas:
            self._materias_impartidas.append(materia)
            materia.asignar_docente(self) # Interacción de objetos.
            print(f"INFO: Docente {self.obtener_nombre_completo()} ahora imparte {materia.obtener_nombre()}.")

    # Polimorfismo: Personaliza 'mostrar_datos'.
    def mostrar_datos(self):
        datos_base = super().mostrar_datos()
        materias_nombres = [m.obtener_nombre() for m in self._materias_impartidas]
        materias_str = ", ".join(materias_nombres) if materias_nombres else "Ninguna"
        return (f"{datos_base}, Tipo: Profesor, Departamento: {self._departamento}, "
                f"Materias a cargo: [{materias_str}]")


# --- Bloque Principal: Demostración ---

if __name__ == "__main__":
    print("--- DEMO del Sistema Universitario (Ecuador) ---")

    # Creación de objetos.
    poo = Materia("Programación Orientada a Objetos", "POO101", 4)
    redes = Materia("Redes de Computadoras", "RED201", 5)
    calculo = Materia("Cálculo Integral", "CAL301", 5)

    elvio_lapo = Estudiante("Elvio", "Lapo", "1720000001", "Ingeniería en TICS")
    ing_diego_ramirez = Profesor("Diego", "Ramirez", "0910000002", "Ingeniería en TICS")

    print("\n--- Interacción y Encapsulación ---")
    # Docente imparte materias.
    ing_diego_ramirez.impartir_materia(poo)
    ing_diego_ramirez.impartir_materia(redes)

    # Estudiante matricula y registra notas.
    elvio_lapo.matricular_materia(poo)
    elvio_lapo.matricular_materia(redes)
    elvio_lapo.matricular_materia(calculo)

    elvio_lapo.registrar_calificacion("POO101", 90)
    elvio_lapo.registrar_calificacion("POO101", 85)
    elvio_lapo.registrar_calificacion("RED201", 78)
    elvio_lapo.registrar_calificacion("CAL301", 65)
    elvio_lapo.registrar_calificacion("ING001", 99) # Error esperado (materia no matriculada).
    elvio_lapo.registrar_calificacion("POO101", 105) # Error esperado (calificación fuera de rango).

    # Accede a promedio.
    print(f"\nPromedio de {elvio_lapo.obtener_nombre_completo()}: {elvio_lapo.obtener_promedio_general():.2f}")


    print("\n--- Herencia y Polimorfismo ---")
    # Lista de objetos relacionados por herencia.
    elementos_universitarios = [elvio_lapo, ing_diego_ramirez]

    for elemento in elementos_universitarios:
        # Polimorfismo: Cada objeto muestra sus datos de forma personalizada.
        print(elemento.mostrar_datos())
        print("-" * 60)

    # Polimorfismo extra: Objetos mixtos (incluye Materia).
    print("\n--- Polimorfismo Adicional ---")
    todos_los_elementos = [elvio_lapo, ing_diego_ramirez, poo, redes]
    for elemento in todos_los_elementos:
        if isinstance(elemento, Persona):
            print(f"Detalle Persona: {elemento.mostrar_datos()}")
        elif isinstance(elemento, Materia):
            print(f"Detalle Materia: {elemento}")
            if elemento._docente_asignado:
                print(f"  Docente asignado: {elemento._docente_asignado.obtener_nombre_completo()}")
        print("=" * 60)

    print("\n--- FIN de la DEMO ---")
