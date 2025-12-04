# 📋 Guia para o Pro Player Fornecer Conhecimento

Este guia é para **seu amigo Pro Player** entender como fornecer o conhecimento para a IA.

---

## 🎯 PARTE 1: Builds de Cartas (2 Tipos)

### Tipo A: Regras Gerais (Qualquer Carta)

**O que é:** Regras automáticas para 99% das cartas do jogo.

**Template do Google Sheets:**

Crie 1 planilha com aba "Regras por Posição":

| Posição | Estilo | Prioridade 1 | Mín P1 | Prioridade 2 | Mín P2 | Prioridade 3 | Mín P3 | Ignorar | Dica Tática |
|---------|--------|--------------|--------|--------------|--------|--------------|--------|---------|-------------|
| CB | Build-up | Defensive Engagement | 85 | Ground Pass | 75 | Speed | 70 | Finishing, Curl | Use para sair jogando |
| CB | Destroyer | Defensive Engagement | 90 | Physical Contact | 85 | Tight Possession | 75 | Finishing, Passes | Pressione agressivo |
| LB | Offensive | Speed | 85 | Stamina | 85 | Ground Pass | 75 | Heading, Finishing | Suba para cruzar |

**Preencha para:**
- CB (2 estilos: Build-up e Destroyer)
- LB/RB (2 estilos: Ofensivo e Defensivo)
- DMF (2 estilos: Anchor Man e Orchestrator)
- CMF (Box-to-Box)
- AMF (Classic No. 10)
- LWF/RWF (Prolific Winger)
- CF (2 estilos: Goal Poacher e Target Man)

**Total: ~12 linhas** (30 minutos de trabalho)

---

### Tipo B: Cartas Meta (Exceções)

**O que é:** Cartas que são "quebradas" e dominam o jogo.

**Template do Google Sheets:**

Crie aba "Cartas Meta":

| Jogador | Versão | Overall | Pos Principal | Por que é Meta? | CF Build | LWF Build | Quando Usar | Comentário |
|---------|--------|---------|---------------|-----------------|----------|-----------|-------------|------------|
| Neymar Jr | Big Time 2015 | 97 | LWF | Drible quebrado | Offensive:10, Finishing:10, Speed:8 | Dribbling:10, Speed:10, Curl:8 | Contra defesas lentas | Essa versão é absurda |
| CR7 | Legendary 2008 | 98 | CF | Físico + cabeceio | Offensive:10, Finishing:10, Header:9 | - | Sempre | Não tem fraqueza |

**Colunas Explicadas:**
- **Jogador/Versão**: Nome + ano da carta (ex: "Messi 2015", "CR7 2008")
- **Por que é Meta?**: 1 frase explicando (ex: "Drible + velocidade absurdos")
- **Build (por posição)**: Apenas 3-4 atributos principais com pontos
- **Quando Usar**: Em qual situação essa carta brilha
- **Comentário**: Sua opinião pessoal (pode xingar, ser engraçado)

**Meta ~5-10 cartas** que dominam o jogo atual.

---

## 🎮 PARTE 2: Gameplay (Problemas e Soluções)

### Método: "Médico e Paciente"

**O que é:** Usuário tem um **problema** (sintoma), você dá a **solução** (remédio).

### 🎤 JEITO MAIS FÁCIL: Gravar Áudio

**Não escreva! Fale!** É 10x mais rápido.

#### Passo a Passo:

1. **Pegue esta lista de 20 reclamações comuns:**

```
1. "Tomo muito gol no kick-off"
2. "Meu atacante erra gol cara a cara"
3. "Levo drible toda hora no 1v1"
4. "Não consigo driblar"
5. "Meus passes são interceptados"
6. "Fico sem stamina no 2º tempo"
7. "Goleiro adversário defende tudo"
8. "Não consigo sair jogando pela defesa"
9. "Levo gol de cruzamento sempre"
10. "Não consigo fazer contra-ataque"
11. "Quando pressiono, levanto buracos"
12. "Não sei quando usar finesse ou power shot"
13. "Meus jogadores não fazem as corridas"
14. "Time adversário passa pela minha defesa fácil"
15. "Não consigo marcar o Mbappe/Haaland"
16. "Perco muito gol de bola parada"
17. "Não consigo criar chances"
18. "Meu time fica muito parado"
19. "Levanto gol de long shot sempre"
20. "Não sei qual formação usar"
```

2. **Grave você respondendo:**

Use celular, Discord, Zoom, qualquer coisa.

