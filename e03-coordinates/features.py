import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e02-hand-tracking"))
from hand_tracker import HandTracker

pontas = [4, 8, 12, 16, 20]
medio = [2, 6, 10, 14, 18]

def vetor(p1,p2):

    v1 = np.array([p1.x, p1.y, p1.z])
    v2 = np.array([p2.x, p2.y, p2.z])

    return v2 - v1

def angulo(p1,p2,p3):

    u = vetor(p2,p1)
    v = vetor(p2,p3)

    cos_theta = np.dot(u,v) / (np.linalg.norm(u) * np.linalg.norm(v))
    cos_theta = max(-1.0, min(1.0, cos_theta))

    rad = np.arccos(cos_theta)
    return np.degrees(rad)

if __name__ == "__main__":
    class P:
        def __init__(self, x, y, z=0):
            self.x = x
            self.y = y
            self.z = z

    p1 = P(1, 0)
    p2 = P(0, 0)
    p3 = P(0, 1)

    print(angulo(p1, p2, p3))
    # dedo reto: três pontos quase em linha → perto de 180
    print(angulo(P(1, 0), P(0, 0), P(-1, 0)))   # espera ~180

    # dedo fechado: as duas setas quase na mesma direção → perto de 0
    print(angulo(P(1, 0), P(0, 0), P(1, 0.001)))  # espera perto de 0