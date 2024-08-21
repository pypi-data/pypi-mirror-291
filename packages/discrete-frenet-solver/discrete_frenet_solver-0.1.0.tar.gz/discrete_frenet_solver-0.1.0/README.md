# DiscreteFrenetSolver

DiscreteFrenetSolver is a Python package for computing the discrete Frenet frame (TNB frame) of a curve with numerical corrections. It handles edge cases such as straight segments and ensures orthogonality of the resulting frame for discrete curve data.

## Installation

pip install discrete-frenet-solver

## Usage

```python
import numpy as np
from discrete_frenet_solver import solve_frenet_frame

# Define your discrete curve
curve = np.array([[0, 0, 0], [1, 1, 1], [2, 0, 2], [3, -1, 1]])

# Solve for the Frenet frame
T, N, B = solve_frenet_frame(curve)

print("Tangent vectors:", T)
print("Normal vectors:", N)
print("Binormal vectors:", B)