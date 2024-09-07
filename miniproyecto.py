import csv

# Autor: Alejandro Ignacio Ortiz Ortega
# Fecha: 6 de septiembre de 2024
# Descripción: Programa para administrar la disponibilidad de horas de exámenes en un laboratorio médico,
#              permitiendo atender pacientes y agregar disponibilidad de exámenes.

"""
    *** Comentario sobre el manejo de disponibilidad y pacientes ***
    |----------------------------------------------------------------------------------------------------------------|
    |   Este programa carga dos archivos: disponibilidad.txt (contiene la disponibilidad de horas para cada examen)  |
    |   y pacientes.csv (contiene el listado de pacientes y los exámenes que requieren).                             |
    |                                                                                                                |
    |   Permite atender a los pacientes si existen suficientes horas disponibles para todos los exámenes requeridos, |
    |   así como agregar horas a la disponibilidad de uno o más exámenes.                                            |
    |----------------------------------------------------------------------------------------------------------------|


    *** Comentario sobre el flujo de instrucciones ***
    |----------------------------------------------------------------------------------------------------------------|
    |   El ciclo principal se repite hasta que se ingresa la instrucción 'stop'. Cada ciclo muestra la disponibilidad |
    |   de los exámenes y luego solicita una instrucción al usuario. El usuario puede elegir entre las siguientes     |
    |   acciones: atender [paciente], agregar [exámenes], o detener el programa.                                      |
    |----------------------------------------------------------------------------------------------------------------|
"""


# Función para cargar la disponibilidad de horas desde un archivo de texto
def cargar_disponibilidad(archivo_disponibilidad):
    """
    *** Comentario sobre el formato del archivo de disponibilidad ***
    |--------------------------------------------------------------------------------------------------------------|
    |   El archivo 'disponibilidad.txt' debe tener el formato 'examen horas' en cada línea, donde 'examen' es el    |
    |   nombre del examen y 'horas' es un número entero que representa la disponibilidad de horas para dicho examen.|
    |--------------------------------------------------------------------------------------------------------------|
    """
    disponibilidad = {}
    with open(archivo_disponibilidad, 'r') as file:
        for linea in file:
            examen, horas = linea.strip().split()
            disponibilidad[examen] = int(horas)
    return disponibilidad


# Función para cargar los pacientes y los exámenes que requieren desde un archivo CSV
def cargar_pacientes(archivo_pacientes):
    """
    *** Comentario sobre el archivo de pacientes ***
    |----------------------------------------------------------------------------------------------------------------|
    |   El archivo 'pacientes.csv' contiene una lista de pacientes y los exámenes que requieren, separados por comas. |
    |   El programa almacena esta información en un diccionario donde la llave es el nombre del paciente y el valor  |
    |   es una lista de exámenes requeridos.                                                                          |
    |----------------------------------------------------------------------------------------------------------------|
    """
    pacientes = {}
    with open(archivo_pacientes, newline='') as file:
        reader = csv.reader(file)
        for fila in reader:
            nombre_paciente = fila[0]
            exámenes = fila[1:]
            pacientes[nombre_paciente] = exámenes
    return pacientes


# Función para atender a un paciente
def atender_paciente(paciente, disponibilidad, pacientes, archivo_disponibilidad):
    """
    *** Comentario sobre la función de atender pacientes ***
    |----------------------------------------------------------------------------------------------------------------|
    |   Esta función verifica si hay horas disponibles para todos los exámenes que requiere el paciente.              |
    |   Si es posible atenderlo, se descuentan las horas del diccionario de disponibilidad y se actualiza el archivo. |
    |   Si no hay suficientes horas para algún examen, se imprime un mensaje indicando el problema.                   |
    |----------------------------------------------------------------------------------------------------------------|
    """
    if paciente not in pacientes:
        print(f"El paciente {paciente} no está registrado.")
        return

    exámenes_requeridos = pacientes[paciente]
    for examen in exámenes_requeridos:
        if disponibilidad.get(examen, 0) <= 0:
            print(f"No es posible atender a {paciente} porque no existen horas disponibles para el examen {examen}.")
            return

    for examen in exámenes_requeridos:
        disponibilidad[examen] -= 1

    print(f"Se ha atendido con éxito a {paciente}!")
    imprimir_disponibilidad(disponibilidad)

    actualizar_disponibilidad(archivo_disponibilidad, disponibilidad)


