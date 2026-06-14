# Quebra de Tarefas — Blocos A e B (E1 a E9)
### Cada tarefa: 30min a 2h. A soma das tarefas = o entregável. A soma dos entregáveis = o sistema.

**Convenções:**
- `[estudo]` = tarefa de consumir material, com link/fonte e duração
- `[código]` = tarefa de construir
- `[teste]` = tarefa de validar
- Cada tarefa produz algo verificável. Se uma tarefa não tem como você provar que terminou, ela está mal definida.
- Marque com checkbox no seu repositório e anote travamentos no NOTES.md do entregável.

---

# BLOCO A — A mão como sensor

## E1 — Webcam ao vivo (≈ 1 semana, ~6h)

- [ ] **T1.1** `[código]` Setup do ambiente: instalar Python 3.10+, criar venv (`python -m venv` ou uv), instalar `opencv-python`, criar o repositório `imitation-arm/` com a estrutura de pastas e README. *Prova: `import cv2` roda sem erro.* (~45min)
- [ ] **T1.2** `[estudo]` Curso OpenCV freeCodeCamp (YouTube): assistir só as seções de leitura de imagem/vídeo e desenho sobre frames. (~1h30)
- [ ] **T1.3** `[código]` Capturar UM frame da webcam e salvar como `frame.png`. *Prova: o arquivo existe e mostra você.* (~30min)
- [ ] **T1.4** `[código]` Loop de vídeo: exibir frames continuamente numa janela, encerrar com a tecla `q`. *Prova: vídeo fluido, fecha limpo.* (~45min)
- [ ] **T1.5** `[código]` Desenhar sobre o frame: um texto fixo e um retângulo usando `cv2.putText` e `cv2.rectangle`. (~30min)
- [ ] **T1.6** `[código]` Medir FPS real (tempo entre frames com `time.time()`, média móvel das últimas 30 medições) e exibir no canto da tela. *Prova: ~30 FPS estável.* (~1h)
- [ ] **T1.7** `[código]` Refatorar: encapsular o loop numa função/classe `VideoLoop` reutilizável (você vai usá-la em TODOS os entregáveis seguintes) + escrever o NOTES.md. (~1h)

**Integração:** o `VideoLoop` do T1.7 é a fundação. E2 em diante são plugins dentro dele.

---

## E2 — Os 21 pontos da mão (≈ 1 semana, ~6h)

- [ ] **T2.1** `[estudo]` Documentação do MediaPipe Hand Landmarker (guia Python): ler a página de overview + entender o diagrama dos 21 landmarks (decorar: 4=polegar, 8=indicador, 12=médio, 16=anelar, 20=mínimo — as pontas). (~1h)
- [ ] **T2.2** `[código]` Instalar `mediapipe` e rodar o exemplo oficial numa FOTO estática da sua mão. *Prova: imagem salva com os pontos desenhados.* (~45min)
- [ ] **T2.3** `[código]` Integrar ao seu `VideoLoop`: detecção em tempo real com o utilitário de desenho padrão do MediaPipe. *Prova: pontos seguem sua mão ao vivo.* (~1h)
- [ ] **T2.4** `[código]` Acessar landmarks programaticamente: imprimir no terminal a coordenada da ponta do indicador (landmark 8) a cada frame. Entender que x, y vêm normalizados (0–1) e z é profundidade relativa. (~45min)
- [ ] **T2.5** `[código]` Converter coordenadas normalizadas → pixels e desenhar VOCÊ MESMO os 21 pontos e as conexões (sem o utilitário pronto): círculos nas juntas, linhas nos ossos, cores diferentes por dedo. *Prova: seu desenho substitui o padrão.* (~1h30)
- [ ] **T2.6** `[código]` Robustez: tratar os casos "nenhuma mão no quadro" (não pode crashar) e "duas mãos" (identificar esquerda/direita pelo campo `handedness`). (~45min)
- [ ] **T2.7** `[teste]` Medir o impacto no FPS (comparar com E1). Anotar no NOTES.md: FPS antes/depois, e em que condições o tracking falha (pouca luz, mão de lado, movimento rápido). (~30min)

**Integração:** o T2.5 prova que você domina a estrutura de dados; é ela que alimenta o E3.

---

## E3 — Da imagem ao número (≈ 1 semana, ~7h)

