# Relatório Técnico — Braço Robótico com Imitation Learning
### Da demonstração humana à execução autônoma: visão computacional + ML + robótica

**Autor do plano:** Nathan
**Duração estimada:** 7 a 10 meses (6–8h/semana)
**Custo estimado de hardware:** R$ 1.500 – R$ 3.500 (detalhado na Seção 6)

---

## 1. Aviso honesto antes de começar

Este é o projeto mais difícil dos cinco que discutimos — ele **pressupõe** os outros quatro. Imitation learning não é um projeto isolado: é a camada final de uma pilha que inclui visão computacional, cinemática, controle de hardware e engenharia de dados. Pular direto para ele sem a base é a receita clássica de abandono no mês 2.

Por isso, este relatório **embute os pré-requisitos no próprio plano**: as Fases 1–3 são, na prática, versões compactadas dos projetos 1, 3 e 4. Você não vai "estudar para depois fazer" — cada fase produz um pedaço funcional do sistema final.

**O que o projeto entrega no final:** um braço robótico de mesa (SO-101) que, depois de assistir você demonstrar uma tarefa ~50 vezes (ex.: pegar um cubo e colocá-lo numa caixa), executa essa tarefa **sozinho**, usando câmeras e uma rede neural treinada por você.

---

## 2. Conceito central: o que é imitation learning, de verdade

### 2.1 A ideia em uma frase
Em vez de programar o robô ("mova a junta 1 para 45°, depois..."), você **coleta demonstrações** (vídeo + posições das juntas ao longo do tempo) e treina uma rede neural que aprende o mapeamento:

```
(imagem da câmera + estado atual das juntas)  →  (próxima ação das juntas)
```

Isso se chama **Behavioral Cloning (BC)**: aprendizado supervisionado onde o "rótulo" é a ação que o humano tomou naquele instante. É o mesmo paradigma de um classificador de imagens — só que a saída é contínua e sequencial.

### 2.2 Por que é um problema de ciência de dados (seu território)
- **Dataset:** episódios de demonstração são séries temporais multimodais (frames de vídeo a 30 FPS + vetores de 6 posições de junta). Qualidade do dado importa mais que arquitetura do modelo — demonstrações inconsistentes geram políticas ruins.
- **Distribution shift:** o problema teórico central. O modelo só viu estados que o *humano* visitou. Quando o robô erra um pouco, ele entra em estados fora da distribuição de treino e os erros se acumulam. As arquiteturas modernas (abaixo) existem para mitigar isso.
- **Avaliação:** taxa de sucesso por episódio, não acurácia por frame. Você vai desenhar o protocolo de avaliação — quantos episódios, variação de posição do objeto, iluminação.

### 2.3 As três arquiteturas que você vai encontrar (e qual usar)

| Arquitetura | Ideia | Quando usar |
|---|---|---|
| **ACT** (Action Chunking with Transformers) | Transformer que prevê *blocos* de ações futuras (ex.: 100 passos de uma vez), reduzindo acúmulo de erro | **Comece por ela.** Padrão do LeRobot, treina em GPU modesta, resultados sólidos com ~50 episódios |
| **Diffusion Policy** | Gera ações via processo de difusão (como geradores de imagem, mas para trajetórias) | Segunda iteração; lida melhor com multimodalidade (várias formas válidas de fazer a tarefa) |
| **SmolVLA / VLAs** | Modelos visão-linguagem-ação: recebem instrução em texto + imagem | Fase avançada; permite "pegue o cubo vermelho" como comando |

Todas estão implementadas e prontas no **LeRobot** (Hugging Face) — você não vai implementá-las do zero, vai entendê-las o suficiente para treinar, depurar e ajustar.

---

## 3. Mapa de conhecimento necessário

Organizado por área, do que você já tem ao que precisa construir.

### 3.1 O que você já tem (não estude de novo)
- Python intermediário ✔
- Noções de ML supervisionado, pandas, pipeline de dados ✔
- Git básico (assumido) ✔

### 3.2 Matemática mínima (não pule, mas não afunde)
| Tópico | Profundidade necessária | Para quê |
|---|---|---|
| Álgebra linear: matrizes de rotação, transformações homogêneas | Saber ler e aplicar, não demonstrar | Entender frames de referência do braço e calibração de câmera |
| Cinemática direta (FK) | Conceitual + usar bibliotecas | Saber onde está a garra dado os ângulos das juntas |
| Cinemática inversa (IK) | Conceitual (bibliotecas resolvem) | Converter "posição desejada da garra" em ângulos |
| Probabilidade básica + gradiente descendente | Você provavelmente já tem | Treino de redes |

