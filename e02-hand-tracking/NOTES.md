# E2 — Os 21 pontos da mão

## O que entreguei
- `HandTracker`: estação plugável no `VideoLoop` do E1, detecta a mão na webcam
  e desenha os 21 keypoints em tempo real.
- Desenho **manual** dos pontos e conexões (sem o drawing_utils pronto): cada dedo
  com cor própria, pulso em branco. Provei que entendo a estrutura de dados crua.
- Coordenada normalizada do landmark 8 (ponta do indicador) exibida na tela.
- Suporte a duas mãos com rótulo Left/Right por mão.
- Estado `self.last_landmarks` guardado para o E3 consumir depois.


## O que estudei
- Estrutura dos 21 landmarks do MediaPipe (pontas: 4=polegar, 8=indicador,
  12=médio, 16=anelar, 20=mínimo; 0=pulso).
- Coordenadas normalizadas (0–1) vs. pixels: a rede fala em proporção, a tela em
  pixels. Conversão `int(lm.x * w), int(lm.y * h)`.
- BGR (OpenCV) vs. RGB (MediaPipe): precisa converter antes de processar.
- MediaPipe Tasks API (`HandLandmarker`), modo VIDEO com timestamp crescente.
- Doc: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python

## Onde travei e como resolvi
1. **`mp.solutions` não existe no mediapipe instalado.** A API clássica
   (`mp.solutions.hands`) que eu ia usar não estava no pacote: o wheel oficial
   0.10.35 para Windows/Python 3.13 só traz `tasks`, não `solutions`. Confirmei
   listando a pasta do pacote (`['modules', 'tasks', '__init__.py']` — sem `python/solutions`).
   Reinstalar o wheel oficial não resolveu. **Decisão:** migrar para a Tasks API
   (`HandLandmarker`), que já estava instalada e é a suportada pelo Google.
2. **VS Code rodando o Python errado.** O botão Run usava o Python 3.14 global em
   vez do venv (3.13), gerando `ModuleNotFoundError` mesmo com o pacote instalado.
   **Lição:** conferir o interpreter no canto do VS Code (deve dizer `venv`) — o
   erro não estava no código, estava em QUAL Python rodava. Tenho 4 Pythons na
   máquina (venv, 3.14, 3.13, 3.12-uv).
3. **Webcam não abria** (`Camera index out of range` → crash no `cvtColor`).
   Era cabo mal conectado. Expôs uma dívida do E1: o `VideoLoop` lia `ret` mas
   ignorava. Adicionei `if not ret: continue` + checagem de `isOpened()`.
4. **idx8 sobreposto com duas mãos:** texto em posição fixa de tela, escrito uma
   vez por mão. Resolvi ancorando a coordenada na própria ponta do indicador.

## O que isso prepara
- **E3:** os landmarks crus (`self.last_landmarks`) viram features (ângulos,
  distâncias). A conversão normalizado→número é a base.
- **Bloco C (E-C1):** já vi o jitter/salto dos pontos que o E-C1 vai ter que
  domar para virar sinal de servo.
- **Bloco D (data_quality.py):** descobri que mão de lado/oclusa faz os pontos
  **saltarem** para posições erradas (não é tremor, é detecção incorreta). E que
  o `handedness.score` **NÃO** detecta isso — permanece alto com pontos errados.
  Então o filtro de qualidade futuro precisará de outro sinal (ex.: variação
  brusca de posição entre frames), não o score.

