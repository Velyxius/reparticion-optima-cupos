from copy import deepcopy
from pathlib import Path
from itertools import combinations, product
from math import inf
from typing import Dict

students = dict[str, list[tuple[str, int]]]


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
        file=(Path(__file__).parent / f"Pruebas/{archivo}"),
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
        file=(
            Path(__file__).parent
            / "Salidas/{}_{}.{}".format(dato[0], tipo_algoritmo, dato[1])
        ),
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


def insatisfaccion(
    estudiantes: dict,
    asignacion: tuple[str, list[tuple[str, int]]],
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
    asignacion: tuple[str, list[tuple[str, int]]],
) -> tuple:
    """Calcula los parámetros de la insatisfacción de un estudiante"""
    solicitadas = 0
    asignadas = 0
    prioridad_no_asignadas = 0

    estudiante = asignacion[0]
    materias = asignacion[1]
    solicitudes = estudiantes.get(estudiante)
    # print(estudiante, materias, solicitudes)

    for soli in solicitudes:
        prioridad = soli[1]
        solicitadas += 1

        if soli in materias:
            asignadas += 1
        elif soli not in materias:
            prioridad_no_asignadas += prioridad

    return (
        solicitadas,
        asignadas,
        prioridad_no_asignadas,
    )


def combinar_solicitud_estudiante(estudiante: str, solicitud: list[tuple]) -> list:
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
                solis.append((soli))

            combinaciones.append((estudiante, solis))

    return combinaciones


def generar_combinaciones_asignaciones(
    estudiantes: dict,
) -> tuple[tuple[tuple[str, list[tuple[str, int]]]]]:
    """
    Devuelve todas las combinaciones posibles de asignaciones a todos los estudiantes

    Complejidad: O((2^k)^r)
    """
    combs = [
        combinar_solicitud_estudiante(est, soli) for est, soli in estudiantes.items()
    ]
    return tuple(product(*combs))


def restar_cupos_disponibles(
    asignaciones: tuple[tuple[str, list[tuple[str, int]]]], cupos: dict
) -> dict:
    cupos_disponibles = cupos

    if len(asignaciones) == 0:
        return cupos_disponibles

    for estudiante in asignaciones:
        materias = estudiante[1]
        for materia in materias:
            codigo_materia = materia[0]
            cupos[codigo_materia] -= 1

    return cupos_disponibles


def comprobar_factibilidad(
    asignaciones: tuple[tuple[str, list[tuple[str, int]]]], cupos: dict
) -> bool:
    """
    Comprueba si una asignación es factible en términos de cupos
    """
    cupos_disponibles = restar_cupos_disponibles(asignaciones, cupos)

    for cupo in cupos_disponibles.values():
        if cupo < 0:
            return False

    return True


def obtener_lista_llaves(dicti: dict) -> list:
    """Devuelve una lista con las llaves de un diccionario"""
    return list(dicti.keys())


def obtener_lista_valores(dicti: dict) -> list:
    """Devuelve una lista con los valores de un diccionario"""
    return list(dicti.values())


def obtener_primer_llave(dicti: dict) -> str:
    """Devuelve la primer llave de un diccionario"""
    return next(iter(dicti.keys()))


def rocFB(
    numero_materias: float, numero_estudiantes: float, materias: dict, estudiantes: dict
) -> tuple[dict[str, list[tuple[str, int]]], float]:
    combinaciones = generar_combinaciones_asignaciones(estudiantes)
    solucion = []
    insatis = inf

    for asignaciones in combinaciones:
        cupos = materias.copy()
        if comprobar_factibilidad(asignaciones, cupos):
            insat = 0
            for estudiante in asignaciones:
                insat += insatisfaccion(estudiantes, estudiante)
            if insat < insatis:
                insatis = insat
                solucion = asignaciones

    solucion = dict(solucion)
    return (solucion, insatis / numero_estudiantes)


def main():
    archivillo = "e_3_5_5.roc"
    # print(f"Datos: {leer_archivo(archivillo)}")
    (numero_materias, numero_estudiantes, materias, estudiantes) = leer_archivo(
        archivillo
    )
    solucion = rocFB(numero_materias, numero_estudiantes, materias, estudiantes)
    print(solucion)
    escribir_archivo(archivillo, solucion[0], solucion[1], "rocFB")


if __name__ == "__main__":
    main()
