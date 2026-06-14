# Trilha de Entregáveis — Imitation Learning do Zero
### Modelo: cada entregável puxa apenas o estudo que ele exige

**Como usar este documento:** um entregável por vez, em ordem. Só avance quando o critério de "pronto" for cumprido. Documente cada um (ver Seção final). Os tempos de estudo são de *material novo* — o tempo de codar varia por pessoa.

**Estrutura do repositório (crie no dia 1):**
```
imitation-arm/
├── README.md            # índice dos entregáveis com status
├── e01-webcam/
├── e02-hand-tracking/
├── e03-features/
│   └── ...              # cada pasta: código + NOTES.md (o que aprendi, o que travou)
```

---

## BLOCO A — A mão como sensor (sem ML próprio)
*Tema: dominar captura e geometria de keypoints. Nenhuma rede neural sua ainda.*

### E1 — Webcam ao vivo
- **Entrega:** script que abre a webcam, exibe o vídeo com contador de FPS na tela, fecha com tecla.
- **Estudo (~2h):** seções iniciais do curso OpenCV da freeCodeCamp (YouTube) — leitura de vídeo, exibição, desenho de texto/formas no frame.
- **Pronto quando:** roda estável a ~30 FPS.
- **Ensina:** o loop fundamental de visão em tempo real — tudo daqui pra frente vive dentro dele.

### E2 — Os 21 pontos da mão
- **Entrega:** sua mão na webcam com os 21 keypoints e as conexões desenhados em tempo real (o exemplo que você deu).
- **Estudo (~2h):** documentação do MediaPipe Hands (guia Python) — só o necessário para rodar e entender a estrutura de saída (landmarks normalizados x, y, z).
- **Pronto quando:** pontos seguem a mão com fluidez; você sabe dizer qual índice é a ponta do indicador sem olhar a doc.
- **Ensina:** consumir saída de um modelo de visão pronto — o formato de dado que alimenta todo o resto.

### E3 — Da imagem ao número
- **Entrega:** a partir dos 21 pontos, calcular features geométricas — ângulos entre falanges (produto escalar de vetores), distâncias entre pontas — e plotar um gráfico ao vivo de 2–3 dessas medidas enquanto você move a mão.
- **Estudo (~2h):** revisão de vetores e produto escalar (qualquer vídeo curto de álgebra vetorial) + matplotlib em modo animado/interativo.
- **Pronto quando:** dobrar o indicador altera visivelmente a curva do ângulo correspondente.
- **Ensina:** *feature engineering espacial* — keypoints crus viram variáveis. É o coração da conexão visão↔dados.

### E4 — Reconhecedor de gestos por regras
- **Entrega:** sistema que reconhece 5 gestos estáticos (mão aberta, punho, joinha, paz, apontar) usando apenas regras sobre as features do E3 — zero ML.
- **Estudo (0h):** nenhum material novo; é engenharia sobre o que você já tem.
- **Pronto quando:** acerta os 5 gestos de forma consistente para *você*; e você consegue listar onde as regras quebram (outras mãos, rotação, iluminação).
- **Ensina:** o limite das heurísticas — a justificativa concreta para o ML do próximo bloco. Documente as falhas: elas viram seu argumento.

---

## BLOCO B — O primeiro ML (e o PyTorch entra na hora certa)
*Tema: substituir regras por modelos, com dataset coletado por você.*

### E5 — Coletor de dataset
- **Entrega:** ferramenta de coleta: você pressiona uma tecla correspondente ao gesto e o script grava os keypoints rotulados num CSV (centenas de amostras por gesto, com variação de posição/rotação da mão).
- **Estudo (0h):** nenhum — engenharia pura.
- **Pronto quando:** CSV com ≥300 amostras/gesto e um mini-EDA em notebook (distribuição por classe, exemplos plotados).
- **Ensina:** a disciplina de coleta e rotulagem — a habilidade nº 1 do projeto final (a Fase 4 do relatório anterior é isto em escala maior).

