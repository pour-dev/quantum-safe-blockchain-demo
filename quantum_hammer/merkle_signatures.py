"""
Project: Quantum-Safe Blockchain Demonstrator
Module: merkle_signature.py

Author: Davood Ziaeian-Pour
GitHub: https://github.com/pour-dev
Created: 2026-03-15
License: MIT

Description:
    Educational implementation of a hash-based Merkle signature scheme
    using Lamport-style One-Time Signatures (OTS).

    This module demonstrates the core principles of hash-based
    post-quantum cryptography. Each message is signed using a Lamport
    One-Time Signature, and many such keys are aggregated using a
    Merkle tree structure to allow multiple signatures from a single
    compact public root.

    The implementation illustrates how hash-based signature schemes
    remain secure even in the presence of quantum computers, because
    their security relies only on the preimage resistance of
    cryptographic hash functions.

Features:
    - SHA-256 based hashing
    - Lamport-style one-time signatures
    - Merkle tree construction
    - Authentication path (Merkle proof)
    - Signature verification

Classes:
    ToyMerkleSignatureScheme
        Demonstrates a simplified Merkle tree signature system suitable
        for educational demonstrations of post-quantum cryptography.

Dependencies:
    - Python 3.9+
    - hashlib (standard library)

Notes:
    This implementation is intentionally simplified and NOT secure for
    real-world use. It uses very small parameters and deterministic
    key generation to make the algorithm easier to understand.

    The goal is to demonstrate the principles behind hash-based
    signature systems such as XMSS and SPHINCS+.

References:
    - XMSS: eXtended Merkle Signature Scheme
    - SPHINCS+: Stateless Hash-Based Signatures
"""

import hashlib


def sha256(x: bytes) -> bytes:
    return hashlib.sha256(x).digest()


class ToyMerkleSignatureScheme:
    """
    Educational Merkle signature scheme using Lamport-style OTS.

    Example:
        scheme = ToyMerkleSignatureScheme(num_keys=8)

        message = b"Hello blockchain"
        signature = scheme.sign(message)

        valid = ToyMerkleSignatureScheme.verify(
            scheme.root,
            message,
            signature
        )

        print("Signature valid:", valid)
    """

    def __init__(self, num_keys: int):
        self.num_keys = num_keys

        # Each OTS key consists of TWO random 32-byte values
        # (Lamport OTS: one for bit=0, one for bit=1)
        self.private_keys = [
            (sha256(f"sk{i}_0".encode()), sha256(f"sk{i}_1".encode()))
            for i in range(num_keys)
        ]

        # Public keys = hash of each private component
        self.public_keys = [
            (sha256(sk0), sha256(sk1))
            for (sk0, sk1) in self.private_keys
        ]

        # Track used OTS keys
        self.used = set()

        # Build Merkle tree from public keys
        leaves = [sha256(pk0 + pk1) for (pk0, pk1) in self.public_keys]
        self.tree = self._build_merkle_tree(leaves)
        self.root = self.tree[-1][0]

    # ---------------------------------------------------------
    # Merkle tree construction
    # ---------------------------------------------------------
    def _build_merkle_tree(self, leaves):
        tree = [leaves]
        level = leaves

        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else left
                next_level.append(sha256(left + right))
            tree.append(next_level)
            level = next_level

        return tree

    # ---------------------------------------------------------
    # Merkle proof
    # ---------------------------------------------------------
    def _merkle_proof(self, index):
        proof = []
        idx = index

        for level in self.tree[:-1]:
            sibling = idx ^ 1
            if sibling < len(level):
                proof.append(level[sibling])
            else:
                proof.append(level[idx])
            idx //= 2

        return proof

    # ---------------------------------------------------------
    # Lamport-style OTS signing
    # ---------------------------------------------------------
    def _sign_ots(self, sk_pair, message: bytes):
        """
        For each bit of the message hash:
        - If bit = 0 → reveal sk0
        - If bit = 1 → reveal sk1
        """
        h = sha256(message)
        bits = bin(int.from_bytes(h, "big"))[2:].zfill(256)

        sk0, sk1 = sk_pair
        signature = []

        for bit in bits:
            signature.append(sk0 if bit == "0" else sk1)

        return signature

    # ---------------------------------------------------------
    # Public sign() method
    # ---------------------------------------------------------
    def sign(self, message: bytes):
        available = [i for i in range(self.num_keys) if i not in self.used]
        if not available:
            raise IndexError("All OTS keys have been used.")

        idx = available[0]
        self.used.add(idx)

        sk_pair = self.private_keys[idx]
        pk_pair = self.public_keys[idx]

        sig = self._sign_ots(sk_pair, message)
        proof = self._merkle_proof(idx)

        return {
            "index": idx,
            "pk": pk_pair,
            "sig": sig,
            "proof": proof,
        }

    # ---------------------------------------------------------
    # Verification
    # ---------------------------------------------------------
    @staticmethod
    def verify(root: bytes, message: bytes, signature: dict) -> bool:
        idx = signature["index"]
        pk0, pk1 = signature["pk"]
        sig = signature["sig"]
        proof = signature["proof"]

        # Recompute expected public key from signature
        h = sha256(message)
        bits = bin(int.from_bytes(h, "big"))[2:].zfill(256)

        # Verify each revealed secret matches the public key
        for bit, revealed in zip(bits, sig):
            expected = pk0 if bit == "0" else pk1
            if sha256(revealed) != expected:
                return False

        # Recompute leaf = hash(pk0 || pk1)
        node = sha256(pk0 + pk1)

        # Recompute Merkle root
        for sibling in proof:
            if idx % 2 == 0:
                node = sha256(node + sibling)
            else:
                node = sha256(sibling + node)
            idx //= 2

        return node == root