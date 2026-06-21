import os
import sys
import cv2

# importar angulo do features.py (mesma pasta)
from features import angulo

# importar HandTracker e VideoLoop (outras pastas — padrão sys.path do E2)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e02-hand-tracking"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e01-webcam"))
from hand_tracker import HandTracker
from video_loop import VideoLoop

tracker = HandTracker()

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
        for i, (nome, (a, b, c)) in enumerate(DEDOS.items()):
            ang = angulo(lm[a], lm[b], lm[c])
            y = 110 + i * 40
            cv2.putText(frame, f"{ang:.0f}", (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return frame

VideoLoop().run(process_frame=process)