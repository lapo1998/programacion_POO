# programa para calculara el area de uno o varios círculo

# En este programa solicita al usuario el radio de un círculo y calcula
#  su área. Muestra el uso de diferentes tipos de datos (float,
#   string, boolean, integer) y tambien sigue la convención snake_case.
#   Es un ejemplo sencillo, pero muestra cómo usamos diferentes tipos de datos
#   (como números y texto) de forma ordenada.

# Importamos el módulo 'math' para acceder al valor de la constante pi.
import math
PI_CONSTANTE = math.pi

# Funciones y variables: snake_case la función calcula el área de un círculo.
def calcular_area_circulo(radio_circulo):
    # -aplicamos Identificador descriptivo siguiendo la convención snake_case: radio_circulo
    # - Tipo de dato: 'radio_circulo' es un float.
    # - Tambien usamos Identificador descriptivo siguiendo la convención snake_case: area_calculada
    area_calculada = PI_CONSTANTE * (radio_circulo ** 2)
    return area_calculada

# Función principal para la lógica del programa.
def main():
    # - Identificador descriptivo siguiendo la convención snake_case: 'mensaje_bienvenida'
    # - Tipo de dato: 'mensaje_bienvenida' es una variable de tipo string.
    mensaje_bienvenida = "Este programa calcula el área de un círculo."
    print(mensaje_bienvenida)

    # Aca aplicamos
    # - Identificador descriptivo siguiendo la convención snake_case: 'programa_activo'
    # - Tipo de dato: 'programa_activo' es una variable booleana.
    programa_activo = True

    while programa_activo:
        try:
            # - Identificador descriptivo siguiendo la convención snake_case: 'entrada_usuario'
            # - Tipo de dato: La entrada del usuario es un string.
            entrada_usuario = input("\nIngresa el radio del círculo (o 'salir'): ")

            # Verificamos si el usuario quiere salir.
            if entrada_usuario.lower() == 'salir':
                # En esta línea aplicamos el tipo de dato: boolean, al cambiar el valor de 'programa_activo'.
                programa_activo = False
                # Mensaje de despedida un mensaje bastante comun.
                print("¡Hasta luego nos volveremos aver!")
                continue
            # - Identificador descriptivo siguiendo la convención snake_case: 'radio_ingresado'
            # - Tipo de dato: float, al convertir el string a número.
            radio_ingresado = float(entrada_usuario)

            # - Identificador descriptivo siguiendo la convención snake_case: 'es_radio_valido'
            # - Tipo de dato: 'es_radio_valido' es una variable booleana.
            es_radio_valido = radio_ingresado > 0

            if es_radio_valido:
                # - aplicamos Identificador descriptivo siguiendo la convención snake_case: 'area_del_circulo'
                # - Tipo de dato: El resultado de la función es un float.
                area_del_circulo = calcular_area_circulo(radio_ingresado)
                radio_entero = int(radio_ingresado)

                # En esta línea aplicamos el tipo de dato string para formatear el resultado.
                print(f"Radio ingresado: {radio_ingresado} (aprox. {radio_entero})")
                print(f"Área calculada: {area_del_circulo:.4f}")
            else:
                print("El radio debe ser un número positivo.")

        except ValueError:
            # aplicamos el tipo de dato string.
            print("Entrada no válida. Por favor, ingresa un número o 'salir'.")

# Por ultimo realizamos la ejecion del programa
if __name__ == "__main__":
    main()