**Formato:**
```
Pergunta 1: "Davi, o cara tá reclamando que toma gol no kick-off. O que ele faz?"

[VOCÊ RESPONDE FALANDO]
"Ah cara, isso é clássico. O problema é que logo depois que você faz gol, 
sua defesa fica toda desorganizada né. Aí o cara te pressiona e você já quer 
correr pra cima. Não faz isso! Segura o L2 e recua os cara. Espera uns 5 segundos, 
deixa a defesa organizar, aí sim você pressiona..."

Pergunta 2: "E quando o atacante erra gol cara a cara?"

[VOCÊ RESPONDE]
"Isso aí é porque o maluco tá correndo enquanto chuta. Tem que soltar o R2, 
esperar a bola encostar no pé, aí mira e chuta. Não pode fazer tudo junto..."
```

3. **Manda o áudio pra mim**

Eu uso IA pra transcrever automaticamente e organizo no JSON.

---

### 📝 Se PREFERIR escrever (mais trabalhoso):

Use este template:

**Template Google Sheets - Aba "Problemas Gameplay":**

| ID | Sintoma (reclamação) | Categoria | Solução (passo a passo) | Comandos | Erro Comum | Dica Extra |
|----|---------------------|-----------|-------------------------|----------|------------|------------|
| 1 | Tomo gol no kick-off | Defesa | 1. Não pressione logo\n2. Segure L2 e recue\n3. Espere 5s | L2 + Stick pra trás | Correr direto no atacante | Faça falta tática se necessário |
| 2 | Erro gol cara a cara | Finalização | 1. Solte R2\n2. Espere bola no pé\n3. Mire\n4. Chute | Soltar R2 → Mira → ⭕ | Chutar correndo | Finesse é mais confiável |

**20-30 problemas** são suficientes para MVP.

---

## 📊 RESUMO DO QUE VOCÊ PRECISA FORNECER

| Item | Formato | Tempo Estimado | Prioridade |
|------|---------|----------------|------------|
| **Regras por Posição** | Google Sheets (12 linhas) | 30 min | 🔴 ALTA |
| **Cartas Meta** | Google Sheets (5-10 cartas) | 1h | 🔴 ALTA |
| **Problemas Gameplay** | Áudio gravado (20 perguntas) | 30 min | 🟡 MÉDIA |

**Total: ~2 horas de trabalho** para ter MVP funcional.

---

## 🎯 PRIORIDADE PARA COMEÇAR

### Semana 1: Builds Básicos
1. Preencha "Regras por Posição" (12 linhas)
2. Adicione 3 cartas meta (Neymar, CR7, Messi)

### Semana 2: Gameplay
3. Grave áudio respondendo 10 problemas principais

### Semana 3+: Expansão
4. Adicione mais cartas meta conforme meta do jogo mudar
5. Adicione mais problemas de gameplay

---

## 📞 COMO ME ENVIAR

### Google Sheets:
- Compartilhe link comigo (me dá permissão de visualizar)
- Ou exporta pra Excel e manda

### Áudio:
- Whatsapp, Discord, Google Drive, qualquer coisa
- Formato: MP3, WAV, M4A (qualquer um serve)

### Dúvidas:
- Manda mensagem que eu explico melhor
- Podemos fazer chamada para eu te ajudar a preencher

---

## 💡 DICAS PRO PRO PLAYER

### Para Builds:
- **Seja específico**: "Offensive Awareness 10" é melhor que "Foca em ataque"
- **Justifique**: "Por que 10 pontos?" → "Porque movimentação é chave"
- **Seja honesto**: Se carta é ruim, fala "Essa carta é lixo, não usa"

### Para Gameplay:
- **Fale como você fala pro seus amigos**: Pode xingar, ser engraçado
- **Dê comandos EXATOS**: "R1 + ⭕" é melhor que "faz finesse"
- **Explique o erro**: "Por que tá errando?" é tão importante quanto "Como acerta"

### O que NÃO fazer:
- ❌ Escrever texto corrido gigante
- ❌ Ser muito técnico (usuário é noob)
- ❌ Dar dica genérica tipo "treina mais"

### O que fazer:
- ✅ Passos práticos: "1. Faz X, 2. Depois Y"
- ✅ Comandos específicos: "Segura L2 + aperta ⭕"
- ✅ Ser direto: "Tá errando porque..."

---

**Qualquer dúvida, me chama! Vamos fazer isso juntos.** 🚀
