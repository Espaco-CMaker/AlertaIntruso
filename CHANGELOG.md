# CHANGELOG - AlertaIntruso

## v4.5.8 (20/02/2026)
### ✅ Aceite de Versao
- **ITEM**: MODIFICADO: Remocao da guia Performance e respectivas funcoes
- **ITEM**: ALTERADO: Adicionado script accept_release.py para automacao de aceite
- **ITEM**: CORRIGIDO: Removidas referencias e integracoes obsoletas de metricas
- **COMMIT**: pending

## v4.5.6 (19/02/2026)
### ✅ Hotfix: versão + commit visível
- **NOVO**: Aba **Sobre** exibe o hash curto do commit atual
- **NOVO**: Mensagem de início do sistema no Telegram inclui versão e commit
## v4.5.5 (04/02/2026)
### ✅ Aceite & Estabilização
- **FIX**: `photo_callback` e fila de fotos corrigidos (inclui `crop_path`)
- **FIX**: Implementado `TelegramBot.enviar_grupo_fotos()` (sendMediaGroup)
- **LOG**: STDERR classificado como **ERROR**
- **LOG**: Filtros INFO/WARN/ERROR movidos para a aba Logs
- **LOG**: Botão “Limpar Logs” apaga histórico (log.txt) e fila
- **TELEGRAM**: Watchdog não é mais enviado; WARN não é enviado ao Telegram
- **UI**: Separadores compactados nas mensagens do Telegram

## v4.3.19 (02/02/2026)
### 🐛 Correção Crítica
- **BUG FIX CRÍTICO**: Corrigido bug de "Confiança: 0.0%" em alertas Telegram
- **Causa**: `conf_avg` era recalculado a cada foto usando apenas as detecções do frame atual
- **Problema**: Frames subsequentes sem detecções acima do threshold resultavam em `conf_avg=0.0`
- **Solução**: Armazenado `conf_avg` do evento inicial no atributo `_event_conf_avg`
- **Resultado**: Todas as fotos do mesmo evento agora usam a confiança original da detecção que disparou o evento
- **Garantia**: Valor de confiança consistente e correto em todas as fotos de um evento

## v4.3.18 (02/02/2026)
### 🎨 Melhorias Visuais + 🐛 Correção
- **Telegram**: Emoji-based color coding para níveis de confiança
  - 🟢 Verde: Confiança ≥ 70%
  - 🟡 Amarelo: Confiança entre 50-69%
  - 🟠 Laranja: Confiança < 50%
- **Telegram**: Alertas críticos com código de cores
  - 🔴 Vermelho: Problemas críticos (RTSP, conexão)
  - 🟠 Laranja: Avisos (reconnect, falhas)
  - 🟡 Amarelo: Informações críticas
- **FIX**: Safe division em `conf_pct` para evitar display incorreto

## v4.3.17 (02/02/2026)
### 🐛 Correção Crítica
- **BUG FIX**: Adicionada dupla validação de confiança após NMS
- **Causa**: `cv2.dnn.NMSBoxes` não filtra por threshold de confiança
- **Problema**: Detecções com confiança abaixo do threshold configurado eram aceitas
- **Solução**: Loop de validação adicional após NMS verificando `confs[i] >= self.conf_th`
- **Garantia**: Apenas detecções com confiança ≥ threshold configurado são processadas

## v4.3.16 (02/02/2026)
### 🐛 Correções
- **Performance**: Fallback para bitrate interno se NetworkMonitor indisponível
- Aba Performance agora exibe todas as métricas mesmo sem Scapy/Npcap

## v4.3.15 (02/02/2026)
### 🔧 Correções
- **GUI**: Conteúdo da aba Config agora visível com scroll funcional
- Botões de controle fixos na base (não afetados pelo scroll)

## v4.3.14 (02/02/2026)
### ✨ Melhorias
- **GUI**: Fotos mais novas aparecem primeiro na aba Fotos
- Eventos antigos descem automaticamente

## v4.3.13 (02/02/2026)
### ✨ Melhorias
- **GUI**: Botões de controle (Salvar, Recarregar, Iniciar, Parar) agora fixos na base
- Não são mais cortados mesmo em tela cheia

## v4.3.12 (02/02/2026)
### ✨ Melhorias
- **GUI**: Scroll na aba Config para facilitar navegação
- Label melhorado: "Intervalo mín. entre fotos (s)" mais descritivo
- Mouse wheel support para scroll suave

## v4.3.11 (02/02/2026)
### ✨ Otimizações
- **RTSP**: Backoff inicial aumentado de 2s para 5s
- Máximo de backoff aumentado de 20s para 30s
- Reduz ciclos rápidos de reconexão

## v4.3.10 (02/02/2026)
### 🔧 Correções
- **RTSP**: Timeout aumentado de 5s para 10s
- Buffer flush após reconectar (10 frames) para descartar dados stale
- Corrige problema de CAM3 reconnectando a cada ~30s

## v4.3.9 (02/02/2026)
### ✨ Melhorias
- **Detections**: Nomes de classes agora inclusos na mensagem Telegram
- Removido log "MOVIMENTO SEM PESSOA" (reduz spam)
- Mensagens mais compactas e focadas

## v4.3.8 (01/02/2026)
### ✨ Melhorias
- **Telegram**: Reduzida quantidade de dados por foto (1 decimal para floats)
- Precisão suficiente, economia de bandwidth

## v4.3.7 (01/02/2026)
### ✨ Melhorias
- **LogManager**: Detecta padrões críticos ("falha rtsp", "sem frame", etc)
- Erros críticos automaticamente encaminhados para Telegram
- Status operacional em tempo real

## v4.3.6 (01/02/2026)
### ✨ Novos
- **Telegram**: Botão "Testar envio" na aba Config
- Simula detecção com foto de teste para validar conexão

## v4.3.5 (01/02/2026)
### 🔧 Correções
- **GUI**: Camera frames agora vazios ao desconectar (sem frozen frames)
- Melhora visual quando há problema de conexão

## v4.3.4 (01/02/2026)
### ✨ Melhorias
- **GUI**: Checkbox "Auto-scroll automático" na aba Logs
- Persiste em config.ini
- Melhora UX para debugging

## v4.3.3 (31/01/2026)
### ✨ Melhorias
- **Telegram**: Reduzido separador de dashes (12 chars ao invés de 24)
- Mensagens mais compactas e limpas

## v4.3.2 (31/01/2026)
### ✨ Melhorias
- **Telegram**: Mensagens de início/parada do sistema mais amigáveis
- Formato: ✅ SISTEMA INICIADO / ⏹️ SISTEMA ENCERRADO
- Inclui emojis para melhor visualização

## v4.3.1 (31/01/2026)
### ✨ Melhorias
- **Telegram**: Detecção com métricas de qualidade
- Timestamp, confiança, FPS, latência
- Formato organizado e legível

## v4.3.0 (30/01/2026)
### ✨ Novos
- **NetworkMonitor**: Captura RTP em tempo real (Scapy)
- Bitrate real das câmeras
- Métricas avançadas de rede (latência, jitter, ping, perda)

## v4.2.4+ (Versões anteriores)
- Spinner animado de loading
- Indicadores de status descritivos
- Taxa de transferência em Mbps/MB/s
- Logs coloridos (ERROR em vermelho, WARN em laranja)
- Métricas avançadas de rede na aba Performance

