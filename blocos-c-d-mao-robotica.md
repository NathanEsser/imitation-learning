# Trilha de Entregáveis — Blocos C e D (REMODELADOS)
### Destino: mão robótica DIY de 5 dedos, teleoperada por visão, que aprende a manipular

**O que mudou em relação aos documentos originais:** os Blocos A e B permanecem **idênticos** — eles constroem o pipeline de visão (keypoints → features → ML) que serve de espinha dorsal aqui. A partir do Bloco C, o destino deixa de ser o braço SO-101 e passa a ser uma **mão robótica antropomórfica construída por você**, controlada pelos seus próprios movimentos via webcam.

**As três decisões de design que estruturam estes blocos:**
1. **Hardware:** mão imprimível pronta (Amazing Hand ou DexHand), não projetada do zero. Projetar geometria de dedos é onde projetos morrem.
2. **Teleoperação por visão**, não por luva — reusa todo o Bloco A-B, ao custo de mais fragilidade (oclusão de dedos). Você aceitou esse trade-off conscientemente.
3. **ML por behavior cloning caseiro em PyTorch**, não via LeRobot — porque o LeRobot é construído para hardware oficial e sua mão DIY não é reconhecida por ele de fábrica.

**🚧 Os dois gates do projeto:**
- **Gate de simulação (fim do E-C2):** só compre/imprima hardware depois de provar que o pipeline pose→ângulos→robô funciona em simulação.
- **Gate de impressão (início do E-C3):** decisão de impressora/serviço fica para este momento, não antes.

---

## BLOCO C — Da mão real à mão virtual (custo quase zero)
*Tema: robótica de mão em simulação + a ponte pose→servo. Nenhum hardware comprado ainda.*

A lógica do bloco: antes de gastar um real, você prova em simulação que consegue mapear os keypoints da sua mão (que o Bloco A já extrai) em comandos de junta de uma mão robótica. Se isso funciona na tela, funciona no hardware. Se você desiste aqui, desiste de graça.

### E-C1 — Ângulos da mão como sinal de controle
- **Entrega:** a partir dos 21 keypoints do MediaPipe (já dominados no E2-E3), calcular os ângulos de flexão de cada dedo de forma **estável e normalizada**, prontos para virar comando de servo. Plotar os 5 ângulos ao vivo.
- **Por que separado do E3:** o E3 calculava ângulos para *classificar gestos*; aqui o alvo é diferente — você precisa de um sinal contínuo, suave e calibrado (0 = dedo esticado, 1 = totalmente dobrado) que um servo possa seguir sem tremer. É um problema de qualidade de sinal, não de feature para ML.
- **Estudo (~1h):** revisão de mapeamento/normalização de faixas (range mapping) + filtro de suavização (média móvel ou filtro exponencial — você já viu no T3.7).
- **Pronto quando:** os 5 ângulos variam de forma suave e repetível entre 0 e 1; dobrar um dedo move só a curva dele; o ruído de jitter está visivelmente controlado.
- **Ensina:** a diferença entre "sinal para humano ver" e "sinal para máquina seguir" — a primeira lição de teleoperação.

### E-C2 — A mão virtual imita você 🤖
- **Entrega:** uma mão robótica em simulação (PyBullet ou MuJoCo, ambos gratuitos) cujos dedos seguem os SEUS ângulos do E-C1 em tempo real. **O entregável-vitrine do bloco.**
- **Decisão de simulador:** comece por uma mão simples de URDF pronta. A Amazing Hand e a DexHand têm modelos; se a integração travar, use qualquer mão genérica de 5 dedos só para validar o pipeline — o objetivo aqui é o *mapeamento*, não o realismo.
- **Estudo (~5h):** quickstart do PyBullet (carregar URDF, setar ângulos de junta, `stepSimulation`) + entender a estrutura de juntas de uma mão (quais juntas existem, limites de cada uma).
- **O ponto difícil (antecipado):** seus dedos têm 3 falanges; um servo controla tipicamente 1-2 juntas via tendão. O mapeamento NÃO é 1 keypoint → 1 junta. Você vai precisar decidir como um ângulo de flexão do MediaPipe vira o(s) comando(s) de junta da mão virtual. Comece com 2-3 dedos, não os 5.
- **Pronto quando:** vídeo lado a lado — sua mão movendo ↔ mão virtual espelhando, ao menos para indicador, médio e polegar.
- **Ensina:** o mapeamento humano→robô no espaço de juntas; a primeira sensação real de teleoperação. **🚧 GATE DE HARDWARE: só passe ao E-C3 com este vídeo pronto.**

### E-C3 — Decisão de hardware e plano de montagem
- **Entrega:** NÃO é código. É um documento de decisão: qual design de mão (Amazing Hand vs. DexHand vs. outro), lista de materiais (BOM) com preços reais no Brasil, e como você vai imprimir (impressora própria, serviço em Blumenau, ou maker da região).
- **Por que é um entregável formal:** comprar/imprimir errado custa semanas e dinheiro. Este documento é o seu gate financeiro — o equivalente ao "gate de compra" do relatório original.
- **Pontos a resolver no documento:**
  - **Servos:** evite SG90 (jitter, sem feedback de posição confiável). MG90S é o mínimo; servos de barramento serial (Feetech SCS0009, como na Amazing Hand) são bem melhores porque reportam posição — e *posição reportada é exatamente o que você vai precisar gravar como rótulo no Bloco D*.
  - **Controladora:** Arduino (Mega, se forem muitos servos) + driver PCA9685, ou a placa específica do design escolhido.
  - **Impressão:** material (PLA serve para v1; TPU flexível para partes que precisam ceder), e quem imprime.
  - **Câmera:** webcam que você já usa nos Blocos A-B serve.