**O que você NÃO precisa:** dinâmica de corpos rígidos, controle PID avançado, teoria de controle ótimo. O SO-101 + LeRobot abstraem isso.

### 3.3 Deep Learning prático (a maior lacuna a fechar)
- **PyTorch:** tensores, `Dataset`/`DataLoader`, loop de treino, salvar/carregar checkpoints, treinar em GPU.
- **CNNs e Transformers em nível de "usuário avançado":** entender o que cada bloco faz, ler um diagrama de arquitetura, ajustar hiperparâmetros. Não precisa implementar atenção do zero (mas fazer uma vez ajuda muito).
- **Visão computacional aplicada:** normalização de imagens, data augmentation, por que resolução e FPS importam.

### 3.4 Robótica prática
- Conceitos: graus de liberdade (DOF), espaço de juntas vs. espaço cartesiano, workspace, servo, encoder, teleoperação leader-follower.
- Ferramentas: simulador (MuJoCo via LeRobot), formato URDF (descrição do robô), comunicação serial USB.

### 3.5 Engenharia (cola de tudo)
- Linha de comando Linux/WSL (o LeRobot é CLI-first)
- Ambientes virtuais (conda/uv), gestão de dependências CUDA
- Hugging Face Hub (datasets e modelos são versionados lá)

---

## 4. Stack tecnológica

### Linguagem
**Python 3.10+, exclusivamente.** Não há necessidade de C++ neste projeto — o LeRobot encapsula a comunicação de baixo nível com os servos. (C++ entra apenas se um dia você migrar para ROS 2 industrial, o que está fora do escopo.)

### Bibliotecas principais
| Biblioteca | Papel |
|---|---|
| **LeRobot** (Hugging Face) | Núcleo: drivers do braço, teleoperação, gravação de datasets, treino (ACT/Diffusion/SmolVLA), inferência |
| **PyTorch** | Backend de treino |
| **OpenCV** | Captura e pré-processamento de câmera |
| **MuJoCo / gym (via LeRobot)** | Simulação para praticar o pipeline antes do hardware |
| **MediaPipe ou YOLO-Pose** | Fase 1 (pose estimation humana) |
| **wandb ou TensorBoard** | Acompanhar curvas de treino |
| **NumPy / pandas / matplotlib** | Análise dos datasets de episódios |

### Hardware de computação
- **Mínimo para treinar ACT:** GPU NVIDIA com 8 GB VRAM (RTX 3060/4060) ou **Google Colab Pro** (~US$ 10/mês) — treino de ACT com 50 episódios leva poucas horas.
- Inferência (rodar a política no robô) roda em CPU ou GPU modesta, em tempo real.
- Notebook comum serve para coleta de dados e controle.

---

## 5. Arquitetura do sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     FASE DE COLETA                          │
│                                                             │
│  Braço LEADER (você move) ──serial──┐                       │
│                                     ├──► LeRobot record     │
│  Braço FOLLOWER (replica) ──serial──┤      │                │
│                                     │      ▼                │
│  Câmera frontal ────USB─────────────┤  LeRobotDataset       │
│  Câmera no punho ───USB─────────────┘  (vídeo + juntas      │
│                                         sincronizados,      │
│                                         por episódio)       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASE DE TREINO                          │
│                                                             │
│  LeRobotDataset ──► DataLoader ──► Política ACT             │
│                                    (encoder visual CNN +    │
│                                     transformer de ações)   │
│                                          │                  │
│                              checkpoints + métricas (wandb) │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   FASE DE INFERÊNCIA                        │
│                                                             │
│  Câmeras ──► política treinada ──► ações ──► FOLLOWER       │
│                 (30 Hz, loop fechado)         executa só    │
└─────────────────────────────────────────────────────────────┘
```

**Conceito-chave — teleoperação leader-follower:** o kit SO-101 vem com **dois braços**: o *leader* (sem força, você move com a mão) e o *follower* (motorizado, espelha o leader em tempo real). É assim que se coletam demonstrações naturais: você "veste" o robô através do leader. Os encoders magnéticos registram as posições com precisão suficiente para que o ruído de coleta não degrade o treino.

### 5.1 Estrutura de código do repositório

```
imitation-arm/
├── README.md
├── pyproject.toml              # dependências (uv ou pip)
├── configs/
│   ├── camera_setup.yaml       # índices, resolução, FPS das câmeras
│   └── train_act.yaml          # hiperparâmetros do treino
├── notebooks/
│   ├── 01_explore_dataset.ipynb    # análise exploratória dos episódios
│   ├── 02_quality_checks.ipynb     # detectar episódios ruins (jitter, dropout de frames)
│   └── 03_eval_analysis.ipynb      # análise das taxas de sucesso
├── scripts/
│   ├── record_episodes.sh      # wrapper do lerobot-record com seus parâmetros
│   ├── train.sh                # wrapper do lerobot-train
│   └── deploy.sh               # inferência no braço real
├── src/
│   ├── data_quality.py         # suas métricas de qualidade de episódio
│   ├── eval_protocol.py        # protocolo de avaliação padronizado
│   └── viz.py                  # visualização de trajetórias de junta
└── reports/
    └── experiment_log.md       # diário de experimentos (data, config, resultado)
