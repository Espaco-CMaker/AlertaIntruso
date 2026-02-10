# 📥 Guia de Download e Instalação - AlertaIntruso v4.5.7

> Tudo o que você precisa saber para baixar, instalar e começar a usar AlertaIntruso

---

## 🎯 Escolha Sua Opção de Download

### ⭐ **Opção 1: Executável Windows (Recomendado)**

**Melhor para**: Usuários que querem usar imediatamente sem instalar Python

```
📦 AlertaIntruso-v4.5.7-Windows-x64.exe
├── Tamanho: ~200 MB
├── Requer: Windows 10/11 x64
├── Python: ❌ Não necessário
├── Setup: 🟢 Pronto para usar
└── Modelos: ✅ YOLO incluído
```

#### ✅ Vantagens
- Sem dependências Python
- Instalação em 1 clique
- Modelo YOLO pré-incluído (48MB)
- Atualizações integradas
- Suporte direto ao Windows

#### 📥 Como Instalar
1. **Baixe** o arquivo `.exe`
2. **Execute** o instalador
3. **Siga** as instruções na tela
4. **Pronto!** Inicie a aplicação

#### ⚙️ Requisitos Mínimos
- Windows 10/11 (64-bit)
- 2GB RAM
- 300MB espaço em disco
- Internet (para Telegram)

#### 🚀 Primeiro Uso
1. Abra AlertaIntruso
2. Vá para aba **"Config"**
3. Adicione URL RTSP da câmera (opcional: Telegram)
4. Clique em **"Enable"** na câmera
5. Vá para aba **"Vídeo"** e veja o stream em tempo real

---

### 💻 **Opção 2: Código-Fonte (Desenvolvimento)**

**Melhor para**: Desenvolvedores que querem modificar/contribuir

#### 📥 Como Instalar

**1. Clone o repositório:**
```bash
git clone https://github.com/Espaco-CMaker/AlertaIntruso.git
cd AlertaIntruso
```

**2. Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Execute a aplicação:**
```bash
python "AlertaIntruso Claude+GPT.py"
```

#### 📋 Dependências Principais
```
opencv-python>=4.13.0        # Visão computacional
requests>=2.31.0             # Telegram API
psutil>=5.9.0                # Métricas de performance
numpy>=1.24.0                # Computação numérica
Pillow>=9.0.0                # Processamento de imagens
```

#### 🔧 Requisitos de Sistema
- Python 3.8+ (3.10+ recomendado)
- 2GB RAM mínimo
- 500MB espaço em disco
- Windows/Linux/macOS

#### 💡 Dicas de Desenvolvimento
- Use Python 3.10+ para melhor performance
- Configure GPU CUDA se disponível (OpenCV)
- Ative logging DEBUG para troubleshooting
- Contribua suas melhorias via Pull Requests

---

### 🐳 **Opção 3: Docker (Experimental)**

**Melhor para**: Ambientes containerizados com suporte a GPU

```bash
docker run -it --gpus all \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/fotos:/app/fotos \
  espaco-cmaker/alerta-intruso:4.5.7
```

**Status**: Em desenvolvimento - disponível em breve

---

## 🎬 Guia Rápido de Primeiro Uso

### Pré-requisitos
✅ AlertaIntruso instalado  
✅ Câmera IP com acesso RTSP (opcional)  
✅ Token Telegram Bot (opcional)  

### Passo a Passo (5 minutos)

#### 1️⃣ Inicie a Aplicação
```
Windows: Execute AlertaIntruso.exe
Linux: python "AlertaIntruso Claude+GPT.py"
```

#### 2️⃣ Configure sua Câmera
- Aba: **Config**
- Seção: **CAM1**
- Campo: `rtsp_url`
- Valor: `rtsp://usuario:senha@192.168.1.100:554/stream`
- Clique: **Enable**

#### 3️⃣ Visualize o Stream
- Aba: **Vídeo**
- Você deve ver a câmera ao vivo em tempo real
- A detecção acontece automaticamente

#### 4️⃣ Configure Telegram (Opcional)
- Aba: **Config**
- Seção: **TELEGRAM**
- Campos: `bot_token` e `chat_id`
- Clique: **Testar envio** para validar

