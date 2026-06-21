import cv2
import time
from collections import deque

class VideoLoop:
    def __init__(self, camera_index=0, fps_window=30):
        self.camera_index = camera_index
        self.frame_times = deque(maxlen=fps_window)
        self.cap = None

    def _draw_fps(self, frame):
        avg_dt = sum(self.frame_times) / len(self.frame_times)
        if avg_dt > 0:
            fps = 1 / avg_dt
        else:
            fps = 0
        cv2.putText(frame, f"FPS: {fps:.1f}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    def run (self, process_frame = None):
        self.cap = cv2.VideoCapture(self.camera_index)
        fps_declarado = self.cap.get(cv2.CAP_PROP_FPS)
        print(f"A camera declara: {fps_declarado} FPS")
        if not self.cap.isOpened():
            raise RuntimeError(
                f"Webcam no indice {self.camera_index} nao abriu. "
                f"Verifique a conexao ou tente outro indice."
            )
        prev = time.time()
        fails = 0

        try:
            while True:
                ret, frame = self.cap.read()
                #Se vier vários frames finaliza o programa
                if not ret:
                    fails += 1
                    if fails > 30:
                        raise RuntimeError(
                            "Camera parou de entregar frames (30 falhas seguidas). "
                            "Provavel desconexao."
                        )
                    continue
                fails = 0   # frame bom: zera o contador
                now = time.time()
                self.frame_times.append(now - prev)
                prev = now

                if process_frame is not None:
                    frame = process_frame(frame)

                self._draw_fps(frame)
                cv2.imshow('frame', frame)

                if cv2.waitKey(1) == ord('q'):
                    break
        #O que estiver aqui dentro roda SEMPRE, deu erro ou não.
        finally:
            self.cap.release()
            cv2.destroyAllWindows()

#Teste do próprio E1: roda o loop sem processamento extra
if __name__ == "__main__":
    loop = VideoLoop()
    loop.run()
