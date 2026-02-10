# Backlog - Melhorias e Correções Futuras

Este arquivo registra funcionalidades planejadas e melhorias a serem implementadas no AlertaIntruso.

---

## 📋 Pendentes

### [2026-02-04] Sistema de Comandos via Telegram

**Descrição:**
Implementar sistema de comandos interativos via Telegram Bot que permita controlar o sistema remotamente através do chat do grupo.

**Requisitos:**
- Comando `/help` ou similar que lista todos os comandos disponíveis e como utilizá-los
- Comando para ativar/desativar o sistema de monitoramento remotamente
- Checkbox na guia **Configurações** para habilitar/desabilitar a funcionalidade de comandos via Telegram
- Processamento de mensagens recebidas no grupo para identificar comandos
- Resposta automática com confirmação de execução ou erro

**Comandos Planejados:**
- `/help` - Lista todos os comandos disponíveis
- `/start` - Ativa o sistema de monitoramento
- `/stop` - Desativa o sistema de monitoramento
- `/status` - Retorna status atual do sistema (ativo/inativo, câmeras conectadas, etc.)

**Segurança:**
- Validar que comandos venham apenas do chat/grupo configurado
- Opção para restringir comandos a usuários autorizados

**Interface:**
- Nova seção na aba **Config** > **Telegram**
- `[ ] Permitir comandos via Telegram` (checkbox)
- Campo de texto para lista de IDs de usuários autorizados (opcional)

---

### [2026-02-04] Opções de Envio de Mídia (Foto/Vídeo)

**Descrição:**
Expandir opções de notificação no Telegram permitindo escolher entre envio de fotos ou vídeos, com controle de qualidade para ambos.

**Requisitos:**

#### 1. Envio de Foto (já implementado parcialmente)
- [x] Checkbox `[ ] Enviar foto` na aba **Config** > **Detector**
- [x] Controle de qualidade JPEG (50-100) já implementado
- [ ] Integrar checkbox com lógica de envio (atualmente sempre envia)

#### 2. Envio de Vídeo (novo)
- [ ] Checkbox `[ ] Enviar vídeo` na aba **Config** > **Detector**
- [ ] Spinbox **Qualidade do vídeo** (1-100, ex: CRF para codec H.264)
- [ ] Spinbox **Duração do vídeo** (segundos, ex: 5-30s)
- [ ] Label com dica: "Vídeo captura movimento antes e depois da detecção"

**Implementação:**
- Opções mutuamente exclusivas (foto OU vídeo) ou permitir ambas?
- Para vídeo: usar buffer circular de frames pré-detecção
- Codec: H.264 (mp4) para compatibilidade com Telegram
- Usar `cv2.VideoWriter` com qualidade configurável

**Layout Sugerido (aba Config > Detector):**
```
┌─ Notificações Telegram ───────────────────┐
│ [✓] Enviar foto                           │
│     Qualidade JPEG: [95] (50-100)         │
│                                            │
│ [ ] Enviar vídeo                           │
│     Qualidade: [23] (CRF: 0-51, menor=melhor)│
│     Duração: [10] segundos (5-30)          │
└────────────────────────────────────────────┘
```

**Telegram API:**
- Fotos: `sendPhoto` (já implementado)
- Vídeos: `sendVideo` (a implementar)
- Grupo de mídias: `sendMediaGroup` (já implementado para fotos)

---

## 📝 Notas

- Priorizar comandos via Telegram primeiro (maior impacto na usabilidade)
- Envio de vídeo requer mais testes de performance e armazenamento
- Considerar impacto no uso de banda e armazenamento temporário

---

## ✅ Concluído

_(Funcionalidades movidas para cá quando implementadas)_