#### 5️⃣ Comece a Monitorar!
- Aba: **Logs** - veja eventos em tempo real
- Aba: **Fotos** - acesse as evidências
- Aba: **Performance** - monitore CPU/RAM/FPS

---

## 🔧 Configuração Detalhada

### Arquivo: `config.ini`

#### Seção [CAM1-4]
```ini
[CAM1]
enabled = True
rtsp_url = rtsp://admin:1578@192.168.1.100:554/stream

[CAM2]
enabled = True
rtsp_url = rtsp://admin:1578@192.168.1.101:554/stream

[CAM3]
enabled = False
rtsp_url = 

[CAM4]
enabled = False
rtsp_url = 
```

#### Seção [DETECTOR]
```ini
[DETECTOR]
cooldown = 3                          # Segundos entre detecções
confidence_threshold = 0.20           # Confiança mínima (0-1)
nms_threshold = 0.30                  # Non-Max Suppression
photos_per_event = 1                  # Fotos por evento
classes_enabled = person,car,dog      # Objetos para detectar
min_capture_interval_s = 6.0          # Intervalo mínimo entre fotos
skip_frames = 2                       # Pular frames (performance)
input_size = 320                      # Resolução YOLO (320/416/608)
rtsp_transport = udp                  # UDP ou TCP
max_photos_keep = 500                 # Máximo de fotos armazenadas
jpeg_quality = 100                    # Qualidade JPEG (1-100)
```

#### Seção [TELEGRAM]
```ini
[TELEGRAM]
bot_token = 1225244164:AAEjzOPGYWUlCQAeSCz-LnqvMRSKIeiDBpA
chat_id = -1003752805157
alert_mode = all                      # all, critical, none
```

#### Seção [UI]
```ini
[UI]
show_tips = True                      # Mostrar dicas?
auto_scroll_logs = True               # Auto-scroll nos logs
log_show_info = False                 # Mostrar logs INFO
log_show_warn = True                  # Mostrar logs WARN
log_show_error = True                 # Mostrar logs ERROR
```

---

## 🔗 Encontrando URLs RTSP

### Como Obter a URL RTSP da Sua Câmera

#### 1. Câmeras Comuns
```
Hikvision:   rtsp://admin:senha@IP:554/stream
Uniview:     rtsp://admin:senha@IP:554/h264/ch1/main
Dahua:       rtsp://admin:senha@IP:554/stream
Axis:        rtsp://admin:senha@IP:554/axis-media/media.amp
Intelbras:   rtsp://admin:senha@IP:554/stream
```

#### 2. Testar URL no VLC
- Abra VLC
- `File > Open Network Stream`
- Cole a URL
- Clique `Play`

#### 3. Se Funcionar no VLC
- Copie a URL para AlertaIntruso
- AlertaIntruso também funciona

---

## 🤖 Configurando Telegram

### Passo 1: Criar Bot no Telegram

1. Abra Telegram
2. Procure por **@BotFather**
3. Envie: `/start`
4. Envie: `/newbot`
5. Escolha nome e username
6. **Copie o TOKEN** (será: `1225244164:AAEjzOPGYWU...`)

### Passo 2: Obter Chat ID

1. Procure por **@userinfobot**
2. Envie qualquer mensagem
3. Ele retorna seu **Chat ID** (será: `123456789`)
4. Para grupos: comece com `-`

### Passo 3: Adicionar ao Config

```ini
[TELEGRAM]
bot_token = <SEU_TOKEN_AQUI>
chat_id = <SEU_CHAT_ID_AQUI>
alert_mode = all
```

### Passo 4: Testar

1. Aba **Config**
2. Clique botão **"Testar envio"**
3. Você receberá uma mensagem de teste

---

## 🐛 Troubleshooting Comum

### ❌ Câmera não conecta

**Problema**: "Falha ao conectar RTSP"

**Soluções**:
1. ✅ Verificar URL RTSP (testar no VLC primeiro)
2. ✅ Verificar credenciais (usuário/senha)
3. ✅ Verificar IP e porta (padrão 554)
4. ✅ Testar ping: `ping 192.168.1.100`
5. ✅ Aumentar timeout na config (udp → tcp)

---

### ❌ FPS muito baixo

**Problema**: "Apenas 2-3 fps, muito lento"