- **Pronto quando:** BOM fechada, custo total estimado, fornecedor de impressão definido, pedido de servos feito (importação demora — peça durante o E-C2).
- **Ensina:** engenharia de hardware como decisão de projeto, não improviso.

---

## BLOCO D — A mão física e o aprendizado
*Tema: o mundo real. Aqui começa o investimento (~R$ 300–800 para uma mão, bem abaixo do braço).*

> **Nota de escopo:** os entregáveis abaixo estão deliberadamente menos detalhados que os Blocos A-B. Robótica física gera imprevistos (uma junta que emperra muda seu cronograma de uma semana). Quando você concluir o E-C2, voltamos aqui e quebramos cada um destes em tarefas de 30min-2h, com o conhecimento que você já terá acumulado. Detalhar agora seria inventar precisão falsa.

### E-D1 — Montagem e primeiro movimento
- **Entrega:** mão impressa, montada, com os servos respondendo. Um script Python (via Arduino) que move cada dedo individualmente por comando.
- **O inferno conhecido:** alinhamento de juntas e tensão de tendões/cordas. Todos os builds DIY relatam isso. Reserve tempo de calibração mecânica, não só de código.
- **Pronto quando:** você digita "dobra o indicador" e o indicador dobra, de forma repetível, para todos os dedos.

### E-D2 — Teleoperação: a mão real espelha você
- **Entrega:** o pipeline do E-C2, agora no hardware — sua mão na webcam, a mão robótica física segue. É a **"replicação de movimento"** do seu objetivo original.
- **A fragilidade que você aceitou aqui vira concreta:** quando você dobra os dedos, eles se ocluem na câmera, e o MediaPipe perde precisão. Espere que a teleoperação seja boa com a mão aberta e degrade com a mão fechada. Documentar *onde* degrada é parte do entregável (vira dado para o ML).
- **Pronto quando:** vídeo da mão física espelhando sua mão; relatório das condições onde funciona bem e onde falha.

### E-D3 — A ponte para o ML: definir a tarefa e coletar demonstrações
- **Entrega:** escolher UMA tarefa simples e fechada (ex.: "fechar a mão ao redor de um objeto na palma" ou "fazer o gesto de pinça para segurar algo leve"), e usar a teleoperação do E-D2 como **ferramenta de coleta de dados**: gravar pares (imagem da câmera + ângulos/posições dos servos) ao longo de muitas execuções.
- **Por que este entregável existe (não estava nos docs originais):** o salto "replicação → aprendizado" esconde a parte mais difícil. Aqui é onde sua formação em ciência de dados é o diferencial: a qualidade deste dataset determina tudo. Servos com feedback de posição (decisão do E-C3) tornam isto viável — você grava a posição real, não a comandada.
- **Pronto quando:** dataset de demonstrações da tarefa, com EDA (distribuição, qualidade por episódio, episódios ruins descartados). É o E5 do Bloco B, em escala física.

### E-D4 — Behavior cloning: a mão aprende 🏁
- **Entrega:** treinar uma rede em PyTorch (reaproveitando o loop de treino do E8/E9) que mapeia (imagem da câmera) → (ângulos dos servos), e rodar essa política na mão física: ela executa a tarefa **sozinha**, sem você na câmera.
- **Arquitetura:** comece simples — uma CNN que prevê os ângulos-alvo a partir da imagem (é o que a HIRO Hand faz). Não precisa de ACT/Transformer na v1. Se quiser escalar depois, aí sim arquiteturas de chunking (como no relatório) entram — mas como extensão, não pré-requisito.
- **Por que PyTorch puro e não LeRobot:** o LeRobot não reconhece sua mão DIY de fábrica; adaptá-lo é um buraco de integração. Behavior cloning caseiro reusa tudo que você construiu no Bloco B e te dá controle total do pipeline.
- **Pronto quando:** a mão executa a tarefa autonomamente com taxa de sucesso mensurável (defina o protocolo: N tentativas, variação controlada), + relatório de experimentos.

### E-D5 — Extensão: iterar como cientista de dados
- **Entrega:** o ciclo dado→modelo→dado. Onde a política falha? Posições não cobertas? Oclusão? → colete dados direcionados nessas situações → retreine.
- **Pronto quando:** taxa de sucesso melhora de forma documentada entre versões do dataset/modelo.

---

## Resumo do esforço de estudo (material novo)

| Bloco | Estudo novo | Quando |
|---|---|---|
| C (E-C1 a E-C3) | ~7h + decisão de hardware | Após Bloco B |
| D (E-D1 a E-D5) | ~6h + montagem + iteração | Mão física em diante |

## O fio condutor (por que nada é desperdiçado)

```
Bloco A (visão: keypoints, features)
   └─► E-C1 ângulos como sinal de controle
         └─► E-C2 mão virtual espelha você (GATE hardware)
               └─► E-D2 mão física espelha você  ← "replicação"
                     └─► E-D3 teleoperação coleta demonstrações
                           └─► E-D4 behavior cloning  ← "aprendizado"
                                 (reusa loop de treino do Bloco B / E8-E9)
```

Sua sequência original — "keypoints → replicação → aprendizado" — está estruturalmente correta. O que estes blocos adicionam é o **elo que conecta replicação e aprendizado**: a teleoperação não é só o produto intermediário, ela é a *ferramenta que gera os dados* do ML. Sem esse elo explícito, os dois últimos passos seriam projetos desconexos.