- [ ] **T3.1** `[estudo]` Revisar produto escalar e ângulo entre vetores (qualquer vídeo curto de álgebra vetorial, ex.: 3Blue1Brown *Essence of Linear Algebra*, episódio de dot product). (~45min)
- [ ] **T3.2** `[código]` Função `vetor(p1, p2)` que retorna o vetor entre dois landmarks, e `angulo(p1, p2, p3)` que retorna o ângulo no ponto p2 via produto escalar. Testar com pontos sintéticos cujo ângulo você sabe (ex.: 90°). *Prova: teste unitário passa.* (~1h)
- [ ] **T3.3** `[código]` Aplicar ao vivo: calcular o ângulo de flexão do indicador (landmarks 5-6-8) e exibir o número na tela ao lado do dedo. *Prova: dedo esticado ≈170–180°, dobrado <90°.* (~45min)
- [ ] **T3.4** `[código]` Generalizar: ângulo de flexão dos 5 dedos, exibidos simultaneamente. (~45min)
- [ ] **T3.5** `[código]` Distâncias: medir a distância polegar-indicador (gesto de pinça) normalizada pelo tamanho da mão (para não variar com a distância da câmera). (~1h)
- [ ] **T3.6** `[código]` Gráfico ao vivo: plotar a série temporal dos últimos ~100 valores de 2 features. Dica: desenhar o gráfico no próprio frame com OpenCV (polylines sobre um retângulo) é mais simples e rápido que matplotlib animado. *Prova: dobrar o dedo move a curva.* (~1h30)
- [ ] **T3.7** `[código]` Suavização: média móvel (deque de 5 frames) nas features para reduzir o tremido (jitter). Comparar visualmente com/sem. (~45min)
- [ ] **T3.8** `[código]` Refatorar: módulo `features.py` com todas as funções, importável pelos próximos entregáveis + NOTES.md. (~30min)

**Integração:** `features.py` é o tradutor imagem→número. E4 (regras), E5 (coleta) e E6 (ML) consomem ele.

---

## E4 — Gestos por regras (≈ 1 semana, ~5h)

- [ ] **T4.1** `[código]` No papel/NOTES.md: tabela de definição — para cada um dos 5 gestos (mão aberta, punho, joinha, paz, apontar), quais condições sobre ângulos/distâncias o definem. (~45min)
- [ ] **T4.2** `[código]` Detector binário "dedo levantado vs. dobrado" por threshold de ângulo, para cada dedo (atenção: o polegar tem geometria diferente — use distância, não ângulo). *Prova: 5 indicadores na tela, um por dedo.* (~1h)
- [ ] **T4.3** `[código]` Contador de dedos levantados (0–5) exibido grande na tela. (~30min)
- [ ] **T4.4** `[código]` Classificador por combinação: mapear o padrão de dedos → nome do gesto, exibido na tela. (~45min)
- [ ] **T4.5** `[código]` Debounce temporal: o gesto só é confirmado se mantido por N frames consecutivos (ex.: 10) — elimina oscilação durante a transição. (~45min)
- [ ] **T4.6** `[teste]` Teste sistemático de quebra: tabela no NOTES.md testando cada gesto em 6 condições (mão rotacionada, mão longe, mão perto, pouca luz, mão esquerda, movimento rápido). Marcar ✅/❌. (~1h)
- [ ] **T4.7** `[código]` Conclusão escrita no NOTES.md: onde regras bastam, onde quebram, e por quê — este texto é a justificativa do Bloco B. (~30min)

**🏁 Marco do Bloco A:** grave um vídeo de 1 minuto do sistema funcionando. Você tem um produto completo sem ter treinado nenhum modelo.

---

# BLOCO B — O primeiro ML

## E5 — Coletor de dataset (≈ 1 semana, ~5h)

- [ ] **T5.1** `[código]` Desenhar o schema do CSV antes de codar: colunas = 21 landmarks × (x,y,z) + features do E3 + `gesto` (rótulo) + `sessao` + `timestamp`. Justificar cada coluna no NOTES.md. (~45min)
- [ ] **T5.2** `[código]` Modo coleta no `VideoLoop`: segurar a tecla 1–5 grava amostras rotuladas com o gesto correspondente; HUD mostra contagem por classe ao vivo. (~1h30)
- [ ] **T5.3** `[código]` Metadado de sessão: cada execução do coletor gera um `sessao_id` (data-hora). **Por quê:** validar treino/teste separando por sessão é o que impede vazamento — duas amostras da mesma sessão são quase idênticas. (~30min)
- [ ] **T5.4** `[código]` Coletar de verdade: ≥300 amostras/gesto, em ≥2 sessões em dias/iluminações diferentes, variando posição e rotação da mão deliberadamente. (~1h, mecânico)
- [ ] **T5.5** `[código]` Notebook de EDA: distribuição por classe e por sessão, scatter de 2 features coloridas por gesto (as classes separam visualmente?), amostras anômalas. (~1h15)

## E6 — Classificador clássico (≈ 1 semana, ~5h)

- [ ] **T6.1** `[código]` Carregar o CSV, split treino/teste **por sessão** (sessão A treina, sessão B testa — nunca `train_test_split` aleatório aqui). (~45min)
- [ ] **T6.2** `[código]` Baseline: RandomForest do sklearn com hiperparâmetros padrão. Reportar acurácia no teste. (~45min)
- [ ] **T6.3** `[código]` Matriz de confusão + análise: quais gestos se confundem entre si? Faz sentido geométrico? Anotar. (~1h)
- [ ] **T6.4** `[código]` Inferência ao vivo: salvar o modelo (joblib), carregar no `VideoLoop`, prever o gesto a cada frame com debounce do E4. *Prova: nome do gesto na tela, agora vindo do modelo.* (~1h)
- [ ] **T6.5** `[teste]` Repetir a tabela de quebra do T4.6 com o modelo. Comparar lado a lado regras vs. ML no NOTES.md: onde o ML ganhou? Onde ainda falha? (~1h)

