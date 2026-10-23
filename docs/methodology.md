# Methodology and limitations

## Problem

The prototype explores selecting time slots for flexible electrical loads using solar generation, demand, and electricity prices.

## Classical baseline

The classical solver enumerates binary scheduling candidates and evaluates their estimated grid-energy cost. A penalty term discourages schedules that violate the requested number of selected slots.

## QAOA experiment

The QAOA experiment constructs a cost-dependent phase separator, applies mixer rotations, and samples candidate schedules using Qiskit Aer. Aer is a classical simulator. The experiment is limited to small scheduling instances because enumerating all basis-state energies grows exponentially with the number of decision bits.

## Battery demonstration

The battery example uses a simplified state-of-charge update and illustrative charge/discharge rules. It is not a complete physical battery model and does not account for all operational constraints.

## Evaluation plan

Future evaluation should compare classical and QAOA results on identical instances, report feasibility and objective values, measure runtime, test multiple random seeds, and use realistic local energy data. Any carbon estimates should use documented regional emissions factors.
