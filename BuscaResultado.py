import csv
import numpy as np


def buscar_resultado(concurso=100):
    f = open('lotofacil.csv')
    csv_f = csv.reader(f)
    resultados = []
    for row in csv_f:
        if row != []:
            resultados.append(row)
    list_resultado = resultados[concurso]
    num_sort = list_resultado[2:17]
    num_sort = list(map(int, num_sort))
    num_sort = sorted(num_sort)
    resultado = {
        "data": list_resultado[1],
        "numbers": num_sort,
        "p15": real_float(list_resultado[17]),
        "p14": real_float(list_resultado[18]),
        "p13": real_float(list_resultado[19]),
        "p12": real_float(list_resultado[20]),
        "p11": real_float(list_resultado[21])
    }
    return resultado

def real_float(real):
    return float(real.replace(".", "").replace(",", "."))
