import os
import sys
import cv2
import numpy as np
from collections import deque

from features import distancia,angulo

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e02-hand-tracking"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e01-webcam"))
from hand_tracker import HandTracker
from video_loop import VideoLoop


class FeatureExtractor:
    def __init__(self, tracker, janela=5):
        self.tracker = tracker
        self.buffer_pinca = deque(maxlen=janela)
        self.DEDOS = {
            "indicador": (5, 6, 8),
            "medio":     (9, 10, 12),
            "anelar":    (13, 14, 16),
            "minimo":    (17, 18, 20),
        }

    def extract(self, frame):
        frame = self.tracker(frame)
        lm = self.tracker.last_landmarks
        if lm is None:
            return frame, None

        pinca_crua = distancia(lm[4], lm[8]) / distancia(lm[0], lm[9])
        self.buffer_pinca.append(pinca_crua)
        pinca_suave = sum(self.buffer_pinca) / len(self.buffer_pinca)

        features = {"pinca": pinca_suave, "pinca_crua": pinca_crua}
        for nome, (a, b, c) in self.DEDOS.items():
            features[f"ang_{nome}"] = angulo(lm[a], lm[b], lm[c])
        return frame, features

if __name__ == "__main__":
    GX, GY = 10, 300
    GW, GH = 200, 100
    PINCA_MIN, PINCA_MAX = 0.0, 1.2

    tracker = HandTracker()
    extractor = FeatureExtractor(tracker)
    hist_crua = deque(maxlen=100)
    hist_suave = deque(maxlen=100)

    def process(frame):
        frame, feats = extractor.extract(frame)
        if feats is not None:
            hist_crua.append(feats["pinca_crua"])
            hist_suave.append(feats["pinca"])

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

        cv2.rectangle(frame, (GX, GY), (GX+GW, GY+GH), (50, 50, 50), -1)
        desenha_curva(hist_crua, (0, 0, 255))     # crua: vermelho
        desenha_curva(hist_suave, (0, 255, 0))    # suave: verde

        return frame

    VideoLoop().run(process_frame=process)