"""
This module contains the implementation of a neutrosophic number
and its operations based on the paper: Pura Vida Neutrosophic Algebra.
"""

from dataclasses import dataclass
import re

@dataclass
class Indeterminacy:
    """Represents the indeterminacy part of a neutrosophic number."""
    coefficient: float


class NeutrosophicNumber:
    """
    A neutrosophic number is a number of the form "X = a + bI".
    Where "a" is a real or complex coefficient and
    "b" is a real or complex number binded to indeterminacy (I).

    Having two neutrosophic numbers `X = a + bI` and `Y = c + dI`
    Operations for them stated in Pura Vida Neutrosophic Algebra are:
    - Addition using Max-Plus algebra.
        > add_max(X, Y) = max(a, c) + max(b, d)I.
    - Addition using Min-Plus (Tropical) algebra.
        > add_min(X, Y) = min(a, c) + min(b, d)I.
    - Multiplication.
        > multipy(X, Y) = (a + c) + (b + d)I.
    """

    def __init__(self, *args):
        if isinstance(args[0], str):
            real_part = 0
            imaginary_part = 0

            real_pattern = r'[-+]?\d*\.?\d+(?!I)'
            imaginary_pattern = r'[-+]?\s?\d*\.?\d*I'

            real_terms = re.findall(real_pattern, args[0])
            real_part = sum(float(term) for term in real_terms)

            imaginary_terms = re.findall(imaginary_pattern, args[0])
            for term in imaginary_terms:
                if term == '+I' or term == 'I':
                    imaginary_part += 1
                elif term == '-I':
                    imaginary_part -= 1
                elif "-" in term:
                    imaginary_part -= float(term.strip('-I'))
                else:
                    imaginary_part += float(term.strip('+I'))
            self.coefficient = real_part
            self.indet = Indeterminacy(imaginary_part)

        elif len(args) == 2:
            if all([val for val in args if isinstance(val, int)]):
                self.coefficient = int(args[0])
                self.indet = Indeterminacy(int(args[1]))
            elif all([val for val in args if isinstance(val, float)]):
                self.coefficient = float(args[0])
                self.indet = Indeterminacy(float(args[1]))
        else:
            print("ConstructorError: NeutrosophicNumber() does not support the provided arguments")

    def add_max(self, other: "NeutrosophicNumber") -> "NeutrosophicNumber":
        """Addition using Max-Plus algebra."""
        return NeutrosophicNumber(
            max(self.coefficient, other.coefficient),
            max(self.indet.coefficient, other.indet.coefficient),
        )

    def add_min(self, other: "NeutrosophicNumber") -> "NeutrosophicNumber":
        """Addition using Min-Plus (Tropical) algebra."""
        return NeutrosophicNumber(
            min(self.coefficient, other.coefficient),
            min(self.indet.coefficient, other.indet.coefficient),
        )

    def multiply(self, other: "NeutrosophicNumber") -> "NeutrosophicNumber":
        """Multiplication"""
        return NeutrosophicNumber(
            self.coefficient + other.coefficient, 
            self.indet.coefficient + other.indet.coefficient
        )

    def __repr__(self):
        sign = "+" if self.indet.coefficient >= 0 else "-"
        coefficient = self.coefficient
        indeterminacy = self.indet.coefficient
        if not coefficient and not indeterminacy:
            return "(0)"
        elif abs(indeterminacy) == 1:
            return f"({coefficient}{sign}I)"
        return f"({coefficient}{sign}{abs(indeterminacy)}I)"


def add_min(number1: "NeutrosophicNumber", number2: "NeutrosophicNumber"):
    return number1.add_min(number2)


def add_max(number1: "NeutrosophicNumber", number2: "NeutrosophicNumber"):
    return number1.add_max(number2)


def multiply(number1: "NeutrosophicNumber", number2: "NeutrosophicNumber"):
    return number1.multiply(number2)