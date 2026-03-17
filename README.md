
# Quantum Hammer

## Educational Demonstration of Quantum Threats to Blockchain Cryptography

Quantum Hammer is an educational Python project that demonstrates how future quantum computers could threaten classical blockchain cryptography and how post-quantum alternatives can mitigate this risk.

## GUI Demonstration

The simulator includes a graphical interface for demonstrating
quantum-style attacks on elliptic-curve cryptography and
post-quantum hash-based signatures.

### Main Application

![Main GUI](https://github.com/pour-dev/quantum-safe-blockchain-demo/blob/main/doc/images/gui_main.png)

### Quantum Attack Simulation

![Attack Simulation](https://github.com/pour-dev/quantum-safe-blockchain-demo/blob/main/doc/images/attack_simulation.png)

### Merkle Signature Demonstration

![Merkle Demo](https://github.com/pour-dev/quantum-safe-blockchain-demo/blob/main/doc/images/merkle_demo.png)

## The project illustrates three core concepts:

- Elliptic Curve Cryptography (ECC)
- Quantum attacks on the Elliptic Curve Discrete Logarithm Problem
- Post-quantum hash-based signature schemes using Merkle trees

This repository is intended for educational and research demonstration purposes only.

## Project Overview

The system demonstrates the contrast between classical and quantum-resistant cryptography.

## Components

Elliptic Curve Module

A simplified elliptic curve implementation used to demonstrate:
- point addition
- scalar multiplication
- public key derivation

This illustrates the classical structure used in blockchain signatures.

## Quantum Attack Simulator

A simulated attack on the elliptic curve discrete logarithm problem.

The simulator supports three execution modes:

1.	Quantum simulation using Qiskit
2.	Quantum simulation using Cirq
3.	Classical brute-force fallback

Because current quantum frameworks do not implement a full elliptic-curve Shor algorithm, the attack is demonstrated using QFT-style circuits and toy curves.


## Post-Quantum Signature Scheme

A simplified implementation of a hash-based signature system using Merkle trees.

The scheme demonstrates the basic idea behind quantum-safe signatures such as:
- XMSS
- SPHINCS+


## Mathematical Foundation

Elliptic Curve Cryptography

The security of elliptic curve cryptography relies on the hardness of the Elliptic Curve Discrete Logarithm Problem (ECDLP).

Given

- a cyclic group ⟨G⟩ of order n
- a generator point G
- a public key

Q = d.G


where  d € Zₙ is the private key.

For classical computers, no efficient algorithm is known to compute d from Q and G.


## Quantum Attack Principle

Quantum computers can apply Shor’s algorithm to solve discrete logarithm problems efficiently.

The algorithm reduces the problem to period finding.

Define the function

f(x₁, x₂) = x₁ G + x₂ Q

A quantum computer evaluates this function in superposition.

Applying the Quantum Fourier Transform (QFT) reveals the period of the function.

From this period, the private key can be recovered efficiently.

Thus a sufficiently powerful quantum computer would break ECC-based cryptographic systems.



## Post-Quantum Alternative: Hash-Based Signatures

Hash-based signatures do not rely on algebraic group structures.

Instead, they rely only on cryptographic hash functions.

Private key:

S = {s₁, s₂, … , sₖ}

Public key:

P = {H(s₁), H(s₂), … , H(sₖ)}

Because hash functions do not exhibit periodic structure, Shor’s algorithm cannot be applied.

Quantum computers only provide a quadratic speedup against brute-force hash attacks via Grover’s algorithm, which can be mitigated by increasing hash size.


## Merkle Tree Aggregation

One-time signatures can only be used once.

Merkle trees allow many one-time keys to be combined into a single public root.

Leaf nodes

Lᵢ = H(PKᵢ)

Internal nodes

N = H(Nₗ || Nᵣ)

Merkle root

Root = {top hash}

The root acts as the public key for the entire signature system.

Verification reconstructs the root using an authentication path.


## Security Model

Classical Security Assumptions

Elliptic curve cryptography relies on the hardness of the ECDLP under classical computation.


Quantum Threat Model

A large-scale quantum computer could apply Shor’s algorithm to recover private keys from public keys.

This would compromise blockchain systems relying on elliptic curve signatures.


Post-Quantum Security

Hash-based signatures rely on:

- preimage resistance
- second-preimage resistance
- collision resistance

These properties remain secure even in the presence of quantum computing.


## Running the Project

Install dependencies:

pip install -r requirements.txt

Run the application:

python main.py

Optional quantum simulation backends:
- Qiskit
- Cirq

If these frameworks are not installed, the simulator falls back to a classical demonstration.


## Educational Disclaimer

This project intentionally uses very small cryptographic parameters and simplified implementations.

It is not secure and must not be used in production systems.

The goal is to illustrate the conceptual impact of quantum computing on blockchain cryptography.


## References

Foundational research related to this project includes:

- Algorithms for Quantum Computation: Discrete Logarithms and Factoring
-	National Institute of Standards and Technology Post-Quantum Cryptography Standardization Project
- XMSS
- SPHINCS+


## License

MIT License

