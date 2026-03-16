
"""
Project: Quantum-Safe Blockchain Demonstrator
Module: quantum_attack.py

Author: Davood Ziaeian-Pour
GitHub: https://github.com/pour-dev
Created: 2026-03-15
License: MIT

Description:
    Educational simulator demonstrating how a quantum-style attack could
    threaten classical elliptic-curve cryptography used in blockchain
    systems.

    The module implements a simplified simulation of the elliptic-curve
    discrete logarithm problem (ECDLP). Because current quantum computing
    frameworks do not provide a full implementation of Shor's algorithm
    for elliptic curves, this simulator illustrates the concept using
    small quantum circuits and a toy elliptic curve.

Attack Backends:
    1. Qiskit-based simulated quantum attack
    2. Cirq-based simulated quantum attack
    3. Classical brute-force fallback

    If quantum frameworks are available, the simulator builds a small
    circuit that demonstrates Shor-style period finding using a
    QFT-inspired structure. The measured value is then mapped to a
    candidate private key on the toy elliptic curve.

Classes:
    QuantumECDLPSimulator
        Demonstrates how quantum algorithms could recover private keys
        from elliptic-curve public keys on a toy curve.

Dependencies:
    - Python 3.9+
    - Optional: qiskit
    - Optional: cirq
    - numpy

Notes:
    This implementation is purely educational and does NOT implement
    a real quantum attack on elliptic curve cryptography.

    The elliptic curve parameters are intentionally very small so that
    attacks can be demonstrated quickly.
"""
from .elliptic_curve import ToyEllipticCurve


class QuantumECDLPSimulator:
    """
    Simulates a quantum-style attack on the toy elliptic curve.

    Backend priority:
    1) Qiskit-based simulated quantum attack (if available)
    2) Cirq-based simulated quantum attack (if available)
    3) Classical brute-force fallback (always available)

    This is an educational demonstration. It does NOT implement a real
    elliptic-curve Shor algorithm, because no such implementation exists
    in current quantum frameworks. Instead, it uses real quantum circuits
    (QFT-style) to illustrate the principle and then maps the result to
    the toy curve.

    Example:
        curve = ToyEllipticCurve()
        G = (1, 1)
        public_key = curve.mul(G, 3)

        simulator = QuantumECDLPSimulator(curve, G, public_key)
        private_key, backend = simulator.run_attack()

        print("Recovered key:", private_key)
        print("Backend used:", backend)
    """

    def __init__(self, curve: ToyEllipticCurve, G, public_key):
        self.curve = curve
        self.G = G
        self.public_key = public_key

    # ---------------------------------------------------------
    # MAIN ENTRY POINT
    # ---------------------------------------------------------
    def run_attack(self):
        """
        Returns:
            (private_key, backend_name)

        """
        # Try Qiskit first
        try:
            import qiskit  # noqa: F401
            key = self._run_qiskit_simulated_attack()
            return key, "Qiskit"
        except Exception:
            pass

        # Try Cirq second
        try:
            import cirq  # noqa: F401
            key = self._run_cirq_simulated_attack()
            return key, "Cirq"
        except Exception:
            pass

        # Fallback
        key = self._run_simulated_attack()
        return key, "Classical"

    # ---------------------------------------------------------
    # CLASSICAL FALLBACK
    # ---------------------------------------------------------
    def _run_simulated_attack(self):
        """
        Classical brute-force attack.

        Because the toy curve is extremely small, the private key can be
        found by exhaustively checking all possible values. This simulates
        the effect of a quantum attack in a didactic way.
        """
        for d in range(1, self.curve.order + 1):
            if self.curve.mul(self.G, d) == self.public_key:
                return d
        return None

    # ---------------------------------------------------------
    # QISKIT-BASED SIMULATED ATTACK
    # ---------------------------------------------------------
    def _run_qiskit_simulated_attack(self):
        """
        Qiskit-based simulated quantum attack.

        This does NOT solve the elliptic-curve discrete logarithm problem
        directly, because Qiskit does not provide an ECDLP implementation.

        Instead, this function builds a small quantum circuit that
        demonstrates the principle of Shor-style period finding (using
        superposition + QFT-like structure), then maps the measurement
        result to a candidate private key on the toy curve.
        """
        try:
            from qiskit import QuantumCircuit
            from qiskit_aer import AerSimulator
            import numpy as np
        except Exception:
            return self._run_simulated_attack()

        # 1. Build a small QFT-style circuit
        num_qubits = 3
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Put all qubits into superposition
        qc.h(range(num_qubits))

        # Apply a simple QFT-like pattern
        for i in range(num_qubits):
            qc.h(i)
            for j in range(i + 1, num_qubits):
                angle = np.pi / (2 ** (j - i))
                qc.cp(angle, j, i)

        qc.measure(range(num_qubits), range(num_qubits))

        # 2. Run on Aer simulator
        sim = AerSimulator()
        result = sim.run(qc, shots=1).result()
        counts = result.get_counts()
        measured_bitstring = list(counts.keys())[0]
        measured = int(measured_bitstring, 2)

        # 3. Map measurement to a valid private key
        d_guess = measured % self.curve.order
        if d_guess == 0:
            d_guess = 1

        # 4. Validate guess on the toy curve
        if self.curve.mul(self.G, d_guess) == self.public_key:
            return d_guess

        # If guess fails, fall back to brute-force
        return self._run_simulated_attack()

    # ---------------------------------------------------------
    # CIRQ-BASED SIMULATED ATTACK
    # ---------------------------------------------------------
    def _run_cirq_simulated_attack(self):
        """
        Cirq-based simulated quantum attack.

        This does NOT solve the elliptic-curve discrete logarithm problem
        directly, because Cirq does not provide an ECDLP implementation.

        Instead, this function builds a small quantum circuit that
        demonstrates the principle of Shor-style period finding, then
        maps the measurement result to a candidate private key on the
        toy curve.
        """
        try:
            import cirq
            import numpy as np
        except Exception:
            return self._run_simulated_attack()

        # 1. Build a small QFT-style circuit
        num_qubits = 3
        qubits = cirq.LineQubit.range(num_qubits)
        circuit = cirq.Circuit()

        # Put all qubits into superposition
        circuit.append(cirq.H.on_each(*qubits))

        # Apply a simple QFT-like pattern
        for i in range(num_qubits):
            circuit.append(cirq.H(qubits[i]))
            for j in range(i + 1, num_qubits):
                angle = np.pi / (2 ** (j - i))
                # Use CZ with fractional exponent to mimic controlled phase
                circuit.append(cirq.CZ(qubits[j], qubits[i]) ** (angle / np.pi))

        # Measure
        circuit.append(cirq.measure(*qubits, key="result"))

        # 2. Run on Cirq simulator
        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=1)
        bits = result.measurements["result"][0]
        measured = int(bits.dot(1 << np.arange(num_qubits)))

        # 3. Map measurement to a valid private key
        d_guess = measured % self.curve.order
        if d_guess == 0:
            d_guess = 1

        # 4. Validate guess on the toy curve
        if self.curve.mul(self.G, d_guess) == self.public_key:
            return d_guess

        # If guess fails, fall back to brute-force
        return self._run_simulated_attack()