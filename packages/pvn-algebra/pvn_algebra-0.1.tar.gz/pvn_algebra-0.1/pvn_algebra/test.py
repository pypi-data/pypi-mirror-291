from neutrosophic_number import NeutrosophicNumber
import neutrosophic_number as number
import neutrosophic_matrix as matrix
import numpy as np

a = NeutrosophicNumber(5, 6)
b = NeutrosophicNumber(-1, 14)
c = NeutrosophicNumber(1, 6.66)
d = NeutrosophicNumber(0, -1.4)
e = NeutrosophicNumber("7.9 + 5.1 + 8.9I - 7.4I") # 13 + 1.5I
f = NeutrosophicNumber("8 + 9 + 4 - 8.1 - 0.005I") #29.1 + 0.005I
print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"d = {d}")
print(f"e = {e}")
print(f"f = {f}")

print(f"number.add_max(a, f) = {number.add_max(a, f)}")
print(f"number.add_min(c, d) = {number.add_min(c, d)}")
print(f"number.multiply(b, e) = {number.multiply(b, e)}")


print(NeutrosophicNumber(1, 0))
print(NeutrosophicNumber(0, 9))
print(NeutrosophicNumber(0, 0))
print(NeutrosophicNumber(0, -1))
print(NeutrosophicNumber(0, 1))

A = np.matrix([
    [NeutrosophicNumber(-8, 1), NeutrosophicNumber(5, -1)],
    [NeutrosophicNumber(3, 8), NeutrosophicNumber(23, -2)]
])

B = np.matrix([
    [NeutrosophicNumber(3, 2), NeutrosophicNumber(13, 3)],
    [NeutrosophicNumber(7, 9), NeutrosophicNumber(3, 5)]
])
print("----------- ADD MIN -----------")
C = matrix.add_min(A, B)
print(C, "\n")
print("----------- ADD MAX -----------")
E = matrix.add_max(A, B)
print(E, "\n")
print("----------- MULTIPLY -----------")
A = np.matrix([
    [NeutrosophicNumber(-1,0), NeutrosophicNumber(2,0), NeutrosophicNumber(0,-1)],
    [NeutrosophicNumber(3,0), NeutrosophicNumber(0, 1), NeutrosophicNumber(0,0)]
])

B = np.matrix([
    [NeutrosophicNumber(0,1), NeutrosophicNumber(1,0), NeutrosophicNumber(2,0), NeutrosophicNumber(4,0)],
    [NeutrosophicNumber(1,0), NeutrosophicNumber(0,1), NeutrosophicNumber(0,0), NeutrosophicNumber(2,0)],
    [NeutrosophicNumber(5,0), NeutrosophicNumber(-2,0), NeutrosophicNumber(0,3), NeutrosophicNumber(0,-1)]
])
E = matrix.multiply(A, B)
print(E, "\n")