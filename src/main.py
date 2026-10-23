"""Command-line entry point for QuantumGreen AI."""

import argparse
from .optimizer import make_demo_data, solve_classical, solve_qaoa


def main():
    parser = argparse.ArgumentParser(
        description="Demonstrate energy scheduling with QuantumGreen AI."
    )
    parser.add_argument(
        "--qaoa",
        action="store_true",
        help="Run the QAOA experiment on the Qiskit Aer simulator.",
    )
    args = parser.parse_args()

    data = make_demo_data()
    print("QuantumGreen AI - energy scheduling demonstration")
    print("\nInput data:")
    print(data.to_string(index=False))

    print("\nClassical optimizer:")
    print(solve_classical(data))

    if args.qaoa:
        print("\nQAOA simulator experiment:")
        print(solve_qaoa(data))


if __name__ == "__main__":
    main()
