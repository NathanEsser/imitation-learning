# E1 — Webcam, loop de vídeo e VideoLoop reutilizável

Primeiro entregável: provar que a câmera funciona e construir a base de vídeo
que todos os entregáveis seguintes (E2 keypoints, E3 features...) vão reutilizar.
Nada de ML ou MediaPipe ainda — só a fundação.

## O que foi entregue (T1.1 a T1.7)

- **T1.1** Ambiente: venv + OpenCV instalados, git iniciado e repositório remoto no ar.
- **T1.3/T1.4** Captura de frame e loop de vídeo ao vivo com saída pela tecla `q`.
- **T1.5** Desenho sobre o frame (retângulo + texto).
- **T1.6** Cálculo e exibição do FPS real, com média móvel (`deque`) para suavizar.
- **T1.7** Refatoração de tudo numa classe `VideoLoop` reutilizável, com ponto de
  injeção (`process_frame`) para os próximos entregáveis plugarem comportamento.

## Tropeços e como resolvi (pra não cair de novo)

- **cmd vs PowerShell:** `New-Item` é comando do PowerShell e não roda no Prompt
  de Comando (cmd). O prompt `PS C:\...>` indica PowerShell; `C:\...>` é cmd.
  Mantive PowerShell pelo resto do projeto.

- **Ativação do venv no Windows:** se der erro de "execution policy", rodar uma vez
  `Set-ExecutionPolicy -Scope CurrentUser -RemoteSigned` e ativar de novo.

- **OpenCV não importava:** o `import cv2` falhava porque o pacote tinha sido
  instalado fora do venv ativo. Instalar com o venv ativado resolveu (versão 4.13.0).

- **git: `master` vs `main`:** o commit inicial criou a branch `master`, mas o push
  foi tentado em `main` → erro `src refspec main does not match any`. Resolvido com
  `git branch -M main` antes do `git push -u origin main`.

- **Autenticação do GitHub:** push pede login; senha comum não funciona mais (precisa
  de token ou autenticação pelo navegador). Resolveu na primeira vez via navegador.

- **Cor BGR, não RGB (IMPORTANTE pro E2):** OpenCV usa ordem **B, G, R** — não RGB.
  Vermelho é `(0, 0, 255)`, não `(255, 0, 0)` (que dá azul). Cada canal vai de 0 a 255;
  valores acima (ex.: 1288) são truncados silenciosamente. Causa nº 1 de "cor saiu trocada".

- **Bug do `else` solto:** escrever só `0` numa linha (em vez de `fps = 0`) não atribui
  nada — a variável `fps` não é criada e a linha seguinte quebra com `NameError`.
  Atribuição precisa do `nome =`.

## Conceitos que aprendi nesta etapa

- **`time.time()`** retorna segundos desde 1970 (epoch). O valor absoluto não importa;
  o que importa é a **diferença entre duas chamadas** = tempo decorrido. Base do cálculo
  de FPS. (`time.perf_counter()` é mais preciso para intervalos curtos — fica de nota.)

- **Padrão `now`/`prev`:** `prev` guarda o tempo da volta anterior do loop; `now` é o
  tempo atual. `dt = now - prev` mede um frame; `prev = now` passa o bastão para a
  próxima volta.

- **`deque(maxlen=N)`:** fila de tamanho fixo que descarta o valor mais antigo sozinha.
  Usada para a média móvel do FPS. Mesmo padrão volta no E3 (suavização de keypoints).

- **Classe vs objeto:** a classe é o molde (planta); o objeto é a instância construída
  a partir dela. `VideoLoop` é o molde; `loop = VideoLoop()` é o objeto.

- **`__init__`:** roda automaticamente quando o objeto nasce. Define as características
  do objeto (com `self.`) e prepara recipientes vazios. Não liga a câmera ainda — isso
  fica pro `run`, separando "nascer" de "operar".

- **`self`:** referência ao próprio objeto. `self.x` grava/lê um valor *naquele* objeto
  específico, sobrevivendo entre métodos. Sem `self.`, a variável morre no fim da função.

- **Método:** ação que o objeto sabe fazer. `_draw_fps` e `run` são métodos. O underscore
  em `_draw_fps` sinaliza "uso interno" (convenção, não proibição).

- **`process_frame` (função como argumento):** uma função pode ser passada como valor
  para outra. O `run` executa o trabalho fixo (câmera, FPS, exibição) e chama a função
  injetada para o processamento específico de cada entregável. Passar `func` (sem
  parênteses) = entregar a função; `func(frame)` (com parênteses) = executá-la.

- **`try`/`finally`:** o bloco `finally` roda SEMPRE, com erro ou não. Garante que a
  câmera seja liberada mesmo se o processamento quebrar no meio — evita câmera "presa"
  durante a depuração.

## Decisões de design registradas

- `VideoLoop` foi feito como **classe** (não função) pensando em entregáveis futuros que
  vão guardar estado entre frames (buffers de suavização, janelas temporais no E3/E7).

- O `run` aceita **uma** estação (`process_frame`) por enquanto. Quando o E3 precisar
  encadear várias (keypoints + ângulos + suavização), refatorar para aceitar uma **lista**
  de estações e rodar num `for`. Não construir essa flexibilidade antes de ter o caso real.

## Próximo passo (E2)

Plugar o **MediaPipe Hands** (`mp.solutions.hands`) como a primeira `process_frame`:
detectar a mão e desenhar os 21 keypoints sobre o frame, dentro do `VideoLoop`.

- Usar a **API clássica** `mp.solutions.hands` (legada mas funcional e muito mais
  documentada que a nova Tasks API; o que se aprende sobre os 21 pontos é igual nas duas).
- **Atenção à versão do Python:** MediaPipe costuma não suportar as versões mais novas
  do Python. Se `pip install mediapipe` falhar, criar um venv numa versão compatível.
