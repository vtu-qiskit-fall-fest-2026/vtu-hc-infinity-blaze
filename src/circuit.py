"""Parameterized QAOA circuit construction for energy scheduling."""

import math

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


def build_qaoa_circuit(energies, gamma=None, beta=None, measure=False):
    """Build a one-layer QAOA circuit from a complete energy table.

    energies maps integer basis-state indices to real-valued costs.
    The cost phase is implemented using an exact Z-string decomposition.
    This is intended for small simulator-based experiments.
    """
    if not energies:
        raise ValueError("energies must not be empty")

    n_states = len(energies)
    n = n_states.bit_length() - 1

    if n < 1 or 2**n != n_states:
        raise ValueError("energies must contain exactly 2**n states")

    if set(energies) != set(range(n_states)):
        raise ValueError("energies must have every state index from 0 to 2**n - 1")

    costs = [float(energies[i]) for i in range(n_states)]
    if not all(math.isfinite(cost) for cost in costs):
        raise ValueError("all energy values must be finite")

    gamma = gamma if gamma is not None else Parameter("gamma")
    beta = beta if beta is not None else Parameter("beta")

    circuit = QuantumCircuit(n, n) if measure else QuantumCircuit(n)

    # Initial equal superposition.
    for qubit in range(n):
        circuit.h(qubit)

    # Walsh-Z transform: express the diagonal cost as a sum of Z strings.
    # This lets us construct the cost phase with parameterized RZ/CX gates.
    for mask in range(n_states):
        coefficient = sum(
            costs[state] * (-1 if (state & mask).bit_count() % 2 else 1)
            for state in range(n_states)
        ) / n_states

        if abs(coefficient) < 1e-12:
            continue

        qubits = [q for q in range(n) if (mask >> q) & 1]

        if not qubits:
            circuit.global_phase -= gamma * coefficient
            continue

        # Compute the parity onto the final qubit.
        for control, target in zip(qubits[:-1], qubits[1:]):
            circuit.cx(control, target)

        circuit.rz(2 * gamma * coefficient, qubits[-1])

        # Uncompute the parity.
        for control, target in reversed(list(zip(qubits[:-1], qubits[1:]))):
            circuit.cx(control, target)

    # QAOA mixer.
    for qubit in range(n):
        circuit.rx(2 * beta, qubit)

    if measure:
        circuit.measure(range(n), range(n))

    return circuit
