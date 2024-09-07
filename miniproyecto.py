import csv


def cargar_disponibilidad(archivo_disponibilidad):
    disponibilidad = {}
    with open(archivo_disponibilidad, 'r') as file:
        for linea in file:
            examen, horas = linea.strip().split()
            disponibilidad[examen] = int(horas)
    return disponibilidad


def cargar_pacientes(archivo_pacientes):
    pacientes = {}
    with open(archivo_pacientes, newline='') as file:
        reader = csv.reader(file)
        for fila in reader:
            nombre_paciente = fila[0]
            exámenes = fila[1:]
            pacientes[nombre_paciente] = exámenes
    return pacientes


def atender_paciente(paciente, disponibilidad, pacientes, archivo_disponibilidad):
    # Verificar que el paciente exista
    if paciente not in pacientes:
        print(f"El paciente {paciente} no está registrado.")
        return

    # Verificar disponibilidad de los exámenes
    exámenes_requeridos = pacientes[paciente]
    for examen in exámenes_requeridos:
        if disponibilidad.get(examen, 0) <= 0:
            print(f"No es posible atender a {paciente} porque no existen horas disponibles para el examen {examen}.")
            return

    # Si hay disponibilidad, se atiende al paciente
    for examen in exámenes_requeridos:
        disponibilidad[examen] -= 1

    print(f"Se ha atendido con éxito a {paciente}!")
    imprimir_disponibilidad(disponibilidad)

    # Actualizar el archivo 'disponibilidad.txt'
    actualizar_disponibilidad(archivo_disponibilidad, disponibilidad)


def agregar_disponibilidad(exámenes, disponibilidad, archivo_disponibilidad):
    for examen in exámenes:
        if examen in disponibilidad:
            disponibilidad[examen] += 1
        else:
            disponibilidad[examen] = 1
    imprimir_disponibilidad(disponibilidad)

    # Actualizar el archivo 'disponibilidad.txt'
    actualizar_disponibilidad(archivo_disponibilidad, disponibilidad)


def imprimir_disponibilidad(disponibilidad):
    for examen, horas in disponibilidad.items():
        print(f"{examen.upper()}: {horas}")


def ciclo_principal(disponibilidad, pacientes, archivo_disponibilidad):
    while True:
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


def actualizar_disponibilidad(archivo_disponibilidad, disponibilidad):
    with open(archivo_disponibilidad, 'w') as file:
        for examen, horas in disponibilidad.items():
            file.write(f"{examen} {horas}\n")


def actualizar_pacientes(archivo_pacientes, pacientes):
    with open(archivo_pacientes, 'w', newline='') as file:
        writer = csv.writer(file)
        for paciente, exámenes in pacientes.items():
            writer.writerow([paciente] + exámenes)


disponibilidad = cargar_disponibilidad('disponibilidad.txt')
pacientes = cargar_pacientes('pacientes.csv')

ciclo_principal(disponibilidad, pacientes, 'disponibilidad.txt')