### E6 — Classificador clássico
- **Entrega:** RandomForest/SVM (sklearn) treinado no CSV do E5, integrado ao loop da webcam: o nome do gesto aparece na tela em tempo real.
- **Estudo (~2h):** revisão de sklearn (você já tem base) + matriz de confusão e validação treino/teste correta (sem vazamento entre sessões de coleta).
- **Pronto quando:** >90% de acurácia em dados de uma *sessão de coleta diferente* da de treino + matriz de confusão analisada.
- **Ensina:** que com boas features, modelos simples resolvem — e como avaliar sem se enganar.

### E7 — Gestos dinâmicos
- **Entrega:** reconhecer 3 gestos de *movimento* (acenar, círculo, deslizar) usando janelas temporais de keypoints (ex.: 30 frames) com features agregadas (médias, amplitudes, velocidades) ainda em sklearn.
- **Estudo (~1h):** conceito de janelamento de séries temporais (sliding window).
- **Pronto quando:** reconhece os 3 gestos ao vivo com latência aceitável (<1s).
- **Ensina:** dado sequencial — a ponte conceitual para políticas de robô, que são exatamente sequências de (observação → ação).

### E8 — ⚡ Aqui entra o PyTorch
- **Entrega:** reimplementar o classificador do E6 como uma MLP em PyTorch, do zero: Dataset, DataLoader, loop de treino, curvas de loss, checkpoint salvo. Meta: igualar a acurácia do sklearn.
- **Estudo (~6h):** *Learn the Basics* da documentação oficial do PyTorch (~3h) **ou** os 3 primeiros módulos do curso do Daniel Bourke. Não assista as 25h — só isto.
- **Pronto quando:** acurácia ≈ sklearn e você explica cada linha do loop de treino (forward, loss, backward, step).
- **Ensina:** PyTorch com motivação real — você já sabe qual resultado esperar, então depura o framework, não o problema.

### E9 — Rede sequencial
- **Entrega:** substituir as features agregadas do E7 por uma GRU/LSTM pequena que recebe a sequência crua de keypoints e classifica o gesto dinâmico.
- **Estudo (~3h):** um tutorial de RNN/LSTM em PyTorch para classificação de sequências.
- **Pronto quando:** desempenho ≥ E7 e você sabe justificar quando a rede vale a complexidade extra (e quando não).
- **Ensina:** modelos sequenciais — a família de onde vêm ACT e as políticas do projeto final.

---

## BLOCO C — O braço entra em cena (simulado, custo zero)
*Tema: robótica de verdade, sem gastar um real.*

### E10 — Do dedo ao braço
- **Entrega:** trocar MediaPipe Hands por MediaPipe Pose: extrair keypoints do corpo e calcular ângulos de ombro e cotovelo ao vivo (reaproveita E3 quase inteiro).
- **Estudo (~1h):** doc do MediaPipe Pose (mesma lógica do Hands).
- **Pronto quando:** ângulos de ombro/cotovelo plotados ao vivo, estáveis.
- **Ensina:** generalização do pipeline — e gera o sinal de controle do próximo entregável.

### E11 — 🤖 O braço virtual imita você
- **Entrega:** braço robótico em PyBullet (gratuito, URDF pronto — ex.: Kuka ou um braço simples) cujas juntas de ombro/cotovelo seguem os SEUS ângulos do E10, em tempo real. **O entregável-vitrine do meio da trilha.**
- **Estudo (~5h):** quickstart do PyBullet (~3h: carregar URDF, setar posições de junta, stepSimulation) + 2 vídeos selecionados do curso Modern Robotics sobre graus de liberdade e cinemática direta (~2h).
- **Pronto quando:** vídeo lado a lado: você movendo o braço ↔ robô virtual espelhando.
- **Ensina:** espaço de juntas, mapeamento humano→robô, e a primeira sensação real de "robótica".

### E12 — Cinemática inversa
- **Entrega:** em vez de mapear junta-a-junta, controlar a *posição da garra* do braço virtual com a posição da sua mão no espaço — o PyBullet resolve a IK (`calculateInverseKinematics`).
- **Estudo (~3h):** conceito de IK (1 aula do Modern Robotics ou vídeo equivalente) + a função de IK do PyBullet.
- **Pronto quando:** sua mão "arrasta" a garra virtual pelo espaço com fluidez; você entende por que algumas posições são inalcançáveis (workspace).
- **Ensina:** espaço cartesiano vs. espaço de juntas — o conceito que separa quem entende robótica de quem só roda scripts.

