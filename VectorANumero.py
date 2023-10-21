from math import floor, inf
from itertools import combinations, product


def vector_I_i(materias: dict[str, int]) -> list[int]:
    I_i_list = [1]
    K = len(materias)
    cupos = [cupo for cupo in materias.values()]

    I_i = 1

    for j in range(K - 1):
        m_j = cupos[(K - 1) - j]
        I_i *= m_j + 1
        I_i_list.insert(0, I_i)

    return I_i_list


def vector_a_numero(materias: dict[str, int], cupos: list[int]) -> int:
    n = 0
    K = len(materias)
    I_i_list = vector_I_i(materias)
    lista_cupos = [cupo for cupo in cupos.values()]

    for i in range(K):
        c_i = lista_cupos[i]
        I_i = I_i_list[i]
        n += c_i * I_i
        print(f"c_{i}: {c_i}, I_{i}: {I_i}, n: {n}")

    return n


def numero_a_vector(materias: dict[str, int], num: int) -> list[int]:
    I_i_list = vector_I_i(materias)
    cupos = []
    K = len(I_i_list)

    aux = num

    for i in range(K):
        c_i = floor(aux / I_i_list[i])
        aux %= I_i_list[i]
        cupos.append(c_i)

    return cupos


def main():
    materias = {"M1": 3, "M2": 4, "M3": 2}
    cupos = {"M1": 1, "M2": 1, "M3": 2}
    I_i_list = vector_I_i(materias)
    print(I_i_list)
    numero = vector_a_numero(materias, cupos)
    print(numero)
    cupitos = numero_a_vector(materias, numero)
    print(cupitos)


if __name__ == "__main__":
    main()
