import unittest

from qiskit.circuit import Parameter
from qiskit.circuit.library import Diagonal

from src.circuit import build_qaoa_circuit


class TestQAOACircuit(unittest.TestCase):
    def test_builds_two_qubit_circuit(self):
        energies = {0: 0.0, 1: 1.0, 2: 2.0, 3: 3.0}
        circuit = build_qaoa_circuit(energies)

        self.assertEqual(circuit.num_qubits, 2)
        self.assertEqual(circuit.num_clbits, 0)
        self.assertEqual(len(circuit.parameters), 2)

    def test_measurements_are_optional(self):
        energies = {0: 0.0, 1: 1.0}
        circuit = build_qaoa_circuit(energies, measure=True)

        self.assertEqual(circuit.num_qubits, 1)
        self.assertEqual(circuit.num_clbits, 1)

    def test_rejects_invalid_state_count(self):
        with self.assertRaises(ValueError):
            build_qaoa_circuit({0: 0.0, 1: 1.0, 2: 2.0})


if __name__ == "__main__":
    unittest.main()
