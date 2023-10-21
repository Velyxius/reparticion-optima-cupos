from copy import deepcopy
from pathlib import Path
from itertools import combinations
from math import inf


class rocfile:
    """Tipo de Archivo .ROC"""

    pass


def leer_archivo(archivo: rocfile) -> tuple:
    """Lee archivos .ROC"""
    numero_materias = 0
    numero_estudiantes = 0
    materias = {}
    estudiantes = {}

    entrada = open(
        file=(Path(__file__).parent / "Pruebas/{}".format(archivo)),
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
    archivo: rocfile,
    asignaciones: dict[str, list[tuple[str, int]]],
    insatisfaccion: float,
    tipo_algoritmo: str,
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


def combinar_solicitud_estudiante(
    estudiante: str, solicitud: list[tuple], cupos: dict
) -> list:
    """
    Devuelve todas las combinaciones posibles de la solicitud de un estudiante
    para generar asignaciones

    Complejidad: O(2^k)
    """
    combinaciones = []

    for i in range(len(solicitud) + 1):
        for comb in combinations(solicitud, i):
            if not comb:
                combinaciones.append((estudiante, list(comb)))
                continue

            solis = []
            for soli in comb:
                mat = soli[0]
                if cupos.get(mat) == 0:
                    pass
                else:
                    solis.append((soli))

            combinaciones.append((estudiante, solis))

    return combinaciones


def restar_cupos_disponibles(asignacion: tuple, cupos: dict) -> dict:
    cupos_disponibles = cupos.copy()
    asignaciones = asignacion[1]

    if len(asignaciones) == 0:
        return cupos_disponibles

    for asign in asignaciones:
        materia = asign[0]
        if materia in cupos_disponibles.keys():
            cupos_disponibles[materia] -= 1

    return cupos_disponibles


def insatisfaccion(
    estudiantes: dict,
    asignacion: tuple,
) -> float:
    """Calcula la insatisfacción de un estudiante"""
    parametros = calcular_parametros_insatisfaccion(estudiantes, asignacion)
    solicitadas = parametros[0]
    asignadas = parametros[1]
    prioridad_no_asignadas = parametros[2]
    prioridad_total = (3 * solicitadas) - 1

    insatis = (1 - (asignadas / solicitadas)) * (
        prioridad_no_asignadas / prioridad_total
    )
    return insatis


def calcular_parametros_insatisfaccion(
    estudiantes: dict,
    asignacion: tuple,
) -> tuple:
    """Calcula los parámetros de la insatisfacción de un estudiante"""
    solicitadas = 0
    asignadas = 0
    prioridad_no_asignadas = 0

    estudiante = asignacion[0]
    asignaciones = asignacion[1]
    solicitudes = estudiantes.get(estudiante)
    # print(estudiante, asignaciones, solicitudes)

    for soli in solicitudes:
        prioridad = soli[1]
        solicitadas += 1

        if soli in asignaciones:
            asignadas += 1
        elif soli not in asignaciones:
            prioridad_no_asignadas += prioridad

    return (
        solicitadas,
        asignadas,
        prioridad_no_asignadas,
    )


# Diccionario para almacenar la llave de estudiante y su asignación, y la insatisfacción calculada
almacen = {}


def asignar_materias(estudiantes: dict, cupos: dict) -> tuple:
    global almacen

    if len(estudiantes) == 0:
        return [], 0

    # Obtenemos al primer estudiante y su asignación
    estudiante = obtener_primer_llave(estudiantes)
    solicitud = estudiantes.get(estudiante)
    valor_cupos = obtener_lista_valores(cupos)

    if sum(valor_cupos) == 0:
        return [], 1

    llave = (estudiante, tuple(valor_cupos))

    if llave in almacen:
        return almacen.get(llave)

    aux_estudiantes = estudiantes.copy()
    aux_estudiantes.pop(estudiante)

    insatisfacciones = []
    ruta_asignaciones = []

    asignaciones = combinar_solicitud_estudiante(estudiante, solicitud, cupos)

    for asignacion in asignaciones:
        # print(asignacion)

        cupos_restantes = restar_cupos_disponibles(asignacion, cupos)

        asignacion_subproblema, insatisfaccion_subproblema = asignar_materias(
            aux_estudiantes, cupos_restantes
        )

        if len(estudiantes) == 1:
            insatisfaccion_general = (
                insatisfaccion(estudiantes, asignacion) + (insatisfaccion_subproblema)
            ) / len(estudiantes)
        else:
            insatisfaccion_general = (
                insatisfaccion(estudiantes, asignacion)
                + (insatisfaccion_subproblema * (len(estudiantes) - 1))
            ) / len(estudiantes)

        # print(insatisfaccion_general)
        insatisfacciones.append(insatisfaccion_general)
        ruta_asignaciones.append(
            [{estudiante: asignacion[1]}] + asignacion_subproblema
        )  # Añadir a la asignacion actual la asignacion del subproblema como un diccionario

    # print(insatisfacciones)
    # print(ruta_asignaciones)
    insatisfaccion_minima = min(insatisfacciones)
    min_index = insatisfacciones.index(insatisfaccion_minima)

    # Guardar el    resultado en almacen
    almacen[llave] = (ruta_asignaciones[min_index], insatisfaccion_minima)
    return almacen[llave]


def formatear_solucion(solucion: tuple[list[dict], float], materias: dict) -> tuple:
    """Formatea las asignaciones"""
    asignaciones = {}

    for estudiante in solucion[0]:
        asignaciones.update(estudiante)

    salida = (asignaciones, solucion[1])

    return salida


def obtener_lista_llaves(dicti: dict) -> list:
    """Devuelve una lista con las llaves de un diccionario"""
    return list(dicti.keys())


def obtener_lista_valores(dicti: dict) -> list:
    """Devuelve una lista con los valores de un diccionario"""
    return list(dicti.values())


def obtener_primer_llave(dicti: dict) -> str:
    """Devuelve el último estudiante"""
    return next(iter(dicti.keys()))


def obtener_ultima_llave(dicti: dict) -> str:
    """Devuelve el último estudiante"""
    return next(reversed(dicti.keys()))


def invertir_diccionario(dicti: dict) -> list:
    """Devuelve un diccionario invertido"""
    return dict(reversed(list(dicti.items())))


def rocPD(
    numero_materias: float, numero_estudiantes: float, materias: dict, estudiantes: dict
) -> tuple[list[dict], float]:
    cupos = materias
    asignaciones = asignar_materias(estudiantes, cupos)
    formato = formatear_solucion(asignaciones, materias)
    print(formato)

    return formato


def main():
    archivillo = "a_prueba_custom.roc"
    # print(f"Datos: {leer_archivo(archivillo)}")
    (numero_materias, numero_estudiantes, materias, estudiantes) = leer_archivo(
        archivillo
    )
    solucion = rocPD(numero_materias, numero_estudiantes, materias, estudiantes)
    escribir_archivo(archivillo, solucion[0], solucion[1], "rocPD")
    print(almacen)
    print(len(almacen))


if __name__ == "__main__":
    main()
