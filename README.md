# AlertaIntruso - Sistema de Alarme Inteligente por Visão Computacional

**Versão Atual Baseada na: 4.5.6** (19/02/2026)

## Descrição Geral

O **AlertaIntruso** é uma aplicação desktop em Python desenvolvida para monitoramento contínuo (24/7) de múltiplas câmeras IP via RTSP, utilizando detecção de pessoas com OpenCV DNN (YOLOv4-tiny). O sistema prioriza robustez operacional, tolerância a falhas de stream, controle de falsos positivos e rastreabilidade completa de eventos de movimento.

## Arquitetura

- **Thread dedicada por câmera** (RTSPObjectDetector)
- **Interface gráfica centralizada** (Tkinter + ttk)
- **Comunicação thread-safe** via queue.Queue
- **Watchdog ativo** por câmera com soft reconnect e hard restart
- **Backoff progressivo** para reconexões RTSP
- **Persistência** via config.ini, log.txt, fotos/ e models/

## Fluxo de Detecção

1. Conexão RTSP resiliente (FFmpeg/OpenCV)
2. Leitura protegida de frames com tratamento de cv2.error e Exception
3. Validação do frame (None, tamanho zero, baixa variância)
4. Inferência YOLOv4-tiny
5. Filtro por classes habilitadas (pessoa por padrão)
6. Análise espacial: evento somente se pessoa cruza linha central
7. Classificação: movimento SEM pessoa → log informativo; COM pessoa → evento
8. Geração de EVENT_UID único
9. Captura de evidências (fotos espaçadas)
10. Notificação opcional (Telegram)
11. Atualização da interface gráfica

## Abas da Interface

### Vídeo
- Mosaico 2x2 redimensionável
- Overlays com bounding boxes, classe, confiança, timestamp

### Config
- RTSP por câmera
- Enable/disable por câmera
- Cooldown, thresholds (confiança/NMS)
- Classes habilitadas
- Telegram (token, chat, modo)
- Persistência em config.ini

### Fotos
- Agrupamento por EVENT_UID
- Miniaturas lado a lado
- Scroll vertical/horizontal
- Timestamp visível

### Logs
- Tempo real
- Histórico local
- Rotação automática
- Filtros por nível (INFO/WARN/ERROR)

### Performance
- Tabela profissional em tempo real com métricas por câmera
- FPS, CPU%, RAM%, Tempo de Inferência, Detecções Totais, GPU
- Alertas visuais para valores críticos (baixo FPS, alto CPU/RAM, inferência lenta)
- Média do sistema para CPU e RAM

## Resiliência RTSP/OpenCV

- Tratamento explícito de cv2.error, frames inválidos, erros H264, timeouts FFmpeg
- Reconexão automática com backoff
- Watchdog para detecção de travamentos

## Instalação e Execução

### Pré-requisitos
- Python 3.8+
- OpenCV com suporte a CUDA (opcional)
- Tkinter
- Requests
- psutil (opcional, para métricas de performance)

### Instalação
1. Clone o repositório: `git clone https://github.com/Espaco-CMaker/AlertaIntruso.git`
2. Instale dependências: `pip install opencv-python requests psutil`
3. Baixe modelos YOLO: Execute o script, ele baixa automaticamente
4. Configure config.ini com URLs RTSP e Telegram

### Execução
```bash
python "AlertaIntruso Claude+GPT.py"
```

## Configuração

Edite `config.ini`:
- [CAM1-4]: rtsp_url, enabled
- [DETECTOR]: cooldown_s, conf_th, nms_th, etc.
- [TELEGRAM]: bot_token, chat_id

## Logs e Monitoramento

- **log.txt**: Logs rotativos (5MB, backup automático)
- **fotos/**: Evidências por evento (EVENT_UID)
- **models/**: YOLOv4-tiny (baixado automaticamente)

## Desenvolvimento

- **Versão**: 4.5.6
- **Data**: 19/02/2026
- **Autor**: Fabio Bettio
- **Licença**: Uso educacional/experimental

## Changelog

### v3.9.3 (01/01/2026)
- Aba "Performance" redesenhada com tabela profissional (Treeview)
- Adicionado contador de detecções totais por câmera
- Interface mais profissional com colunas organizadas
- Alertas visuais baseados em thresholds (FPS baixo, CPU/RAM alto, inferência lenta)

### v3.9.2 (01/01/2026)
- Aba "Sobre" com versão, autor, data e link do GitHub
- Incremento automático de microversão para alterações

### v3.9.1 (01/01/2026)
- Log detalhado de eventos com parâmetros ativos
- Log explícito de inicialização
- Padronização de mensagens

### v3.9.0 (01/01/2026)
- Estabilização arquitetural
- EVENT_UID consistente
- Agrupamento visual de fotos
- Scroll na aba Fotos

### v3.8.6
- Miniaturas agrupadas por evento

### v3.8.5
- Evento apenas na linha central

### v3.8.4
- Reconexão RTSP robusta
- Watchdog por câmera

### v3.8.3
- Interface em abas
- Mosaico 2x2

## Contribuição

Para contribuir:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push e abra um Pull Request

## Suporte

Para dúvidas ou issues, abra uma issue no GitHub ou entre em contato.

---

*Sistema desenvolvido para aplicações de segurança residencial/comercial com foco em eficiência e confiabilidade.*