### E13 — Primeiro imitation learning (em simulação)
- **Entrega:** instalar LeRobot, explorar um dataset público com `visualize_dataset`, e treinar uma política ACT no ambiente simulado PushT, com curvas de treino e vídeo do agente executando.
- **Estudo (~6h):** *Getting Started* + tutorial de simulação da documentação do LeRobot; leitura conceitual do paper do ACT (só seções de método, ~1h).
- **Pronto quando:** política treinada por você resolve o PushT na maioria dos episódios + relatório de 1 página.
- **Ensina:** o pipeline completo do projeto final, de ponta a ponta, sem hardware. **🚧 GATE DE COMPRA: só passe ao Bloco D com este entregável concluído.**

---

## BLOCO D — Hardware e o projeto final
*Tema: o mundo real. Aqui começa o investimento financeiro (~R$ 1.500–3.500).*

### E14 — Montagem e teleoperação do SO-101
- **Entrega:** par leader-follower montado, motores configurados, calibrado, follower espelhando o leader com fluidez (vídeo).
- **Estudo (~4h + montagem):** guia oficial de montagem e calibração do SO-101 nas docs do LeRobot; Discord do LeRobot como suporte quando travar.
- **Pronto quando:** teleoperação fluida + checklist de calibração documentado.

### E15 — Dataset de demonstrações
- **Entrega:** 50 episódios da tarefa "pegar cubo → colocar na caixa" gravados via `lerobot-record` (2 câmeras: frontal + punho), publicados no Hugging Face Hub, com notebook de EDA e um script próprio de qualidade (detectar episódios com frames perdidos/jitter).
- **Estudo (~3h):** tutorial *Imitation Learning on Real-World Robots* (docs LeRobot).
- **Pronto quando:** dataset no Hub + EDA + episódios ruins identificados e regravados.
- **Ensina:** é o E5 em escala industrial — seu diferencial de cientista de dados aplicado.

### E16 — 🏁 Política autônoma
- **Entrega:** ACT treinado no seu dataset executando a tarefa sozinho. Protocolo de avaliação fixo: 20 episódios de teste, posições sorteadas do cubo, taxa de sucesso reportada. Iterar: diagnosticar falhas → coletar dados direcionados → retreinar.
- **Estudo (~2h + iteração):** seção de treino e avaliação das docs do LeRobot; wandb/TensorBoard para acompanhar.
- **Pronto quando:** ≥70% de sucesso + relatório de experimentos (cada versão de dataset/modelo e seu resultado).

### E17 — Extensão: demonstrar com o próprio corpo
- **Entrega:** substituir o leader arm pela SUA mão — teleoperação via pose estimation (E10) + IK (E12) controlando o follower real, e coletar demonstrações assim. Fecha o ciclo com a sua motivação original: movimento humano → robô.
- **Estudo (0h novo):** é integração de tudo que você construiu.
- **Pronto quando:** vídeo do braço real espelhando seu braço, sem tocar em nada.

---

## Resumo do esforço de estudo (material novo)

| Bloco | Estudo novo total | Quando |
|---|---|---|
| A (E1–E4) | ~6h | Semanas 1–4 |
| B (E5–E9) | ~12h (PyTorch incluso: 9h) | Semanas 5–10 |
| C (E10–E13) | ~15h | Semanas 11–16 |
| D (E14–E17) | ~9h + montagem | Meses 4–7 |

As 25h de PyTorch viraram ~9h distribuídas (E8 + E9), consumidas exatamente quando têm aplicação. Se em algum ponto sentir lacuna de fundamento, anote num **"log de dívida de estudo"** no README e pague a dívida entre blocos — não no meio de um entregável.

## Como documentar (proposta)
Cada pasta `eNN-*/` contém um `NOTES.md` com 4 seções fixas: **O que entreguei** (com gif/vídeo curto), **O que estudei** (links), **Onde travei e como resolvi**, **O que isso prepara**. No fim, o README com a tabela de status vira, sozinho, a narrativa do portfólio — e material pronto para posts no LinkedIn por entregável, se quiser visibilidade.