```

Note o padrão: **o LeRobot faz o trabalho pesado via CLI; seu código próprio vive na análise de dados e no protocolo experimental** — exatamente onde sua formação em ciência de dados gera diferencial. A maioria das pessoas trata a coleta como caixa-preta; você vai tratá-la como um problema de qualidade de dados.

### 5.2 O pipeline em comandos (visão real do fluxo)

```bash
# 1. Calibrar os braços (uma vez)
lerobot-calibrate --teleop.type=so101_leader --teleop.port=/dev/ttyACM0 ...

# 2. Gravar 50 episódios da tarefa
lerobot-record \
  --robot.type=so101_follower \
  --teleop.type=so101_leader \
  --robot.cameras="{front: {...}, wrist: {...}}" \
  --dataset.repo_id=nathan/pega-cubo-v1 \
  --dataset.num_episodes=50 \
  --dataset.single_task="Pegar o cubo e colocar na caixa"

# 3. Treinar a política ACT
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=nathan/pega-cubo-v1 \
  --output_dir=outputs/act-pega-cubo

# 4. Rodar autonomamente e gravar episódios de avaliação
lerobot-record --policy.path=outputs/act-pega-cubo/checkpoints/last ...
```

---

## 6. Hardware: o que comprar e quando

**Regra de ouro: não compre nada até concluir a Fase 2 (simulação).** Se você desistir, desiste de graça.

### Opção recomendada: SO-101 (par leader + follower)
- Braço open-source de 6 DOF, padrão de facto da comunidade LeRobot; peças impressas em 3D + servos Feetech STS3215 com encoder magnético.
- **Caminhos de compra no Brasil:**
  1. **Kit importado completo** (AliExpress/Seeed/WowRobo): US$ 230–350 o par + impostos de importação → estime **R$ 2.500–3.500** no total.
  2. **DIY:** comprar só os 12 servos + controladora importados (~US$ 150–200) e imprimir as peças (arquivos STL são gratuitos no GitHub do projeto; serviços de impressão 3D em Blumenau/região cobram ~R$ 150–300 o conjunto) → **R$ 1.500–2.200**. Mais barato, mais aprendizado, mais risco de fricção na montagem.
- **Extras:** 2 webcams USB (1080p, ~R$ 100–150 cada — uma frontal, uma no punho), fonte 12V 5A, cubos/objetos de teste.

### Por que não alternativas mais baratas (R$ 300 com servos SG90)?
Servos de hobby sem encoder têm folga e imprecisão que **viram ruído de treino** — você não saberia se a política falhou por causa do modelo ou do hardware. Para imitation learning, o encoder magnético do SO-101 não é luxo, é requisito do método.

---

## 7. Plano de estudo e execução — fase a fase

### FASE 0 — Setup e PyTorch (3–4 semanas)
**Objetivo:** fechar a lacuna de deep learning prático.

| Atividade | Recurso |
|---|---|
| PyTorch do zero ao loop de treino completo | **"PyTorch for Deep Learning" — Daniel Bourke (freeCodeCamp/YouTube, gratuito, ~25h)** ou curso oficial *Learn the Basics* da documentação PyTorch |
| Fundamentos de redes (se quiser solidez) | **fast.ai — Practical Deep Learning for Coders** (gratuito) — pelo menos as lições 1–4 |
| Transformers em nível conceitual | Vídeo "Attention is all you need explained" do canal 3Blue1Brown + post *The Illustrated Transformer* (Jay Alammar) |

**Entregável:** treinar um classificador de imagens em PyTorch do zero (CIFAR-10), com curvas no TensorBoard. Critério de saída: você consegue explicar cada linha do loop de treino.

---

### FASE 1 — Visão computacional e pose humana (3–4 semanas)
**Objetivo:** dominar captura e processamento de vídeo em tempo real (versão compacta do "projeto 1").

| Atividade | Recurso |
|---|---|
| OpenCV: captura, transformação, calibração de câmera | Curso OpenCV da freeCodeCamp (YouTube, gratuito) + docs oficiais |
| Pose estimation aplicada | Documentação MediaPipe Pose + tutoriais Ultralytics YOLO-Pose |
| Noção de calibração intrínseca/extrínseca | Tutorial oficial de *camera calibration* do OpenCV |

**Entregável:** script que captura sua webcam, extrai keypoints do seu braço em tempo real (30 FPS) e plota os ângulos de ombro/cotovelo ao vivo. Esse código será reaproveitado.

---

### FASE 2 — Robótica em simulação (5–6 semanas)
**Objetivo:** aprender os conceitos de robótica e rodar o pipeline completo do LeRobot **sem hardware**.

| Atividade | Recurso |
|---|---|
| Fundamentos teóricos: frames, FK, IK | **Modern Robotics (Northwestern/Coursera, gratuito p/ auditar)** — apenas Cursos 1 e 2 da especialização. Disciplina: não faça tudo |
| Instalar LeRobot, explorar datasets públicos | Documentação oficial LeRobot (huggingface.co/docs/lerobot) — comece pelo *Getting Started* |
| Treinar uma política ACT em ambiente simulado (PushT ou ALOHA sim) | Tutoriais de simulação do LeRobot + notebook de treino oficial |
| Visualizar e dissecar um LeRobotDataset público | Ferramenta `visualize_dataset` + seu notebook de EDA |

**Entregável:** política ACT treinada por você em simulação, com vídeo do agente executando a tarefa e relatório curto (1 página) das curvas de treino. **Critério de compra do hardware: só passe à Fase 3 com isso pronto.**

---

### FASE 3 — Hardware: montagem e teleoperação (4–6 semanas)
**Objetivo:** braço físico montado, calibrado e teleoperável.

| Atividade | Recurso |
|---|---|
| Comprar/imprimir e montar o par SO-101 | Guia oficial de montagem SO-101 (docs LeRobot) + vídeos da comunidade no YouTube |
| Configurar motores, portas seriais, calibração | `lerobot-setup-motors` e `lerobot-calibrate` (docs oficiais) |
| Montar setup de câmeras (frontal + punho) e iluminação | Guia de câmeras do LeRobot |
| Teleoperar: leader controla follower em tempo real | Tutorial *Imitation Learning on Real-World Robots* (docs LeRobot) |

**Entregável:** vídeo do follower espelhando o leader com fluidez; checklist de calibração documentado. Comunidade de apoio: **Discord do LeRobot** (muito ativo — use quando travar em hardware).

---

### FASE 4 — Coleta de dados como cientista de dados (3–4 semanas)
**Objetivo:** dataset de demonstrações de alta qualidade — a fase mais subestimada e a que mais determina o resultado.

Tarefa-alvo sugerida: **pegar um cubo de posição semi-aleatória e colocá-lo numa caixa fixa.**

Boas práticas (extraídas da experiência da comunidade):
1. **50 episódios** como baseline; varie a posição do cubo entre episódios de forma controlada (grade de 3×3 posições, por exemplo).
2. Consistência de execução: mesma estratégia de pegada em todos os episódios (multimodalidade desnecessária prejudica BC).
3. Iluminação e fundo fixos na v1; varie só na v2 (robustez é experimento, não padrão).
4. **Seu diferencial:** escreva `data_quality.py` — detectar episódios com frames perdidos, jitter anormal de junta, duração fora do padrão. Descarte e regrave os ruins.

**Entregável:** `nathan/pega-cubo-v1` publicado no Hugging Face Hub + notebook de EDA do dataset (distribuição de durações, heatmap de trajetórias, qualidade por episódio).

---

### FASE 5 — Treino, avaliação e iteração (4–8 semanas)
**Objetivo:** política autônoma com taxa de sucesso mensurável.

1. Treinar ACT com a config padrão → avaliar com protocolo fixo: **20 episódios de teste, posições do cubo sorteadas, métrica = taxa de sucesso**.
2. Diagnosticar falhas como cientista de dados: onde a política falha? Posições não cobertas no treino? Oclusão da câmera? → coletar dados direcionados (é o ciclo dado→modelo→dado, que você já conhece do trabalho).
3. Iterar: mais episódios nas regiões de falha, ajuste de chunk size do ACT, augmentation de imagem.
4. **Extensão A:** treinar Diffusion Policy no mesmo dataset e comparar (relatório comparativo = ouro de portfólio).
5. **Extensão B (liga com sua paixão original):** substituir o leader arm por **teleoperação via pose estimation da sua mão/braço** (código da Fase 1 + IK) — você demonstra a tarefa com o próprio corpo, sem tocar no robô. Há projetos da comunidade fazendo isso como referência.

**Entregável final:** vídeo do braço executando a tarefa sozinho + repositório documentado + relatório de experimentos (taxas de sucesso por versão de dataset/modelo).

---

## 8. Cronograma consolidado

| Fase | Semanas | Marco |
|---|---|---|
| 0 — PyTorch | 1–4 | Classificador treinado do zero |
| 1 — Visão/pose | 5–8 | Tracking de braço em tempo real |
| 2 — Simulação | 9–14 | Política ACT treinada em sim ✅ *gate de compra* |
| 3 — Hardware | 15–20 | Teleoperação fluida |
| 4 — Coleta | 21–24 | Dataset v1 no Hub |
| 5 — Treino/iteração | 25–32+ | Execução autônoma ≥70% sucesso |

Total: ~8 meses no ritmo de 6–8h/semana. Fases 0–2 podem comprimir se o PyTorch fluir rápido.

---

## 9. Recursos de estudo — lista consolidada

**Centrais (use sempre):**
- Documentação LeRobot — huggingface.co/docs/lerobot (tutoriais de sim, SO-101, imitation learning real)
- Repositório LeRobot no GitHub — github.com/huggingface/lerobot (issues e exemplos)
- Discord oficial do LeRobot — suporte da comunidade, essencial nas fases de hardware

**Deep learning:**
- PyTorch for Deep Learning — Daniel Bourke (YouTube/freeCodeCamp)
- fast.ai — Practical Deep Learning for Coders
- The Illustrated Transformer — Jay Alammar

**Visão computacional:**
- Curso OpenCV — freeCodeCamp (YouTube)
- Documentação MediaPipe e Ultralytics

**Robótica:**
- Modern Robotics — Kevin Lynch, Northwestern (Coursera, cursos 1–2)
- Livro-texto *Modern Robotics* (PDF gratuito no site dos autores) — como referência, não leitura linear

**Papers (leia quando chegar na Fase 4–5, não antes):**
- *ACT / ALOHA*: "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware" (Zhao et al., 2023)
- *Diffusion Policy*: Chi et al., 2023
- *SmolVLA*: relatório técnico da Hugging Face

**Comunidade BR:** grupos de robótica maker e LeRobot têm presença em fóruns/Telegram brasileiros; vale procurar makers com impressora 3D na região de Blumenau para as peças.

---

## 10. Riscos e como mitigar

| Risco | Probabilidade | Mitigação |
|---|---|---|
| Desistência na fase de hardware (fricção de montagem) | Alta | Gate de compra após Fase 2; Discord para destravar; considerar kit pré-montado se orçamento permitir |
| GPU insuficiente para treino | Média | Colab Pro resolve para ACT; treinos são de horas, não dias |
| Importação cara/demorada dos servos | Média | Comprar com antecedência (durante a Fase 2); comparar Seeed vs. AliExpress vs. revendedores nacionais |
| Política nunca converge | Média | Quase sempre é problema de dados, não de modelo — por isso a Fase 4 é tratada com rigor de cientista de dados |
| Conflito de tempo com trabalho + faculdade | Alta | O plano é modular: cada fase tem valor isolado de portfólio; pausar entre fases não destrói o progresso |

---

## 11. Por que este projeto vale o esforço (visão de portfólio)

Imitation learning em hardware real é, em 2026, a fronteira acessível da robótica — o mesmo paradigma (VLAs, demonstração → política) usado por laboratórios de ponta, mas executável numa mesa com R$ 3 mil. Para um cientista de dados, ele demonstra exatamente o que o mercado não vê em portfólios comuns: **engenharia de dados em domínio físico, avaliação experimental rigorosa e ML que age no mundo, não só prevê**. E cada fase intermediária (pose estimation, política em simulação, dataset publicado no Hub) já é um item de portfólio independente — você não precisa chegar ao fim para ter o que mostrar.