# Función para agregar disponibilidad de horas para uno o más exámenes
def agregar_disponibilidad(exámenes, disponibilidad, archivo_disponibilidad):
    """
    *** Comentario sobre la función de agregar disponibilidad ***
    |----------------------------------------------------------------------------------------------------------------|
    |   Esta función permite aumentar la disponibilidad de horas de uno o más exámenes. Los nombres de los exámenes   |
    |   se reciben como una lista y se actualizan en el diccionario de disponibilidad.                                |
    |----------------------------------------------------------------------------------------------------------------|
    """
    for examen in exámenes:
        if examen in disponibilidad:
            disponibilidad[examen] += 1
        else:
            disponibilidad[examen] = 1
    imprimir_disponibilidad(disponibilidad)
    actualizar_disponibilidad(archivo_disponibilidad, disponibilidad)


# Función para mostrar la disponibilidad actual de horas por examen
def imprimir_disponibilidad(disponibilidad):
    """
    *** Comentario sobre la función de imprimir disponibilidad ***
    |----------------------------------------------------------------------------------------------------------------|
    |   Esta función recorre el diccionario de disponibilidad y muestra las horas disponibles para cada examen.       |
    |   El nombre del examen se imprime en mayúsculas seguido de la cantidad de horas disponibles.                    |
    |----------------------------------------------------------------------------------------------------------------|
    """
    for examen, horas in disponibilidad.items():
        print(f"{examen.upper()}: {horas}")


# Función principal que controla el ciclo de instrucciones
def ciclo_principal(disponibilidad, pacientes, archivo_disponibilidad):
    """
    *** Comentario sobre el ciclo principal ***
    |----------------------------------------------------------------------------------------------------------------|
    |   En cada iteración del ciclo, se muestra la disponibilidad de exámenes y se solicita una instrucción.          |
    |   El usuario puede elegir entre atender a un paciente, agregar disponibilidad o detener el programa.            |
    |----------------------------------------------------------------------------------------------------------------|
    """
    while True:
        imprimir_disponibilidad(disponibilidad)
        instrucción = input("Bienvenido, ingrese la instrucción a continuación: ").strip().lower()

        if instrucción.startswith("atender"):
            _, paciente = instrucción.split()
            atender_paciente(paciente.capitalize(), disponibilidad, pacientes, archivo_disponibilidad)

        elif instrucción.startswith("agregar"):
            exámenes = instrucción.split()[1:]
            agregar_disponibilidad(exámenes, disponibilidad, archivo_disponibilidad)

        elif instrucción == "stop":
            print("Programa detenido.")
            break

        else:
            print("Instrucción no válida. Intente de nuevo.")


# Función para actualizar el archivo de disponibilidad
def actualizar_disponibilidad(archivo_disponibilidad, disponibilidad):
    """
    *** Comentario sobre la actualización del archivo de disponibilidad ***
    |----------------------------------------------------------------------------------------------------------------|
    |   Esta función escribe los cambios en el archivo 'disponibilidad.txt'. Cada examen y su cantidad de horas se    |
    |   escriben en una línea separada del archivo, manteniendo el formato original.                                  |
    |----------------------------------------------------------------------------------------------------------------|
    """
    with open(archivo_disponibilidad, 'w') as file:
        for examen, horas in disponibilidad.items():
            file.write(f"{examen} {horas}\n")


# Función para actualizar el archivo de pacientes (aunque no se modifica en este programa)
def actualizar_pacientes(archivo_pacientes, pacientes):
    """
    *** Comentario sobre la actualización del archivo de pacientes ***
    |----------------------------------------------------------------------------------------------------------------|
    |   Aunque este programa no modifica el archivo de pacientes, esta función permite actualizar el archivo          |
    |   'pacientes.csv' si fuera necesario en futuras expansiones del programa.                                       |
    |----------------------------------------------------------------------------------------------------------------|
    """
    with open(archivo_pacientes, 'w', newline='') as file:
        writer = csv.writer(file)
        for paciente, exámenes in pacientes.items():
            writer.writerow([paciente] + exámenes)


# Iniciar el programa cargando la disponibilidad y los pacientes
disponibilidad = cargar_disponibilidad('disponibilidad.txt')
pacientes = cargar_pacientes('pacientes.csv')
ciclo_principal(disponibilidad, pacientes, 'disponibilidad.txt')
