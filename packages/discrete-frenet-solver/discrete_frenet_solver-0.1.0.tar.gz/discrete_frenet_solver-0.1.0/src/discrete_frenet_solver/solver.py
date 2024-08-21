import numpy as np

def solve_frenet_frame(curve, epsilon=1e-8):
    curve = np.asarray(curve)
    
    # Calculate T (tangent)
    T = np.gradient(curve, axis=0)
    T_norms = np.linalg.norm(T, axis=1)
    T = T / T_norms[:, np.newaxis]
    
    # Identify straight segments
    is_straight = T_norms < epsilon
    
    # Calculate N (normal) for non-straight parts
    dT = np.gradient(T, axis=0)
    N = dT - np.sum(dT * T, axis=1)[:, np.newaxis] * T
    N_norms = np.linalg.norm(N, axis=1)
    
    # Handle points where the normal is undefined or in straight segments
    undefined_N = (N_norms < epsilon) | is_straight
    
    if np.all(undefined_N):
        print("the entire curve is straight")
        # If the entire curve is straight, choose an arbitrary normal
        N = np.zeros_like(T)
        N[:, 0] = T[:, 1]
        N[:, 1] = -T[:, 0]
        N = N / np.linalg.norm(N, axis=1)[:, np.newaxis]
    elif np.any(undefined_N):
        print("handling straight parts")
        # Only proceed with interpolation if there are any straight parts
        # Find segments of curved and straight parts
        segment_changes = np.where(np.diff(undefined_N))[0] + 1
        segments = np.split(np.arange(len(curve)), segment_changes)
        
        for segment in segments:
            if undefined_N[segment[0]]:
                # This is a straight segment
                left_curved = np.where(~undefined_N[:segment[0]])[0]
                right_curved = np.where(~undefined_N[segment[-1]+1:])[0] + segment[-1] + 1
                
                if len(left_curved) > 0 and len(right_curved) > 0:
                    # Interpolate between left and right curved parts
                    left_N = N[left_curved[-1]]
                    right_N = N[right_curved[0]]
                    t = np.linspace(0, 1, len(segment))
                    N[segment] = (1-t[:, np.newaxis]) * left_N + t[:, np.newaxis] * right_N
                elif len(left_curved) > 0:
                    # Use normal from left curved part
                    N[segment] = N[left_curved[-1]]
                elif len(right_curved) > 0:
                    # Use normal from right curved part
                    N[segment] = N[right_curved[0]]
                else:
                    # No curved parts found, use arbitrary normal
                    N[segment] = np.array([T[segment[0]][1], -T[segment[0]][0], 0])
                
                # Ensure N is perpendicular to T
                N[segment] = N[segment] - np.sum(N[segment] * T[segment], axis=1)[:, np.newaxis] * T[segment]
                N[segment] = N[segment] / np.linalg.norm(N[segment], axis=1)[:, np.newaxis]
    else:
        print("no straight parts")
    
    # If there are no straight parts, N is already calculated correctly for all points
    
    # Calculate B (binormal) ensuring orthogonality
    B = np.cross(T, N)
    
    # Ensure perfect orthogonality through Gram-Schmidt
    N = N - np.sum(N * T, axis=1)[:, np.newaxis] * T
    N = N / np.linalg.norm(N, axis=1)[:, np.newaxis]
    
    B = B - np.sum(B * T, axis=1)[:, np.newaxis] * T
    B = B - np.sum(B * N, axis=1)[:, np.newaxis] * N
    B = B / np.linalg.norm(B, axis=1)[:, np.newaxis]
    
    return T, N, B