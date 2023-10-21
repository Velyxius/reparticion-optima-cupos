from pathlib import Path


class rocfile:
    """Tipo de Archivo .ROC"""

    pass


def leer_archivo(archivo: str) -> tuple:
    """Lee archivos .ROC"""
    numero_materias = 0
    numero_estudiantes = 0
    materias = {}
    estudiantes = {}

    entrada = open(
        file=archivo,
        mode="r",
        encoding="utf-8",
    )

    numero_materias = int(entrada.readline())

    # Se leen las materias y se les asigna su respectivo cupo
    for linea in range(0, numero_materias):
        linea = entrada.readline()
        linea = linea.split(",")
        materias[linea[0]] = int(linea[1])

    # Se lee el número de estudiantes
    numero_estudiantes = int(entrada.readline())

    # Se leen los estudiantes
    for estudiante in range(0, numero_estudiantes):
        # Se lee el código de estudiantes y el número de materias solicitadas
        estudiante = entrada.readline().strip()
        estudiante = estudiante.split(",")

        nuevo_estudiante = []
        numero_materias_estudiante = int(estudiante[1])

        # Se leen las materias solicitadas con su respectiva prioridad
        for solicitud in range(0, numero_materias_estudiante):
            solicitud = entrada.readline().strip()
            solicitud = solicitud.split(",")
            # print(solicitud)
            # [solicitud[0]] = int(solicitud[1])
            nuevo_estudiante.append((solicitud[0], int(solicitud[1])))

        estudiantes[estudiante[0]] = nuevo_estudiante
        # estudiantes[estudiante[0]] = (numero_materias_estudiante, nuevo_estudiante)

    entrada.close()

    return (numero_materias, numero_estudiantes, materias, estudiantes)


def escribir_archivo(
    archivo: str, asignaciones: dict, insatisfaccion: float, tipo_algoritmo: str
) -> rocfile:
    """Escribe un archivo .ROC con la solución del problema y su respectivo costo"""
    dato = archivo.split(".")

    salida = open(
        file=(Path(__file__).parent / f"Salidas/{dato[0]}_{tipo_algoritmo}.{dato[1]}"),
        mode="w",
        encoding="utf-8",
    )

    salida.write("Costo" + "\n")
    salida.write(str(insatisfaccion) + "\n")

    for estudiante in asignaciones:
        asignacion = asignaciones[estudiante]
        salida.write(estudiante + "," + str(len(asignacion)) + "\n")

        for materia in asignacion:
            codigo_materia = materia[0]
            salida.write(codigo_materia + "\n")
