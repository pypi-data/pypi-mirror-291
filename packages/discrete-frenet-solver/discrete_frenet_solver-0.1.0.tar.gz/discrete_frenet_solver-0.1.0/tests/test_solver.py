import numpy as np
from discrete_frenet_solver import solve_frenet_frame

def test_straight_line():
    curve = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]])
    T, N, B = solve_frenet_frame(curve)
    assert np.allclose(T, np.array([[1, 0, 0]] * 3))
    assert np.allclose(N, np.array([[0, 1, 0]] * 3))
    assert np.allclose(B, np.array([[0, 0, 1]] * 3))

def test_orthogonality():
    curve = np.array([[0, 0, 0], [1, 1, 1], [2, 0, 2], [3, -1, 1]])
    T, N, B = solve_frenet_frame(curve)
    for t, n, b in zip(T, N, B):
        assert np.isclose(np.dot(t, n), 0)
        assert np.isclose(np.dot(t, b), 0)
        assert np.isclose(np.dot(n, b), 0)