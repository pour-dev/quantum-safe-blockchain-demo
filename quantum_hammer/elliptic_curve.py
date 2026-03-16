"""
Project: Quantum-Safe Blockchain Demonstrator
Module: elliptic_curve.py

Author: Davood Ziaeian-Pour
GitHub: https://github.com/pour-dev
Created: 2026-03-15
License: MIT

Description:
    Minimal educational implementation of elliptic curve arithmetic.

    This module provides a very small "toy" elliptic curve used to
    demonstrate how classical blockchain signatures such as ECDSA
    operate. The implementation includes basic point addition and
    scalar multiplication on a finite field.

    The curve parameters are intentionally tiny and insecure to allow
    easy visualization and simulation of cryptographic concepts.

Features:
    - Modular inverse calculation
    - Elliptic curve point addition
    - Point doubling
    - Scalar multiplication (double-and-add algorithm)

Classes:
    ToyEllipticCurve
        Simplified elliptic curve implementation used for educational
        demonstrations.

Functions:
    mod_inverse(a, p)
        Computes the modular inverse of a modulo p.

Notes:
    This implementation is NOT cryptographically secure and should
    never be used in production systems. It exists solely for
    educational demonstrations of blockchain and cryptographic
    principles.
"""

import math


def mod_inverse(a, p):
    """Compute the modular inverse of a modulo p."""
    return pow(a, -1, p)


class ToyEllipticCurve:
    """
    Toy elliptic curve implementation for educational purposes.

    Represents the curve:

        y² = x³ + a·x + b  (mod p)

    Only intended for demonstrations of elliptic curve cryptography.
    """
    
    def __init__(self, p=5, a=3, b=2, order=5):
        self.p = p
        self.a = a
        self.b = b
        self.order = order
        self.num_bits = math.ceil(math.log2(self.p))

    def add(self, P, Q):
        """Add two points P and Q on the toy elliptic curve."""
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        # Point at infinity (inverse points)
        if x1 == x2 and y1 == (-y2 % self.p):
            return None

        # Point doubling
        if P == Q:
            slope = (3 * x1**2 + self.a) * mod_inverse(2 * y1, self.p) % self.p
        else:
            slope = (y2 - y1) * mod_inverse(x2 - x1, self.p) % self.p

        x3 = (slope**2 - x1 - x2) % self.p
        y3 = (slope * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def mul(self, P, k):
        """Scalar multiplication k * P using double-and-add."""
        result = None
        current = P
        while k > 0:
            if k & 1:
                result = self.add(result, current)
            current = self.add(current, current)
            k >>= 1
        return result