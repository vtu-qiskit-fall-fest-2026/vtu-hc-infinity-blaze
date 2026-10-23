from itertools import product
import numpy as np
import pandas as pd

def make_demo_data():
    return pd.DataFrame({
        "time": ["06:00", "12:00", "18:00", "22:00"],
        "base_demand_kwh": [2.0, 2.5, 3.5, 2.0],
        "solar_kwh": [0.3, 3.0, 0.6, 0.0],
        "price_inr_kwh": [5.0, 4.0, 9.0, 6.0],
    })

def _cost_for_bits(bits, data, flexible_kwh, penalty):
    bits = np.asarray(bits, dtype=int)
    base = data["base_demand_kwh"].to_numpy(dtype=float)
    solar = data["solar_kwh"].to_numpy(dtype=float)
    prices = data["price_inr_kwh"].to_numpy(dtype=float)
    grid = np.maximum(base + bits - solar, 0.0)
    energy_cost = float(np.dot(grid, prices))
    violation = int(bits.sum()) - int(flexible_kwh)
    return energy_cost + penalty * violation * violation, energy_cost, violation == 0

def solve_classical(data, flexible_kwh=2, penalty=8.0):
    candidates = []
    for bits in product([0, 1], repeat=len(data)):
        score, energy_cost, feasible = _cost_for_bits(bits, data, flexible_kwh, penalty)
        candidates.append((score, energy_cost, feasible, bits))
    feasible_candidates = [x for x in candidates if x[2]]
    best = min(feasible_candidates or candidates, key=lambda x: x[1] if x[2] else x[0])
    bits = best[3]
    return {
        "cost": float(best[1]),
        "objective": float(best[0]),
        "feasible": bool(best[2]),
        "selected_slots": [str(data.iloc[i]["time"]) for i, bit in enumerate(bits) if bit],
        "bits": list(bits),
    }

def evaluate_battery_schedule(data, battery_capacity=5.0, max_kw=2.0, efficiency=0.90):
    soc = battery_capacity * 0.5
    soc_history = [soc]
    battery_actions = []

    prices = data["price_inr_kwh"].to_numpy()
    solar = data["solar_kwh"].to_numpy()
    demand = data["base_demand_kwh"].to_numpy()

    for sol, dem, price in zip(solar, demand, prices):
        if sol > dem and soc < battery_capacity:
            action = "Charge"
            power = min(max_kw, battery_capacity - soc, sol - dem)
            soc += power * efficiency
        elif price >= 7.0 and soc > 0.5:
            action = "Discharge"
            power = min(max_kw, soc, dem)
            soc -= power / efficiency
        else:
            action = "Idle"
        battery_actions.append(action)
        soc_history.append(soc)

    return battery_actions, soc_history

def solve_qaoa(data, flexible_kwh=2, penalty=8.0, shots=1024):
    from qiskit import QuantumCircuit, transpile
    from qiskit.circuit import Parameter
    from qiskit.circuit.library import Diagonal
    from qiskit_aer import AerSimulator
    from scipy.optimize import minimize

    n = len(data)
    if n > 8:
        raise ValueError("This demonstration supports at most 8 time slots.")
    states = list(product([0, 1], repeat=n))

    energies = {}
    for bits in states:
        score, _, _ = _cost_for_bits(bits, data, flexible_kwh, penalty)
        energies[sum(int(b) << i for i, b in enumerate(bits))] = score

    reps = 1
    gammas = [Parameter(f"gamma_{i}") for i in range(reps)]
    betas = [Parameter(f"beta_{i}") for i in range(reps)]

    def circuit_for(params, measure=False):
        qc = QuantumCircuit(n, n) if measure else QuantumCircuit(n)
        for q in range(n):
            qc.h(q)
        for layer in range(reps):
            diag_phases = [np.exp(-1j * params[layer] * float(energies[i])) for i in range(2**n)]
            diag_gate = Diagonal(diag_phases)
            qc.append(diag_gate, list(range(n)))
            for q in range(n):
                qc.rx(2 * params[reps + layer], q)
        if measure:
            qc.measure(range(n), range(n))
        return qc

    def expected_cost(params):
        qc = circuit_for(params, measure=True)
        backend = AerSimulator()
        tqc = transpile(qc, backend)
        counts = backend.run(tqc, shots=max(256, shots // 4)).result().get_counts()
        total = sum(counts.values())
        return sum(energies[int(bitstring, 2)] * count for bitstring, count in counts.items()) / total

    rng = np.random.default_rng(7)
    initial = rng.uniform(0.1, 1.0, size=2 * reps)
    result = minimize(expected_cost, initial, method="COBYLA", options={"maxiter": 35, "rhobeg": 0.3})

    qc = circuit_for(result.x, measure=True)
    backend = AerSimulator()
    counts = backend.run(transpile(qc, backend), shots=int(shots)).result().get_counts()

    decoded = []
    feasible_samples = 0
    for bitstring, count in counts.items():
        bits = tuple(int(ch) for ch in bitstring[::-1])
        score, energy_cost, feasible = _cost_for_bits(bits, data, flexible_kwh, penalty)
        if feasible:
            feasible_samples += count
            decoded.append((energy_cost, bits, count))

    if decoded:
        cost, bits, _ = min(decoded, key=lambda item: item[0])
        feasible = True
    else:
        observed = []
        for bitstring, count in counts.items():
            bits0 = tuple(int(ch) for ch in bitstring[::-1])
            score, energy_cost, ok = _cost_for_bits(bits0, data, flexible_kwh, penalty)
            observed.append((score, energy_cost, ok, bits0))
        _, cost, feasible, bits = min(observed, key=lambda x: x[0])

    return {
        "cost": float(cost),
        "feasible": bool(feasible),
        "selected_slots": [str(data.iloc[i]["time"]) for i, bit in enumerate(bits) if bit],
        "bits": list(bits),
        "counts": counts,
        "feasible_samples": int(feasible_samples),
        "backend": "Qiskit AerSimulator (classical simulation)",
        "reps": reps,
    }
