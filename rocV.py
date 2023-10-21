from copy import deepcopy


def insaEstudiante(
    asignaciones: dict[str, list],
    solicitudes: dict[str, list[tuple[str, int]]],
    suma_prioridad_no_asignadas: list[int],
):
    listres = []
    insatisfaccion = 0
    listma = [len(lista) for lista in asignaciones.values()]
    listms = [len(lista1) for lista1 in solicitudes.values()]
    c = 0
    for i in range(len(suma_prioridad_no_asignadas)):
        res = (1 - (abs(listma[i]) / abs(listms[i]))) * (
            suma_prioridad_no_asignadas[i] / ((3 * abs(listms[i])) - 1)
        )
        listres.append(res)
        if len(listres) == len(listms):
            break

    suma_general = sum(listres)
    insatisfaccion = suma_general / len(suma_prioridad_no_asignadas)
    return insatisfaccion


def rocV(
    datos: tuple[dict[str, int], dict[str, list[tuple[str, int]]]]
) -> tuple[dict[str, list[str]], float]:
    # clave cod asig : valor cupo asign
    materias = deepcopy(datos[0])
    estudiantes = deepcopy(datos[1])
    solicitudes = deepcopy(estudiantes)
    asignaciones = {estudiante: [] for estudiante in estudiantes.keys()}

    while True:
        # Los chances que tiene cada estudiante para obtener una materia
        chances = {}
        for estudiantes_chances in estudiantes:
            suma = 0
            materias_solicitadas_chances = estudiantes[estudiantes_chances]
            for codigo, _ in materias_solicitadas_chances:
                if codigo in materias:
                    cupo = int(materias[codigo])
                    suma = suma + cupo
            chances.update({estudiantes_chances: suma})
        # Ordenar el diccionario por valores de menor a mayor
        chances_ordenado = dict(sorted(chances.items(), key=lambda item: item[1]))
        for estudiante in chances_ordenado:
            materias_solicitadas = estudiantes[estudiante]
            materias_solicitadas_ordenadas = sorted(
                materias_solicitadas, key=lambda x: x[1], reverse=True
            )
            for codigo, prioridad in materias_solicitadas_ordenadas:
                if materias[codigo] > 0:
                    if codigo not in asignaciones[estudiante]:
                        asignaciones[estudiante].append((codigo, prioridad))
                        lista_asignatura_solicitada = estudiantes[estudiante]
                        lista_asignatura_solicitada.remove((codigo, prioridad))
                        materias[codigo] = materias[codigo] - 1
                        break

        if all(valor == 0 for valor in materias.values()):
            break
    suma_prioridad_no_asignadas = []

    for lista_de_tuplas in estudiantes.values():
        suma = sum(valor for _, valor in lista_de_tuplas)
        suma_prioridad_no_asignadas.append(suma)

    insatisfaccion = insaEstudiante(
        asignaciones, solicitudes, suma_prioridad_no_asignadas
    )
    return asignaciones, insatisfaccion
