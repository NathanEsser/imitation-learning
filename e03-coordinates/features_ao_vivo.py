import os
import sys
import cv2
from collections import deque
import numpy as np

# importar angulo do features.py (mesma pasta)
from features import angulo, distancia

# importar HandTracker e VideoLoop (outras pastas — padrão sys.path do E2)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e02-hand-tracking"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e01-webcam"))
from hand_tracker import HandTracker
from video_loop import VideoLoop

tracker = HandTracker()
hist_pinca = deque(maxlen=100)

# parâmetros do retângulo do gráfico
GX, GY = 10, 300        # canto superior-esquerdo
GW, GH = 200, 100       # largura, altura
PINCA_MIN, PINCA_MAX = 0.0, 1.2   # faixa esperada da pinça

DEDOS = {
    "indicador": (5, 6, 8),
    "medio":     (9, 10, 12),
    "anelar":    (13, 14, 16),
    "minimo":    (17, 18, 20),
}

def process(frame):
    frame = tracker(frame)
    lm = tracker.last_landmarks
    if lm is not None:
        pinca = distancia(lm[4], lm[8]) / distancia(lm[0], lm[9])
        hist_pinca.append(pinca)

    # desenha o retângulo de fundo
    cv2.rectangle(frame, (GX, GY), (GX+GW, GY+GH), (50, 50, 50), -1)

    # converte cada valor do histórico num ponto
    pontos = []
    for i, val in enumerate(hist_pinca):
        x = GX + int(i / hist_pinca.maxlen * GW)
        val_c = max(PINCA_MIN, min(PINCA_MAX, val))
        fracao = (val_c - PINCA_MIN) / (PINCA_MAX - PINCA_MIN)
        y = (GY + GH) - int(fracao * GH)
        pontos.append((x, y))

    if len(pontos) > 1:
        cv2.polylines(frame, [np.array(pontos)], False, (0, 255, 0), 2)

    return frame

VideoLoop().run(process_frame=process)