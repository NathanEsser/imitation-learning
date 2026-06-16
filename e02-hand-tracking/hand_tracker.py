import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

# Conexões (ossos) entre landmarks, agrupadas por dedo.
FINGER_CHAINS = {
    "polegar":   [0, 1, 2, 3, 4],
    "indicador": [0, 5, 6, 7, 8],
    "medio":     [0, 9, 10, 11, 12],
    "anelar":    [0, 13, 14, 15, 16],
    "minimo":    [0, 17, 18, 19, 20],
}

# Uma cor (BGR) por dedo — para VER a estrutura, não só pontos brancos.
FINGER_COLORS = {
    "polegar":   (255, 0, 0),     # azul
    "indicador": (0, 255, 0),     # verde
    "medio":     (0, 255, 255),   # amarelo
    "anelar":    (0, 128, 255),   # laranja
    "minimo":    (255, 0, 255),   # magenta
}

class HandTracker:
    def __init__(self, max_hands = 2, det_conf = 0.6, track_conf = 0.6):
        # Caminho do modelo, resolvido a partir da localização DESTE arquivo.
        # Sobe um nível (..) da pasta e02-hand-tracking até a raiz, entra em models/.
        
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "models", "hand_landmarker.task"
        )
        
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=det_conf,
            min_tracking_confidence=track_conf,
        )

        self.landmarker = vision.HandLandmarker.create_from_options(options)

        self.last_landmarks = None
        self.last_handedness = None
    
    def __call__(self, frame):
        return self.process(frame)

    def process(self, frame):
        #A Tasks API não aceita o array BGR do OpenCV cru.
        #Precisa: converter BGR->RGB e embrulhar num mp.Image.
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        #Modo VIDEO exige um timestamp em milissegundos, sempre CRESCENTE.
        timestamp_ms = int(time.time() * 1000)
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if not result.hand_landmarks:
            self.last_landmarks = None
            self.last_handedness = None
            cv2.putText(frame, "nenhuma mao", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return frame

        # Guarda a primeira mao para o E3 consumir depois (compatibilidade).
        self.last_landmarks = result.hand_landmarks[0]
        self.last_handedness = (result.handedness[0][0].category_name
                                if result.handedness else None)

        # Desenha TODAS as maos detectadas, com o rotulo Left/Right de cada uma.
        for i, hand in enumerate(result.hand_landmarks):
            self._draw(frame, hand)
            if result.handedness:
                label = result.handedness[i][0].category_name
                # Posiciona o rotulo perto do pulso (landmark 0) daquela mao.
                h, w = frame.shape[:2]
                wrist = hand[0]
                cv2.putText(frame, label,
                            (int(wrist.x * w), int(wrist.y * h) + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return frame
    
    def _draw(self, frame, landmarks):

        h, w = frame.shape[:2]

        # Converte coordenadas normalizadas (0-1) para pixels.
        pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

        # Ossos: liga os pontos em sequencia dentro de cada dedo.
        for finger, chain in FINGER_CHAINS.items():
            color = FINGER_COLORS[finger]
            for a, b in zip(chain, chain[1:]):
                cv2.line(frame, pts[a], pts[b], color, 2)

        # Juntas: um circulo em cada ponto.
        for finger, chain in FINGER_CHAINS.items():
            color = FINGER_COLORS[finger]
            for idx in chain:
                cv2.circle(frame, pts[idx], 5, color, -1)

        # Pulso (indice 0) em branco, maior.
        cv2.circle(frame, pts[0], 8, (255, 255, 255), -1)

        tip = landmarks[8]
        cv2.putText(frame, f"({tip.x:.2f}, {tip.y:.2f})",
                    (int(tip.x * w) + 5, int(tip.y * h)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "e01-webcam"))
    from video_loop import VideoLoop

    tracker = HandTracker()
    VideoLoop().run(process_frame=tracker)