## E7 — Gestos dinâmicos (≈ 1 semana, ~5h)

- [ ] **T7.1** `[estudo]` Conceito de janela deslizante (sliding window) em séries temporais — qualquer artigo/vídeo curto. (~30min)
- [ ] **T7.2** `[código]` Adaptar o coletor: gravar SEQUÊNCIAS de 30 frames rotuladas (tecla pressionada = início da janela) para 3 gestos dinâmicos: acenar, círculo, deslizar. Coletar ~100 sequências/gesto. (~1h30)
- [ ] **T7.3** `[código]` Features agregadas por janela: média, desvio, amplitude e velocidade média de cada feature do E3 ao longo dos 30 frames → uma linha por sequência. (~1h)
- [ ] **T7.4** `[código]` Treinar RandomForest nessas features agregadas; matriz de confusão. (~45min)
- [ ] **T7.5** `[código]` Inferência ao vivo com janela deslizante: buffer dos últimos 30 frames, prever a cada N frames. Medir a latência percebida (deve ser <1s). (~1h15)

## E8 — ⚡ PyTorch entra (≈ 1,5 semana, ~9h)

- [ ] **T8.1** `[estudo]` PyTorch *Learn the Basics* (docs oficiais), partes 1–3: Tensors, Datasets & DataLoaders, Autograd. Fazer digitando junto, não só lendo. (~3h)
- [ ] **T8.2** `[código]` `GestureDataset(torch.utils.data.Dataset)` que lê SEU CSV do E5 e entrega (features_tensor, label); embrulhar num DataLoader com batches. *Prova: iterar um batch e imprimir shapes corretos.* (~1h)
- [ ] **T8.3** `[código]` MLP pequena (ex.: entrada → 64 → 32 → 5 classes) + loop de treino completo escrito À MÃO: forward, loss (CrossEntropy), backward, optimizer.step. Sem copiar-colar sem entender — regra: você explica cada linha. (~2h)
- [ ] **T8.4** `[código]` Curvas: loss e acurácia de treino/validação por época, plotadas. Identificar overfitting se houver. (~1h)
- [ ] **T8.5** `[código]` Salvar checkpoint (`state_dict`), carregar num script separado e plugar no `VideoLoop` no lugar do sklearn. (~1h)
- [ ] **T8.6** `[teste]` Comparação honesta no NOTES.md: acurácia, tempo de treino e complexidade sklearn vs. PyTorch. Conclusão esperada: empate técnico — e a explicação de por que mesmo assim o PyTorch é necessário daqui pra frente (modelos sequenciais, GPU, LeRobot). (~1h)

## E9 — Rede sequencial (≈ 1 semana, ~7h)

- [ ] **T9.1** `[estudo]` Um tutorial de classificação de sequências com GRU/LSTM em PyTorch (docs oficiais ou tutorial bem avaliado). Foco: formato dos tensores (batch, seq_len, features). (~2h)
- [ ] **T9.2** `[código]` Dataset sequencial: cada amostra = tensor (30, n_features) das sequências do E7, sem agregação. (~1h)
- [ ] **T9.3** `[código]` GRU pequena (1 camada, hidden 64) + cabeça de classificação; treinar com o mesmo loop do E8 (reuso!). (~1h30)
- [ ] **T9.4** `[teste]` Comparar com o E7 (features agregadas + RF): acurácia e matriz de confusão. A GRU ganha? Em quais gestos? Vale a complexidade? Escrever o veredito. (~1h)
- [ ] **T9.5** `[código]` Inferência ao vivo da GRU com o buffer deslizante do T7.5. (~1h30)

**🏁 Marco do Bloco B:** você tem um pipeline completo coleta→treino→deploy ao vivo, em duas tecnologias, com análise comparativa documentada. Este é o momento de voltar aqui para quebrarmos o Bloco C (braço simulado) — as tarefas dele serão melhores definidas com o que você terá aprendido.

---

## Visão de montagem (como as peças viram o sistema)

```
E1 VideoLoop ──────────────┐
E2 landmarks ──────────────┤
E3 features.py ────────────┼──► E4 regras ──► (justifica) ──► E6 ML
                           │         E5 coletor ──► dataset ──┘
                           │         E7 sequências ──► E9 GRU
                           │         E8 PyTorch (loop de treino) ─┘
                           ▼
              Bloco C: mesmos blocos, novo alvo
              (E10 pose do braço usa VideoLoop + features.py;
               E13 LeRobot usa o conhecimento do loop de treino do E8)
```

Nada é descartado: cada sub-entrega é um módulo que o próximo entregável importa.
