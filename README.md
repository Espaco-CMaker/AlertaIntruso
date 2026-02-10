# AlertaIntruso - Sistema de Alarme Inteligente por Visão Computacional

**Versão Atual: 4.5.7** (10/02/2026)

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

- **Versão**: 4.5.7
- **Data**: 10/02/2026
- **Autor**: Fabio Bettio
- **Licença**: Uso educacional/experimental

## Changelog (Últimas 20 Versões)

### v4.5.7 (10/02/2026) - Correções e Melhorias de UX
- Scroll do mouse habilitado na aba Fotos (MouseWheel binding)
- Filtros de log corrigidos (linhas sem nível tratadas como INFO)
- Evento movimento agora é INFO (não WARN)
- Linha divisória entre dias corrigida (horizontal, posicionamento correto)
- Fotos persistentes ao reiniciar aplicação (carrega do diretório)

### v4.5.6 (04/02/2026) - Validação Final
- Controle de qualidade JPEG configurável (50-100) na aba Config
- Layout UI ajustado sem sobreposição de controles
- Fotos enviadas ao Telegram com qualidade configurável
- Sistema estável e pronto para uso

### v4.5.5 (04/02/2026) - Aceite & Estabilização
- photo_callback e fila de fotos corrigidos (inclui crop_path)
- Implementado TelegramBot.enviar_grupo_fotos() (sendMediaGroup)
- Logs e filtros INFO/WARN/ERROR na aba Logs
- Botão Limpar Logs apaga histórico

### v4.3.19 (02/02/2026) - Correção Crítica
- BUG FIX CRÍTICO: Corrigido bug de "Confiança: 0.0%" em alertas Telegram
- Armazenado conf_avg do evento inicial no atributo _event_conf_avg
- Todas as fotos do mesmo evento usam a confiança original

### v4.3.18 (02/02/2026) - Melhorias Visuais
- Emoji-based color coding para níveis de confiança
- Alertas críticos com código de cores
- Safe division em conf_pct

### v4.3.17 (02/02/2026) - Correção Crítica
- Dupla validação de confiança após NMS
- Apenas detecções com confiança ≥ threshold configurado são processadas

### v4.3.16 (02/02/2026) - Correções
- Fallback para bitrate interno se NetworkMonitor indisponível
- Aba Performance exibe métricas mesmo sem Scapy/Npcap

### v4.3.15 (02/02/2026) - Correções GUI
- Conteúdo da aba Config visível com scroll funcional
- Botões de controle fixos na base

### v4.3.14 (02/02/2026) - Melhorias GUI
- Fotos mais novas aparecem primeiro na aba Fotos
- Eventos antigos descem automaticamente

### v4.3.13 (02/02/2026) - Melhorias GUI
- Botões de controle fixos na base
- Não cortados em tela cheia

### v4.3.12 (02/02/2026) - Melhorias GUI
- Scroll na aba Config para navegação
- Label melhorado: "Intervalo mín. entre fotos (s)"
- Mouse wheel support

### v4.3.11 (02/02/2026) - Otimizações RTSP
- Backoff inicial aumentado de 2s para 5s
- Máximo de backoff de 20s para 30s
- Reduz ciclos rápidos de reconexão

### v4.3.10 (02/02/2026) - Correções RTSP
- Timeout aumentado de 5s para 10s
- Buffer flush após reconectar (10 frames)
- Corrige CAM3 reconnectando a cada ~30s

### v4.3.9 (02/02/2026) - Melhorias
- Nomes de classes na mensagem Telegram
- Removido log "MOVIMENTO SEM PESSOA"
- Mensagens mais compactas

### v4.3.8 (01/02/2026) - Melhorias Telegram
- Reduzida quantidade de dados por foto (1 decimal)
- Economia de bandwidth

### v4.3.7 (01/02/2026) - Melhorias LogManager
- Detecta padrões críticos ("falha rtsp", "sem frame")
- Erros críticos para Telegram
- Status operacional em tempo real

### v4.3.6 (01/02/2026) - Novo Recurso
- Botão "Testar envio" na aba Config
- Simula detecção com foto de teste

### v4.3.5 (01/02/2026) - Correções GUI
- Camera frames vazios ao desconectar (sem frozen frames)
- Melhora visual em problemas de conexão

### v4.3.4 (01/02/2026) - Melhorias GUI
- Checkbox "Auto-scroll automático" na aba Logs
- Persiste em config.ini
- Melhora UX para debugging

### v4.3.3 (31/01/2026) - Melhorias Telegram
- Reduzido separador de dashes (12 chars)
- Mensagens mais compactas

**Para histórico completo, consulte [CHANGELOG.md](CHANGELOG.md)**

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