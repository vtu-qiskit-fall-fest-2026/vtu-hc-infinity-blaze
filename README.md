<div align="center">

# Infinity Blaze

**VTU-QFF-HC-0185** &nbsp;|&nbsp; Tier: **Online**

</div>

---

<div align="center">

| | |
| :--- | :--- |
| **Team** | Infinity Blaze |
| **Team ID** | VTU-QFF-HC-0185 |
| **Tier** | Online |
| **Repository** | [vtu-hc-infinity-blaze](https://github.com/vtu-qiskit-fall-fest-2026/vtu-hc-infinity-blaze.git) |
| **Organisation** | [vtu-qiskit-fall-fest-2026](https://github.com/vtu-qiskit-fall-fest-2026) |
| **Event** | VTU-QFF Hackathon — VTU-Qiskit Fall Fest 2026 |

</div>

---

## 📌 Table of Contents

- [Team Members](#-team-members-github-ids)
- [Problem Statement](#-problem-statement)
- [Proposed Solution](#-proposed-solution)
- [Approach & Architecture](#-approach--architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How to Run](#-how-to-run)
- [How to Push Code](#-how-to-push-code)
- [Submission Checklist](#-submission-checklist)
- [Resources](#-resources)
- [License](#-license)

---

## 👥 Team Members (GitHub IDs)

> Members are added to this repository as **collaborators** and must accept the
> GitHub invitation before they can push. Add your GitHub username below.

| # | Name | GitHub Username | Role |
| :-- | :--- | :--- | :--- |
| 1 | Purvesh Sudhir Raghatate | Purvesh-07 | Team Lead |
| 2 | Sahil Subhash Jadhao | sjadhao2207-eng! | Developer |
| 3 | Manish Balgovind Rajak | manish-2424 | Developer |

<!--
Optional: add a plain list instead of the table above.
- @username1
- @username2
-->

---

## ❓ Problem Statement

<!--
State the problem you are solving. Be specific: what is broken or missing,
who experiences it, and why does it matter. Link to the official problem
statement from the brief if one applies.
-->

**Problem:** Inefficient renewable energy utilization and electricity scheduling

**Why it matters:** Better energy scheduling can reduce electricity costs, improve the utilization of renewable energy, and support lower-carbon energy systems. This project explores whether quantum optimization techniques can help solve energy-scheduling problems as their complexity grows.

**Track / Category:** Online  · Track 1 · Quantum Applications for Climate Change and Sustainability

---

## 💡 Proposed Solution

<!--
Describe your solution. Keep it concrete: the core idea, the user flow, and
the quantum/ML technique you are applying.
-->

**Solution:** QuantumGreen AI is a Streamlit-based energy optimization prototype that schedules flexible electricity demand across different time slots using solar generation data and electricity prices. It compares an exact classical optimization baseline with a quantum-inspired workflow implemented using the Quantum Approximate Optimization Algorithm (QAOA) and a local quantum circuit simulator. The dashboard presents the selected time slots, estimated grid electricity cost, feasibility, and quantum measurement results.

**Key idea:** Use a QAOA quantum circuit with a cost-based phase separator and mixer operations to sample candidate energy schedules, then compare the best feasible candidate against an exact classical optimizer.

**Why this works:** 

1) Cost-aware scheduling: Electricity prices and solar generation influence the preferred time slots.

2) Constraint handling: A penalty term discourages schedules that select the wrong number of time slots.

3) Measurable evaluation: The classical optimizer checks every possible schedule in the four-slot example, providing an exact reference for QAOA.

4) Accessible visualization: A Streamlit dashboard makes the results easy to inspect and demonstrate.

Scientific note: The current prototype uses synthetic data and a classical simulator of quantum circuits. It does not establish quantum advantage, and its initial implementation schedules flexible loads rather than battery charging and discharging.

---

## 🧩 Approach & Architecture

<!--
Walk through how it works. A simple pipeline diagram in text or Mermaid is ideal.
-->

```mermaid
flowchart LR
    A[Energy inputs] --> B[Preprocessing]
    B --> C[Binary optimization model]
    C --> D[QAOA circuit simulation]
    D --> E[Measurement and decoding]
    E --> F[Feasibility and cost scoring]
    F --> G[Classical comparison]
    G --> H[Dashboard visualization]
```

 Energy inputs → Preprocessing → Binary optimization model → QAOA circuit simulation → Measurement and decoding → Feasibility and cost scoring → Classical comparison → Dashboard visualization.

1. **Input** — The current prototype uses a synthetic dataset with four time slots.
   
| Feature |	Format	| Example |
| :-- | :--- | :--- |
| Time slot	| String | 12:00 |
| Base electricity demand | kWh | 2.5 |
| Solar generation | kWh | 3.0 |
| Electricity price | ₹/kWh | 4.0 |
| Flexible-load decision |	Binary: 0 or 1 | 1 |

 For a real deployment, these inputs could come from smart meters, solar generation forecasts, and applicable electricity tariffs.

2. **Preprocessing** — • Organize the energy data into time slots.
   
• Represent each scheduling decision with a binary variable $$\(x_i\)$$.

• Interpret $$\(x_i=1\)$$ as scheduling one 1-kWh flexible-load block in slot $$\(i\)$$, and $$\(x_i=0\)$$ as not scheduling it.

• Calculate estimated grid imports using demand minus available solar generation, with a lower bound of zero.

3. **Quantum core** — The prototype uses a small, one-layer QAOA circuit simulated through Qiskit Aer.

 The objective function is:

```math
C(x) = \sum_{i=1}^{n} p_i \max(d_i + x_i - s_i, 0)
+ \lambda \left(\sum_{i=1}^{n} x_i - K\right)^2

 Where:
- $$\(p_i\)$$: electricity price in slot i.
  
- $$\(d_i\)$$: base demand.
  
- $$\(s_i\)$$: solar generation.
  
- $$\(x_i\)$$: binary flexible-load decision.
  
- $$\(K\)$$: required number of scheduled load blocks.
  
- $$\(\lambda\)$$: constraint penalty.
  
 The circuit applies a cost-based phase separator followed by mixer rotations. A classical optimizer adjusts the QAOA parameters to seek lower expected cost.

4. **Post-processing** — Measurement and scoring
   
- Measure the quantum circuit to obtain bitstrings.
  
- Decode each bitstring into a candidate schedule.
  
- Calculate its estimated electricity cost and constraint feasibility.
  
- Identify the best feasible candidate observed.
  
- Compare it with the exact classical optimum.
 
 Because QAOA is stochastic, it may not find the optimal schedule in every run.

5. **Output** — The Streamlit interface displays:
   
- Estimated grid electricity cost.
  
- Selected time slots for flexible loads.
  
- Schedule feasibility.
  
- QAOA measurement counts and feasible samples.
  
- Comparison against the exact classical result.
  
  
 The next development stage is to add battery state-of-charge constraints, real energy data, and a validated emissions model.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| Language | Python 3.11+ |
| Quantum SDK | Qiskit `>=1.0`, Qiskit Aer, Qiskit Runtime |
| Optimisation | Qiskit Optimization / COBYLA / SPSA |
| Simulation | AerSimulator (statevector / noisemodel) |
| Environment | JupyterLab / VS Code, `venv` |
| Version control | Git + GitHub |

---

## 📁 Project Structure

```text
vtu-hc-infinity-blaze/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata (optional)
├── .gitignore
├── notebooks/             # Jupyter notebooks for experiments
│   └── exploration.ipynb
├── src/
│   ├── __init__.py
│   ├── circuit.py         # Quantum circuit construction
│   ├── optimizer.py       # Optimization loop
│   └── main.py            # Entry point
├── data/                  # Datasets (use Git LFS for large files)
├── tests/                 # Unit tests
│   └── test_circuit.py
└── docs/                  # Notes, diagrams, reports
```

---

## 🚀 How to Run

### Prerequisites

- Python 3.11 or newer
- [Git](https://git-scm.com/downloads)
- A GitHub account (you need collaborator access to this repo)

### 1. Clone the repository

```bash
git clone https://github.com/vtu-qiskit-fall-fest-2026/vtu-hc-infinity-blaze.git
cd vtu-hc-infinity-blaze
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows (PowerShell)
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run

```bash
python -m src.main
```

Or launch the notebook workflow:

```bash
jupyter lab
```

### 5. Run the tests

```bash
pytest -q
```

---

## 🔁 How to Push Code

> Full walkthrough: **[Git & Collaboration Handbook](../vtu-hc-guide-git-and-collaboration)** — collaboration
> workflow, branches, pull requests, reviews and conflict resolution.

### Configure Git (first time only)

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

### Everyday workflow

```bash
# 1. Get the latest changes
git checkout main
git pull origin main

# 2. Create a branch for your work
git checkout -b feature/my-task

# 3. Commit your work
git add .
git commit -m "feat: add variational circuit for the search problem"

# 4. Push the branch
git push -u origin feature/my-task

# 5. Open a Pull Request on GitHub and request a review
#    https://github.com/vtu-qiskit-fall-fest-2026/vtu-hc-infinity-blaze/compare/main...feature/my-task

# 6. After approval, merge into main
git checkout main
git pull origin main
git branch -d feature/my-task
```

### Commit message convention

| Prefix | Meaning |
| :--- | :--- |
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `test:` | Adding or fixing tests |
| `refactor:` | Code restructure, no behaviour change |
| `chore:` | Build/config/dependency changes |

### Useful commands

```bash
git status              # what changed
git log --oneline -10   # recent commits
git diff                # review changes before committing
git stash               # shelve changes temporarily
git pull --rebase       # update your branch on top of main
```

### Collaborating on the same repo

- **Never push directly to `main`** — open a Pull Request.
- **Pull before you push** to avoid rejected commits.
- **Commit often** with clear messages.
- **Resolve conflicts** locally: `git pull --rebase`, fix the files, then `git add` + `git rebase --continue`.
- **Ask for a review** before merging — a second pair of eyes catches bugs fast.

---

## ✅ Submission Checklist

- [ ] Repository created and **public**
- [ ] All team members added as **collaborators** and invitations accepted
- [ ] `README.md` updated with project details, problem statement and solution
- [ ] Team members listed under [Team Members](#-team-members-github-ids)
- [ ] `requirements.txt` committed and project runs from a clean clone
- [ ] Code pushed to `main` and the latest `main` builds successfully
- [ ] Notebooks committed with **cleared outputs** (or use `nbstrip`)
- [ ] `README` includes a demo screenshot / video link
- [ ] Short project summary submitted on the hackathon portal

---

## 📚 Resources

| Resource | Link |
| :--- | :--- |
| 🔁 Git & collaboration handbook | [Git & Collaboration Handbook](../vtu-hc-guide-git-and-collaboration) |
| ❓ Problem statements, solutions & terms | [Problem Statements, Solutions & Terms](../vtu-hc-guide-problem-and-solution) |
| 📄 README writing guide | [README Guide & Template](../vtu-hc-guide-readme-template) |
| ⚛️ Qiskit documentation | https://docs.quantum.ibm.com/ |
| ⚛️ Qiskit Runtime & primitives | https://quantum.cloud.ibm.com/docs/ |
| 🧪 Qiskit Aer simulator | https://docs.quantum.ibm.com/guides/simulator |
| 💻 IBM Quantum Platform | https://quantum.cloud.ibm.com/ |
| 🎓 Qiskit textbook | https://qiskit.qotlabs.org/learning/ |
| 📋 GitHub Docs | https://docs.github.com/ |

---

## 📄 License

Released under the [MIT License](LICENSE). See `LICENSE` for details.

---

<div align="center">

**Infinity Blaze** · Team ID `VTU-QFF-HC-0185` · Tier `Online`
· Built with ⚛️ Qiskit for the VTU-QFF Hackathon

[⬆ Back to Top](#infinity-blaze)

</div>