**Soluções**:
1. ✅ Aumentar `skip_frames` (2 → 3 ou 4)
2. ✅ Reduzir `input_size` (320 → 224)
3. ✅ Desabilitar câmeras não usadas
4. ✅ Instalar GPU CUDA (OpenCV)
5. ✅ Usar Python 3.12+ (mais rápido)

---

### ❌ Telegram não funciona

**Problema**: "Mensagens não chegam"

**Soluções**:
1. ✅ Validar TOKEN com @BotFather
2. ✅ Validar Chat ID com @userinfobot
3. ✅ Clique "Testar envio" para confirmar
4. ✅ Verificar conexão internet
5. ✅ Usar `alert_mode = critical` (menos mensagens)

---

### ❌ RAM/CPU muito alta

**Problema**: "Processo usando 80%+ CPU"

**Soluções**:
1. ✅ Reduzir número de câmeras
2. ✅ Aumentar `skip_frames`
3. ✅ Aumentar `min_capture_interval_s`
4. ✅ Fechar outras aplicações
5. ✅ Usar máquina com mais CPU/RAM

---

### ❌ Muitas fotos sendo salvas

**Problema**: "Fotos /1000+ consumindo espaço"

**Soluções**:
1. ✅ Aumentar `cooldown` (3s → 6s ou 10s)
2. ✅ Aumentar `min_capture_interval_s` (6s → 15s)
3. ✅ Reduzir `max_photos_keep` (500 → 100)
4. ✅ Aumentar `nms_threshold` (menos detecções)

---

## 📊 Monitorando Performance

### Métrica: FPS (Frames Por Segundo)
- ✅ Ideal: 15-30 fps
- ⚠️ Aceitável: 8-15 fps
- ❌ Problema: < 8 fps

### Métrica: CPU (Processador)
- ✅ Ideal: < 30%
- ⚠️ Aceitável: 30-50%
- ❌ Problema: > 50%

### Métrica: RAM (Memória)
- ✅ Ideal: < 500MB
- ⚠️ Aceitável: 500-800MB
- ❌ Problema: > 800MB

---

## 📖 Documentação Adicional

| Documento | Link |
|-----------|------|
| **README** | [README.md](README.md) |
| **Wiki** | [GitHub Wiki](https://github.com/Espaco-CMaker/AlertaIntruso/wiki) |
| **FAQ** | [Perguntas Frequentes](https://github.com/Espaco-CMaker/AlertaIntruso/wiki/FAQ) |
| **Issues** | [Reportar Bugs](https://github.com/Espaco-CMaker/AlertaIntruso/issues) |
| **Discussions** | [Comunidade](https://github.com/Espaco-CMaker/AlertaIntruso/discussions) |

---

## 🆘 Obter Suporte

### 1. Consultar FAQ
👉 [Perguntas Frequentes](https://github.com/Espaco-CMaker/AlertaIntruso/wiki/FAQ)

### 2. Procurar em Issues Abertas
👉 [GitHub Issues](https://github.com/Espaco-CMaker/AlertaIntruso/issues)

### 3. Fazer Pergunta na Comunidade
👉 [GitHub Discussions](https://github.com/Espaco-CMaker/AlertaIntruso/discussions)

### 4. Abrir Nova Issue
👉 [Novo Issue](https://github.com/Espaco-CMaker/AlertaIntruso/issues/new)

---

## 🎁 Próximas Ações

Após instalar:

1. ✅ Ler documentação
2. ✅ Configurar primeira câmera
3. ✅ Testar detecção (aba Vídeo)
4. ✅ Configurar Telegram (opcional)
5. ✅ Começar monitoramento
6. ✅ Explorar todas as abas

---

## 📞 Contato & Links

| Link | URL |
|------|-----|
| **GitHub** | https://github.com/Espaco-CMaker/AlertaIntruso |
| **Issues** | https://github.com/Espaco-CMaker/AlertaIntruso/issues |
| **Wiki** | https://github.com/Espaco-CMaker/AlertaIntruso/wiki |
| **Email** | [seu-email@exemplo.com] |

---

**Versão**: 4.5.7  
**Data**: 10/02/2026  
**Status**: ✅ Production Ready

Bom monitoramento! 🎉
