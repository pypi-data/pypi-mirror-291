import numpy as np
from . import neutrosophic_number
from .neutrosophic_number import NeutrosophicNumber


def add_min(matrix1, matrix2):
    result = np.empty(matrix1.shape, dtype=object)
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            result[i, j] = neutrosophic_number.add_min(matrix1[i, j], matrix2[i, j])
    return result


def add_max(matrix1, matrix2):
    result = np.empty(matrix1.shape, dtype=object)
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            result[i, j] = neutrosophic_number.add_max(matrix1[i, j], matrix2[i, j])
    return result


def multiply(matrix1, matrix2):
    result = np.empty((matrix1.shape[0], matrix2.shape[1]), dtype=object)
    for i in range(matrix1.shape[0]):
        for j in range(matrix2.shape[1]):
            sum_result = "0 + 0I"
            for k in range(matrix1.shape[1]):
                a = neutrosophic_number.multiply(matrix1[i, k], matrix2[k, j])
                sum_result = f"{sum_result} + {a}"
            result[i, j] = NeutrosophicNumber(sum_result)
    return result



