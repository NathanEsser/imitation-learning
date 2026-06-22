import os
import sys
import cv2
from collections import deque
import numpy as np

# importar angulo do features.py (mesma pasta)
from features import distancia

# importar HandTracker e VideoLoop (outras pastas — padrão sys.path do E2)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e02-hand-tracking"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e01-webcam"))
from hand_tracker import HandTracker
from video_loop import VideoLoop

tracker = HandTracker()
hist_crua = deque(maxlen=100)
hist_suave = deque(maxlen=100)
buffer_pinca = deque(maxlen=5)

# parâmetros do retângulo do gráfico
GX, GY = 10, 300        # canto superior-esquerdo
GW, GH = 200, 100       # largura, altura
PINCA_MIN, PINCA_MAX = 0.0, 1.2   # faixa esperada da pinça

def process(frame):
    frame = tracker(frame)
    lm = tracker.last_landmarks
    if lm is not None:
        pinca_crua = distancia(lm[4], lm[8]) / distancia(lm[0], lm[9])
        buffer_pinca.append(pinca_crua)
        pinca_suave = sum(buffer_pinca) / len(buffer_pinca)
        hist_crua.append(pinca_crua)    
        hist_suave.append(pinca_suave)  

    # desenha o retângulo de fundo
    cv2.rectangle(frame, (GX, GY), (GX+GW, GY+GH), (50, 50, 50), -1)

    # converte cada valor do histórico num ponto
    def desenha_curva(historico, cor):
        pontos = []
        for i, val in enumerate(historico):
            x = GX + int(i / historico.maxlen * GW)
            val_c = max(PINCA_MIN, min(PINCA_MAX, val))
            fracao = (val_c - PINCA_MIN) / (PINCA_MAX - PINCA_MIN)
            y = (GY + GH) - int(fracao * GH)
            pontos.append((x, y))
        if len(pontos) > 1:
            cv2.polylines(frame, [np.array(pontos)], False, cor, 2)

    desenha_curva(hist_crua, (0, 0, 255))     # crua: vermelho
    desenha_curva(hist_suave, (0, 255, 0))    # suave: verde

    return frame

VideoLoop().run(process_frame=process)