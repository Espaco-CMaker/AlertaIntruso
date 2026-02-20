"""
================================================================================
ALERTAINTRUSO — ALARME INTELIGENTE POR VISÃO COMPUTACIONAL (RTSP • YOLO • MULTICAM)
================================================================================
Arquivo:        AlertaIntruso Claude+GPT.py
Projeto:        Sistema de Alarme Inteligente por Visão Computacional
Versão:         4.5.9
Data:           20/02/2026
Autor:          Fabio Bettio
Licença:        Uso educacional / experimental
Status:         ESTÁVEL

================================================================================
Descrição geral
================================================================================
Aplicação desktop em Python (Tkinter) para monitoramento contínuo (24/7) de
múltiplas câmeras IP via RTSP, com detecção de pessoas utilizando OpenCV DNN
(YOLOv4-tiny). O sistema prioriza robustez operacional, tolerância a falhas
de stream, controle de falsos positivos e rastreabilidade completa de eventos
de movimento.

================================================================================
Changelog completo
================================================================================
v4.5.9 (20/02/2026) [ANTI-SPAM ALERTAS] (linhas: 0)
    - NOVO: Eventos de presença com ENTRADA/MEIO/SAÍDA
    - NOVO: Alerta MEIO para presença prolongada/parada
    - NOVO: Alerta SAÍDA após timeout sem pessoa

v4.5.8 (20/02/2026) [ACEITE] (linhas: 0)
    - MODIFICADO: Remocao da guia Performance e respectivas funcoes
    - ALTERADO: Adicionado script accept_release.py para automacao de aceite
    - CORRIGIDO: Removidas referencias e integracoes obsoletas de metricas

v4.5.7 (20/02/2026) [ACEITE] (linhas: 0)
    - MODIFICADO: Remocao da guia Performance e respectivas funcoes
    - ALTERADO: Adicionado script accept_release.py para automacao de aceite
    - CORRIGIDO: Removidas referencias e integracoes obsoletas de metricas

v4.5.6 (19/02/2026) [HOTFIX] (linhas: 0)
    - NOVO: Aba Sobre exibe código do commit atual
    - MELHORIA: Mensagem de inicialização no Telegram inclui commit

v4.5.5 (04/02/2026) [ACEITE - ESTABILIZAÇÃO] (linhas: 0)
    - FIX: Callback de foto e fila corrigidos (crop_path) + método enviar_grupo_fotos()
    - LOG: STDERR agora classificado como ERROR
    - LOG: Filtros INFO/WARN/ERROR movidos para a aba Logs
    - LOG: Botão Limpar Logs apaga histórico (log.txt) e fila
    - TELEGRAM: Sem mensagens de watchdog e sem WARN no Telegram
    - UI: Redução de separadores em mensagens Telegram

v4.5.4 (04/02/2026) [PADRONIZAÇÃO - LOGS] (linhas: 55)
    - NOVO: Sistema de logs compatibilizado com ESPECIFICAÇÃO_LOGS do Guia_de_Padroes
    - FORMATO: Novo formato padronizado "%(asctime)s | %(levelname)-7s | %(name)-15s | %(message)s"
    - NOMENCLATURA: Loggers agora usam hierarquia de módulos (ex: "camera.detector", "telegram.bot")
    - MENSAGENS: Mensagens seguem padrões do guia (ação + contexto + detalhes)
    - ROTAÇÃO: Sistema de rotação automática (5MB por arquivo, 10 backups)
    - ESTRUTURA: Cabeçalho de inicialização padronizado com linhas separadoras
    - COMPATIBILIDADE: 100% compatível com especificação do Guia_de_Padroes

v4.5.3 (04/02/2026) [OTIMIZAÇÃO - TELEGRAM] (linhas: 85)
    - NOVO: Sistema de buffer para eventos de sistema no Telegram
    - NOVO: Mensagens de watchdog/reconnect/falhas agrupadas e enviadas em lote
    - OTIMIZAÇÃO: Redução drástica de mensagens Telegram em caso de instabilidade
    - IMPLEMENTAÇÃO: Buffer com envio a cada 30s ou quando atingir 10 eventos
    - MELHORIA: Mensagens agrupadas com timestamp individual e contador
    - PERFORMANCE: Evita flood de notificações em reconexões/falhas múltiplas
    - TELEGRAM: Envio único consolidado ao invés de uma mensagem por evento
    - CONFIGURÁVEL: system_events_buffer_time e system_events_buffer_max

v4.5.2 (04/02/2026) [FEATURE - TELEGRAM E DIAGNÓSTICO] (linhas: 136)
    - NOVO: Fotos enviadas em GRUPO (sendMediaGroup) - foto geral + crop na mesma msg
    - NOVO: Método TelegramBot.enviar_grupo_fotos() para múltiplas fotos por mensagem
    - MELHORIA: _save_and_notify() agora usa sendMediaGroup quando há crop disponível
    - TELEGRAM: Caption aparece apenas na primeira foto do grupo
    - DIAGNÓSTICO: Warning "No libpcap provider" suprimido do console
    - DIAGNÓSTICO: Log detalhado sobre status Scapy/Npcap no início do sistema
    - DIAGNÓSTICO: Detecção automática de problemas com libpcap mesmo com Scapy instalado
    - DOCUMENTAÇÃO: Criado NPCAP_INSTALL.md com guia completo de instalação
    - LOG: Sistema indica se bitrate será real (RTP) ou estimado (interno)
    - MELHORIA: Tratamento robusto de erros em enviar_grupo_fotos (timeout, conexão, arquivo)

v4.5.1 (04/02/2026) [BUILD] (linhas: 0)
    - Incremento de versão para gerar novo executável

v4.5.0 (04/02/2026) [FEATURE + FIX - LOGS E GESTÃO DE FOTOS] (linhas: 98)
    - NOVO: Limpeza automática de fotos antigas (manter apenas últimas X fotos)
    - NOVO: Configuração max_photos_keep na aba Config (padrão: 500)
    - NOVO: Função _cleanup_old_photos() chamada antes de salvar nova foto
    - MELHORIA: Logs de erro detalhados para Telegram (HTTP status, tipo erro, arquivo)
    - MELHORIA: Erros de Telegram agora são ERROR (não WARN)
    - DETALHAMENTO: Timeout, ConnectionError, FileNotFoundError com contexto completo
    - TELEGRAM: Logs incluem URL, ChatID, tamanho arquivo, resposta API
    - PERSISTÊNCIA: Tabela de fotos agora limitada ao máximo configurado
    - CONFIG.INI: Novo parâmetro max_photos_keep na seção [DETECTOR]

v4.4.0 (04/02/2026) [FEATURE - NOVA FUNCIONALIDADE] (linhas: 42)
    - NOVO: Salvar crop do objeto detectado em cada foto
    - NOVO: Enviar foto crop para Telegram junto com foto geral
    - NOVO: Exibir crop ao lado da foto geral na aba de fotos
    - NOVO: Linha separadora preta (3px) entre dias diferentes na aba de fotos
    - IMPLEMENTAÇÃO: Função _extract_object_crop com margem de 15%
    - MELHORIA: Callback de foto agora inclui path do crop (crop_path)
    - MELHORIA: Layout da aba de fotos com duas colunas (geral + crop)
    - RESULTADO: Cada deteção gera 2 fotos persistidas e exibidas
    - TELEGRAM: Foto crop enviada com prefixo "🔍 ZOOM -"

v4.3.20 (03/02/2026) [BUG FIX - CRÍTICO] (linhas: 1)
    - FIX CRÍTICO: Corrigido bug da "última foto sem objetos detectados"
    - CAUSA: Fotos pendentes eram salvas mesmo em frames SEM detecções
    - CENÁRIO: Com skip_frames=2, último frame processado pode não ter pessoa
    - PROBLEMA: Foto final chegava ao Telegram vazia/sem caixas de detecção
    - SOLUÇÃO: Adicionado verificação `and boxes and self._person_present(cids)` na linha 995
    - RESULTADO: Fotos agora só são tiradas quando há pessoas no frame ATUAL
    - Garantia: Todas as fotos enviadas têm objetos detectados visíveis

v4.3.19 (02/02/2026) [BUG FIX - CRÍTICO] (linhas: 0)
    - FIX CRÍTICO: Corrigido bug de "Confiança: 0.0%" em alertas Telegram
    - CAUSA: conf_avg era recalculado a cada foto usando detecções do frame atual
    - PROBLEMA: Frames subsequentes sem detecções resultavam em conf_avg=0.0
    - SOLUÇÃO: Armazenado conf_avg do evento inicial em _event_conf_avg
    - RESULTADO: Todas as fotos do mesmo evento agora usam a confiança original
    - Garantia: Valor de confiança consistente em todas as fotos de um evento

v4.2.4 (02/02/2026) [UI POLISH] (linhas: 0) (base v4.3.8)
    - NOVO: Spinner animado de loading durante conexão/boot das câmeras
    - NOVO: Indicadores de status descritivos (Iniciando, Conectando, Sem sinal)
    - NOVO: Logo ⊘ para câmeras desativadas na configuração
    - MELHORIA: Taxa de transferência em Mbps/MB/s com estimativa JPEG
    - MELHORIA: Tooltips informativos no cabeçalho da tabela Performance
    - NOVO: Logs coloridos (vermelho para ERROR, laranja para WARN)

v4.2.3 (02/02/2026) [NETWORK + UI] (linhas: 0) (base v4.2.2)
    - NOVO: Métricas avançadas de rede na aba Performance
    - NOVO: Bitrate, Latência, Jitter, Ping, Perda de frames por câmera
    - NOVO: Indicador de protocolo (UDP/TCP) na performance
    - NOVO: Alertas visuais (⚠) para valores fora do ideal
    - MELHORIA: Logs coloridos (vermelho para ERROR, laranja para WARN)
    - MELHORIA: Status das câmeras com indicador visual (círculo verde intenso)

v4.2.2 (18/01/2026) [PERFORMANCE] (linhas: 0) (base v4.2.1)
    - OTIMIZAÇÃO: Skip de frames YOLO (processa 1 a cada 3) - reduz carga CPU em 66%
    - OTIMIZAÇÃO: input_size padrão 320 (era 416) - inferência 2x mais rápida
    - OTIMIZAÇÃO: Watchdog aumentado de 12s para 20s (tolera rede instável)
    - NOVO: Parâmetro skip_frames configurável (padrão: 2)
    - NOVO: Parâmetro input_size configurável (320/416/608)
    - MELHORIA: UI sempre recebe frames (mesmo pulados) - visualização fluida
    - FIX: Reduz hard restarts causados por latência de rede

v4.2.1 (18/01/2026) [ESTÁVEL] (linhas: 0) (base v4.1.0)
    - NOVO: Sistema completo de dicas (tips) explicando cada item do menu de Configurações
    - NOVO: Checkbox para ativar/desativar exibição de tips (reduz poluição visual)
    - NOVO: Tooltips automáticos em cada campo quando tips estão ativados
    - NOVO: Persistência do estado do checkbox de tips em config.ini

v4.1.0 (06/01/2026) [ESTÁVEL] (linhas: 0) (base v4.0.3)
    - FIX CRÍTICO: migrado TODO o controle temporal sensível (captura/fotos/eventos/reconnect/performance/watchdog) para time.monotonic()
    - Garantia: min_capture_interval_s agora é respeitado de forma determinística (independente de ajustes no relógio do Windows)
    - Mantido: timestamps humanos (logs/nomes de arquivo) seguem datetime.now()

v4.0.3 (06/01/2026) [ESTÁVEL] (linhas: 0) (base v3.9.5)
    - Renomeada a v3.9.5 para v4.0.3 sem alterações funcionais (rollback total)
    - Mantém correções e robustez consolidadas da base v3.9.5

v4.0.2 (ABANDONADA) (linhas: 0)
    - Versão descartada (mesmo problema de tela em branco)

v4.0.1 (ABANDONADA) (linhas: 0)
    - Versão descartada (tela em branco)

v3.9.5 (06/01/2026) [ESTÁVEL] (linhas: 0) (base v3.9.3)
    - Corrigido crash na inicialização: callback de log apontava para self.ui_log_queue (inexistente)
    - Compatibilidade com Python < 3.10: removido uso de "int | None" (substituído por Optional[int])
    - Corrigida duplicação/indentação de RTSPObjectDetector.stop()
    - Corrigido hard restart: photo_callback enfileirava tupla incompleta
    - NOVO (persistente): min_capture_interval_s (padrão 1.0s) para impor intervalo mínimo entre imagens salvas
    - Log de CONFIG DETECTOR agora inclui min_capture_interval_s (min_shot_interval)

v3.9.4 (ABANDONADA) (linhas: 0)
    - Versão descartada por solicitação do usuário (não usar)

v3.9.3 (01/01/2026) (linhas: 0)
    - Base robusta RTSP + logs + performance + fotos agrupadas + watchdog

v3.9.1 (01/01/2026) (linhas: 0)
    - Log detalhado de eventos de movimento com parâmetros ativos
    - Log explícito de inicialização informando versão
    - Ajustes finos de padronização de mensagens de log
    - Consolidação final da documentação de eventos e métricas

v3.9.0 (01/01/2026) (linhas: 0)
    - Marco de estabilização arquitetural
    - EVENT_UID definitivo e consistente
    - Agrupamento visual de fotos por evento
    - Scroll vertical e horizontal na aba Fotos
    - Estratégia de evento baseada em cruzamento da linha central
    - Redução significativa de falsos positivos
    - Watchdog estável para operação contínua
================================================================================
NOTA (linhas):
    - Neste release, os campos (linhas: 0) ficam como placeholder proposital.
    - Na próxima interação, eu atualizo o changelog com a contagem REAL por versão.
================================================================================
"""

import os
import sys
import cv2
import numpy as np
import threading
import queue
import configparser
import urllib.request
import requests
import webbrowser
import json
import subprocess
from datetime import datetime
from pathlib import Path
import time
import platform
from typing import Optional, Callable, Any, Dict, List, Tuple

try:
    import psutil  # type: ignore
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk, ImageDraw

def set_ffmpeg_capture_options(transport: str = "udp") -> None:
    mode = (transport or "udp").strip().lower()
    if mode not in ("udp", "tcp"):
        mode = "udp"
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
        f"rtsp_transport;{mode}|"
        "stimeout;8000000|"
        "rw_timeout;8000000|"
        "max_delay;300000|"
        "fflags;nobuffer|"
        "flags;low_delay|"
        "reorder_queue_size;0"
    )

set_ffmpeg_capture_options("udp")

APP_VERSION = "4.5.9"
MAX_THUMBS = 200


def get_commit_code() -> str:
    """Retorna hash curto do commit atual; fora do git retorna N/A."""
    try:
        repo_dir = Path(__file__).resolve().parent
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo_dir),
            stderr=subprocess.DEVNULL,
            timeout=2,
            text=True,
        )
        commit = (out or "").strip()
        return commit if commit else "N/A"
    except Exception:
        return "N/A"

# ----------------------------- Tips do Menu de Configurações -----------------------------
CONFIGURATION_TIPS = {
    "cam_enabled": "Ative/desative câmeras individuais sem precisar editar a URL RTSP",
    "cam_rtsp": "URL RTSP da câmera (ex: rtsp://user:pass@192.168.1.100:554/stream)",
    "cooldown": "Tempo mínimo (em segundos) entre alertas consecutivos da mesma câmera",
    "confidence": "Confiança mínima para aceitar uma detecção (0.2 = sensível, 0.95 = rigoroso)",
    "nms": "Supressão de não-máxima: quanto menor, mais detecções (0.2 = muitas, 0.95 = poucas)",
    "photos": "Quantidade de fotos capturadas por evento de detecção",
    "min_capture": "Intervalo mínimo (segundos) entre cada foto capturada em um evento",
    "max_photos": "Número máximo de fotos (geral + crop) mantidas no diretório. Fotos mais antigas são excluídas automaticamente.",
    "person": "Disparar alerta quando pessoa é detectada",
    "car": "Disparar alerta quando carro é detectado",
    "bus": "Disparar alerta quando ônibus é detectado",
    "truck": "Disparar alerta quando caminhão é detectado",
    "motorcycle": "Disparar alerta quando motocicleta é detectada",
    "bicycle": "Disparar alerta quando bicicleta é detectada",
    "dog": "Disparar alerta quando cachorro é detectado",
    "cat": "Disparar alerta quando gato é detectado",
    "bird": "Disparar alerta quando pássaro é detectado",
    "horse": "Disparar alerta quando cavalo é detectado",
    "bot_token": "Token do bot Telegram (obtenha com @BotFather)",
    "chat_id": "ID do chat/grupo Telegram para receber notificações",
    "alert_mode": "Tipo de alerta: 'all' = eventos de sistema + fotos, 'detections' = somente fotos, 'none' = desativado",
    "rtsp_transport": "Transporte RTSP: 'udp' (padrão, menor latência) ou 'tcp' (mais estável em redes instáveis)",
}


# ----------------------------- Log -----------------------------
class LogManager:
    """Gerenciador de logs padronizado conforme ESPECIFICAÇÃO_LOGS.md
    
    Referência: https://github.com/Espaco-CMaker/Guia_de_Padroes/blob/main/ESPECIFICACAO_LOGS.md
    
    Características:
    - Formato: "%(asctime)s | %(levelname)-7s | %(name)-15s | %(message)s"
    - Rotação automática (5MB por arquivo, 10 backups)
    - Buffer de eventos para Telegram (reduz spam)
    - Thread-safe
    """
    def __init__(self, log_file: str = "log.txt", max_size_mb: int = 5):
        self.log_file = Path(log_file)
        self.max_size = max_size_mb * 1024 * 1024
        self.callbacks: List[Callable[[str], None]] = []
        self._lock = threading.Lock()
        self.telegram = None
        self._sending_telegram = False
        
        # Buffer para eventos de sistema (reduzir mensagens Telegram)
        self._system_events_buffer = []
        self._system_events_lock = threading.Lock()
        self._last_buffer_send_time = time.time()
        self._buffer_send_interval = 30.0  # Enviar a cada 30 segundos
        self._buffer_max_events = 10  # Ou quando atingir 10 eventos

    def add_callback(self, cb: Callable[[str], None]) -> None:
        self.callbacks.append(cb)

    def set_telegram(self, telegram) -> None:
        self.telegram = telegram
    
    def _add_system_event_to_buffer(self, level: str, msg: str, cam: Optional[int], timestamp: str) -> None:
        """Adiciona evento de sistema ao buffer para envio agrupado."""
        with self._system_events_lock:
            if "watchdog" in (msg or "").lower():
                return
            # Emoji de nível baseado no tipo de alerta
            if "RTSP" in msg.upper() or "CONEXÃO" in msg.upper() or "DESCONECT" in msg.upper():
                level_emoji = "🔴"  # Vermelho para problemas críticos
            elif "reconnect" in msg.lower() or "watchdog" in msg.lower():
                level_emoji = "🟠"  # Laranja para warnings
            else:
                level_emoji = "🟡"  # Amarelo para informações críticas
            
            cam_text = f"CAM{cam}" if cam is not None else "SYS"
            event_entry = {
                "emoji": level_emoji,
                "cam": cam_text,
                "timestamp": timestamp.split()[1],  # Apenas HH:MM:SS
                "msg": msg[:80]  # Limitar tamanho da mensagem
            }
            self._system_events_buffer.append(event_entry)
            
            # Enviar se atingir o limite de eventos
            if len(self._system_events_buffer) >= self._buffer_max_events:
                self._flush_system_events_buffer()
    
    def _flush_system_events_buffer(self) -> None:
        """Envia todos os eventos acumulados no buffer em uma única mensagem."""
        if not self._system_events_buffer:
            return
        
        if self._sending_telegram:
            return
        
        try:
            self._sending_telegram = True
            
            # Construir mensagem consolidada
            event_count = len(self._system_events_buffer)
            events_text = "\n".join(
                f"{ev['emoji']} {ev['timestamp']} [{ev['cam']}] {ev['msg']}"
                for ev in self._system_events_buffer
            )
            
            caption = (
                f"⚠️ EVENTOS DE SISTEMA ({event_count})\n"
                f"{'━' * 8}\n"
                f"{events_text}\n"
                f"{'━' * 8}\n"
                f"v{APP_VERSION}"
            )
            
            self.telegram.enviar_mensagem(caption)
            self._system_events_buffer.clear()
            self._last_buffer_send_time = time.time()
        except Exception:
            pass
        finally:
            self._sending_telegram = False
    
    def check_and_flush_buffer(self) -> None:
        """Verifica se deve enviar buffer baseado no tempo."""
        with self._system_events_lock:
            if not self._system_events_buffer:
                return
            
            elapsed = time.time() - self._last_buffer_send_time
            if elapsed >= self._buffer_send_interval:
                self._flush_system_events_buffer()

    def _is_critical_connection_issue(self, level: str, msg: str) -> bool:
        if level not in ("WARN", "ERROR"):
            return False
        text = (msg or "").lower()
        if "watchdog" in text:
            return False
        patterns = [
            "falha rtsp",
            "sem frame",
            "sem sinal",
            "desconect",
            "rtsp vazio",
            "hard restart",
            "soft reconnect",
            "falha ao recriar câmera",
            "erro ao conectar",
        ]
        return any(p in text for p in patterns)

    def _rotate_if_needed(self) -> None:
        if not self.log_file.exists():
            return
        if self.log_file.stat().st_size > self.max_size:
            backup = self.log_file.with_suffix(".bak")
            try:
                if backup.exists():
                    backup.unlink()
            except Exception:
                pass
            try:
                self.log_file.rename(backup)
            except Exception:
                pass

    def log(self, level: str, msg: str, cam: Optional[int] = None) -> None:
        """Gera entrada de log no formato padronizado.
        
        Formato: "YYYY-MM-DD HH:MM:SS | LEVEL | name | message"
        Exemplo: "2026-02-04 14:30:45 | INFO    | camera.cam1     | Frame captured"
        """
        original_level = level
        is_critical = self._is_critical_connection_issue(level, msg)
        if is_critical and level == "WARN":
            level = "ERROR"
        
        # Timestamp no formato padronizado
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Nome do logger hierarquizado
        if cam is not None:
            logger_name = f"camera.cam{cam}"
        else:
            logger_name = "system"
        
        # Formatação padronizada: timestamp | level | name | message
        # Padding: level=7 chars, name=15 chars (alinhamento conforme guia)
        line = f"{ts} | {level:<7} | {logger_name:<15} | {msg}\n"

        with self._lock:
            self._rotate_if_needed()
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(line)
            except Exception:
                pass

        for cb in self.callbacks:
            try:
                cb(line)
            except Exception:
                pass

        # Adicionar evento crítico ao buffer ao invés de enviar imediatamente
        if is_critical and level == "ERROR" and original_level != "WARN" and self.telegram and getattr(self.telegram, "enabled", False):
            if "Erro ao enviar mensagem Telegram" not in msg:
                self._add_system_event_to_buffer(level, msg, cam, ts)


# ----------------------------- Telegram -----------------------------
class TelegramBot:
    def __init__(self, token: str, chat_id: str, log: Optional[LogManager] = None):
        self.token = (token or "").strip()
        self.chat_id = (chat_id or "").strip()
        self.enabled = bool(self.token and self.chat_id)
        self.base_url = f"https://api.telegram.org/bot{self.token}" if self.enabled else ""
        self.log = log

    def enviar_mensagem(self, texto: str) -> bool:
        if not self.enabled:
            return False
        try:
            url = f"{self.base_url}/sendMessage"
            data = {"chat_id": self.chat_id, "text": texto}
            r = requests.post(url, data=data, timeout=10)
            if r.status_code == 200:
                return True
            else:
                # ERROR: resposta HTTP não-200
                if self.log:
                    self.log.log("ERROR", 
                        f"Telegram sendMessage FALHOU | "
                        f"HTTP {r.status_code} | "
                        f"Resposta: {r.text[:200]} | "
                        f"URL: {url} | "
                        f"ChatID: {self.chat_id}")
                return False
        except requests.exceptions.Timeout as e:
            if self.log:
                self.log.log("ERROR", 
                    f"Telegram sendMessage TIMEOUT | "
                    f"Erro: {str(e)} | "
                    f"URL: {url} | "
                    f"ChatID: {self.chat_id}")
            return False
        except requests.exceptions.ConnectionError as e:
            if self.log:
                self.log.log("ERROR", 
                    f"Telegram sendMessage CONEXÃO FALHOU | "
                    f"Erro: {str(e)} | "
                    f"URL: {url} | "
                    f"ChatID: {self.chat_id}")
            return False
        except Exception as e:
            if self.log:
                self.log.log("ERROR", 
                    f"Telegram sendMessage EXCEÇÃO | "
                    f"Tipo: {type(e).__name__} | "
                    f"Erro: {str(e)} | "
                    f"URL: {url} | "
                    f"ChatID: {self.chat_id}")
            return False

    def enviar_foto(self, foto_path: str, caption: str = "") -> bool:
        if not self.enabled:
            return False
        try:
            url = f"{self.base_url}/sendPhoto"
            with open(foto_path, "rb") as photo:
                files = {"photo": photo}
                data = {"chat_id": self.chat_id, "caption": caption}
                r = requests.post(url, files=files, data=data, timeout=30)
            if r.status_code == 200:
                return True
            else:
                # ERROR: resposta HTTP não-200
                if self.log:
                    self.log.log("ERROR", 
                        f"Telegram sendPhoto FALHOU | "
                        f"HTTP {r.status_code} | "
                        f"Resposta: {r.text[:200]} | "
                        f"Arquivo: {foto_path} | "
                        f"Tamanho: {Path(foto_path).stat().st_size / 1024:.1f}KB | "
                        f"URL: {url} | "
                        f"ChatID: {self.chat_id}")
                return False
        except FileNotFoundError as e:
            if self.log:
                self.log.log("ERROR", 
                    f"Telegram sendPhoto ARQUIVO NÃO ENCONTRADO | "
                    f"Erro: {str(e)} | "
                    f"Arquivo: {foto_path}")
            return False
        except requests.exceptions.Timeout as e:
            if self.log:
                self.log.log("ERROR", 
                    f"Telegram sendPhoto TIMEOUT | "
                    f"Erro: {str(e)} | "
                    f"Arquivo: {foto_path} | "
                    f"URL: {url} | "
                    f"ChatID: {self.chat_id}")
            return False
        except requests.exceptions.ConnectionError as e:
            if self.log:
                self.log.log("ERROR", 
                    f"Telegram sendPhoto CONEXÃO FALHOU | "
                    f"Erro: {str(e)} | "
                    f"Arquivo: {foto_path} | "
                    f"URL: {url} | "
                    f"ChatID: {self.chat_id}")
            return False
        except Exception as e:
            if self.log:
                self.log.log("ERROR", 
                    f"Telegram sendPhoto EXCEÇÃO | "
                    f"Tipo: {type(e).__name__} | "
                    f"Erro: {str(e)} | "
                    f"Arquivo: {foto_path} | "
                    f"URL: {url} | "
                    f"ChatID: {self.chat_id}")
            return False

    def enviar_grupo_fotos(self, fotos: List[str], caption: str = "") -> bool:
        if not self.enabled:
            return False
        if not fotos:
            return False
        files = {}
        try:
            url = f"{self.base_url}/sendMediaGroup"
            media = []
            for i, foto_path in enumerate(fotos):
                attach_name = f"file{i}"
                files[attach_name] = open(foto_path, "rb")
                item = {"type": "photo", "media": f"attach://{attach_name}"}
                if i == 0 and caption:
                    item["caption"] = caption
                media.append(item)

            data = {
                "chat_id": self.chat_id,
                "media": json.dumps(media, ensure_ascii=False)
            }
            r = requests.post(url, files=files, data=data, timeout=30)
            if r.status_code == 200:
                return True
            else:
                if self.log:
                    self.log.log("ERROR",
                        f"Telegram sendMediaGroup FALHOU | "
                        f"HTTP {r.status_code} | "
                        f"Resposta: {r.text[:200]} | "
                        f"Qtd: {len(fotos)} | "
                        f"URL: {url} | "
                        f"ChatID: {self.chat_id}")
                return False
        except FileNotFoundError as e:
            if self.log:
                self.log.log("ERROR",
                    f"Telegram sendMediaGroup ARQUIVO NÃO ENCONTRADO | "
                    f"Erro: {str(e)}")
            return False
        except requests.exceptions.Timeout as e:
            if self.log:
                self.log.log("ERROR",
                    f"Telegram sendMediaGroup TIMEOUT | "
                    f"Erro: {str(e)} | "
                    f"URL: {url} | "
                    f"ChatID: {self.chat_id}")
            return False
        except requests.exceptions.ConnectionError as e:
            if self.log:
                self.log.log("ERROR",
                    f"Telegram sendMediaGroup CONEXÃO FALHOU | "
                    f"Erro: {str(e)} | "
                    f"URL: {url} | "
                    f"ChatID: {self.chat_id}")
            return False
        except Exception as e:
            if self.log:
                self.log.log("ERROR",
                    f"Telegram sendMediaGroup EXCEÇÃO | "
                    f"Tipo: {type(e).__name__} | "
                    f"Erro: {str(e)} | "
                    f"URL: {url} | "
                    f"ChatID: {self.chat_id}")
            return False
        finally:
            for f in files.values():
                try:
                    f.close()
                except Exception:
                    pass

    def formatar_msg_inicio(self, cameras_ativas: int, versao: str, commit: str = "N/A") -> str:
        """Formata mensagem amigável de início do sistema."""
        return (
            f"✅ SISTEMA INICIADO\n"
            f"{'━' * 8}\n"
            f"🎥 Câmeras ativas: {cameras_ativas}\n"
            f"🚀 Status: Monitorando\n"
            f"v{versao}\n"
            f"commit {commit}\n"
            f"{'━' * 8}"
        )

    def formatar_msg_encerramento(self, total_deteccoes: int, versao: str) -> str:
        """Formata mensagem amigável de encerramento do sistema."""
        return (
            f"⏹️ SISTEMA ENCERRADO\n"
            f"{'━' * 8}\n"
            f"👤 Detecções registradas: {total_deteccoes}\n"
            f"✓ Monitoramento finalizado\n"
            f"v{versao}\n"
            f"{'━' * 8}"
        )


# ----------------------------- Detector (1 câmera) -----------------------------
class RTSPObjectDetector:
    """
    Detector para 1 câmera.
    - Envia frames para UI via frame_callback(cam_id, frame_bgr)
    - Envia fotos para UI via photo_callback(cam_id, foto_path, timestamp_str, event_uid, shot_idx)
    - Evento/alerta/foto: somente se "person" detectada
    - Watchdog usa soft reconnect via request_soft_reconnect()

    v4.1.0:
    - Todo o controle temporal crítico usa time.monotonic() (captura/evento/reconnect/performance).
    - datetime.now() fica apenas para carimbo humano (log/arquivo).
    """

    def __init__(self, cam_id: int, rtsp_url: str, log: LogManager, telegram: TelegramBot,
                 models_dir: str = "models", foto_dir: str = "fotos"):
        self.cam_id = cam_id
        self.rtsp_url = (rtsp_url or "").strip()
        self.log = log
        self.telegram = telegram

        self.models_dir = Path(models_dir)
        self.foto_dir = Path(foto_dir)
        self.models_dir.mkdir(exist_ok=True)
        self.foto_dir.mkdir(exist_ok=True)

        self.running = False
        self.cap = None

        self.net = None
        self.output_layers = None
        self.classes = None

        self.frame_callback = None
        self.photo_callback = None

        self.inf_times: List[float] = []

        # Config runtime
        self.cooldown_s = 2.0
        self.conf_th = 0.5
        self.nms_th = 0.4
        self.input_size = 416
        self.telegram_mode = "detections"  # all | detections | none
        self.photos_per_event = 2
        self.max_photos_keep = 500  # Número máximo de fotos a manter
        
        # OTIMIZAÇÃO: Skip frames para reduzir carga de processamento
        # skip_frames=2 significa processar 1 frame a cada 3 (pula 2)
        self.skip_frames = 2  # Padrão: processa 1 a cada 3 frames

        # Intervalo mínimo global entre capturas (persistente via config)
        self.min_capture_interval_s = 1.0

        # Contadores / estado
        self.detections_total = 0
        self._frame_skip_counter = 0  # Contador para skip de frames

        # Watchdog: usamos monotonic como referência estável
        self.last_frame_mono = 0.0       # controle (monotonic)
        self.last_frame_wall_ts = 0.0    # apenas informativo (time.time)

        # Evento por pessoa (monotonic)
        self._last_event_time = 0.0
        self._pending_shots = 0
        self._event_uid = ""
        self._event_conf_avg = 0.0  # Confiança média do evento (fixada na detecção inicial)
        self.presence_exit_timeout_s = 3.0
        self.presence_mid_alert_after_s = 20.0
        self.presence_min_move_px = 25.0
        self._presence_active = False
        self._presence_mid_sent = False
        self._presence_start_mono = 0.0
        self._presence_last_seen_mono = 0.0
        self._presence_enter_center = None
        self._presence_last_frame_draw = None
        self._presence_last_frame_clean = None
        self._presence_last_boxes = []

        # Capturas por evento (monotonic)
        self._last_shot_time = 0.0
        self._min_shot_interval = 0.7  # segundos entre fotos do mesmo evento

        # Controle global de captura (monotonic)
        self._last_capture_time_global = 0.0

        # Classes habilitadas (evento só dispara se person estiver presente)
        self.classes_enabled = {0}  # person

        # Soft reconnect trigger (watchdog)
        self.reconnect_event = threading.Event()
        self._last_soft_reconnect_mono = 0.0
        self._pending_reconnect_reason = "watchdog"

        # Robustez RTSP (monotonic)
        self._bad_reads = 0
        self._last_reconnect_try_mono = 0.0
        self._reconnect_backoff_s = 5.0  # Aumentado: esperar 5s antes de tentar reconectar
        self._max_backoff_s = 30.0  # Aumentado: máximo de 30s entre tentativas

        # Throttle de logs (monotonic)
        self._last_nonperson_log_mono = 0.0

        self._init_yolo()

        # Status da câmera
        self.status = "offline"  # offline | online | receiving | frozen
        self.last_frame_timestamp = 0.0

    def _log_detector_config(self) -> None:
        return

    def _safe_read(self):
        """
        Leitura robusta: cap.read() pode explodir com cv2.error.
        Retorna (ret, frame, err_str).
        """
        try:
            ret, frame = self.cap.read()
            return ret, frame, None
        except cv2.error as e:
            return False, None, f"cv2.error: {e}"
        except Exception as e:
            return False, None, f"Exception: {e}"

    def _download_if_missing(self, url: str, dst: Path, label: str) -> None:
        if dst.exists():
            return
        self.log.log("INFO", f"Baixando {label}...", self.cam_id)
        urllib.request.urlretrieve(url, dst)
        self.log.log("INFO", f"{label} OK.", self.cam_id)

    def _init_yolo(self) -> None:
        try:
            self.log.log("INFO", "Initializing YOLO detector...", self.cam_id)

            weights_path = self.models_dir / "yolov4-tiny.weights"
            config_path = self.models_dir / "yolov4-tiny.cfg"
            names_path = self.models_dir / "coco.names"

            weights_url = "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights"
            config_url = "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg"
            names_url = "https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names"

            self._download_if_missing(weights_url, weights_path, "yolov4-tiny.weights")
            self._download_if_missing(config_url, config_path, "yolov4-tiny.cfg")
            self._download_if_missing(names_url, names_path, "coco.names")

            with open(names_path, "r", encoding="utf-8") as f:
                self.classes = [line.strip() for line in f.readlines()]

            self.net = cv2.dnn.readNetFromDarknet(str(config_path), str(weights_path))

            if cv2.cuda.getCudaEnabledDeviceCount() > 0:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                self.log.log("INFO", "CUDA backend enabled", self.cam_id)
            else:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                self.log.log("INFO", "CPU backend enabled", self.cam_id)

            layer_names = self.net.getLayerNames()
            unconnected = self.net.getUnconnectedOutLayers()
            unconnected = unconnected.flatten() if hasattr(unconnected, "flatten") else unconnected
            self.output_layers = [layer_names[i - 1] for i in unconnected]

            self.log.log("INFO", "YOLO detector initialized successfully", self.cam_id)
        except Exception as e:
            self.log.log("ERROR", f"Falha ao inicializar YOLO: {e}", self.cam_id)
            raise

    def _connect(self) -> bool:
        try:
            self.log.log("INFO", "Connecting to RTSP stream...", self.cam_id)

            try:
                if self.cap is not None:
                    self.cap.release()
            except Exception as e:
                self.log.log("WARN", f"Erro ao liberar cap antigo: {e}", self.cam_id)

            cap = cv2.VideoCapture()

            try:
                cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 10000)  # 10s timeout para abrir
                cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 10000)  # 10s timeout para ler (evita falhas por timeout curto)
            except Exception:
                pass

            try:
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            except Exception:
                pass

            ok = cap.open(self.rtsp_url, cv2.CAP_FFMPEG)
            if not ok or (not cap.isOpened()):
                raise Exception("Não abriu stream RTSP")

            # Limpar buffer após reconectar (descartar frames antigos/corrompidos)
            try:
                for _ in range(10):
                    ret, _ = cap.read()
                    if not ret:
                        break
            except Exception:
                pass

            self.cap = cap
            self.log.log("INFO", "RTSP stream connected successfully", self.cam_id)
            self.status = "online"
            return True

        except Exception as e:
            self.log.log("WARN", f"Falha RTSP: {e}", self.cam_id)
            self.status = "offline"
            return False

    def _detect(self, frame_bgr):
        start_inf = time.monotonic()
        h, w = frame_bgr.shape[:2]
        blob = cv2.dnn.blobFromImage(
            frame_bgr, 1 / 255.0, (self.input_size, self.input_size),
            swapRB=True, crop=False
        )
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        boxes, confs, cids = [], [], []
        for out in outs:
            for det in out:
                scores = det[5:]
                cid = int(np.argmax(scores))
                conf = float(scores[cid])
                if cid in self.classes_enabled and conf >= self.conf_th:
                    cx = int(det[0] * w)
                    cy = int(det[1] * h)
                    bw = int(det[2] * w)
                    bh = int(det[3] * h)
                    x = int(cx - bw / 2)
                    y = int(cy - bh / 2)
                    boxes.append([x, y, bw, bh])
                    confs.append(conf)
                    cids.append(cid)

        idxs = cv2.dnn.NMSBoxes(boxes, confs, self.conf_th, self.nms_th)
        f_boxes, f_confs, f_cids = [], [], []
        if len(idxs) > 0:
            for i in idxs.flatten():
                # Validação adicional: garantir que a confiança está acima do threshold
                # (NMSBoxes remove overlaps, não filtra por threshold)
                if confs[i] >= self.conf_th:
                    f_boxes.append(boxes[i])
                    f_confs.append(confs[i])
                    f_cids.append(cids[i])

        inf_time = time.monotonic() - start_inf
        return f_boxes, f_confs, f_cids, inf_time

    def _draw_boxes(self, frame_bgr, boxes, confs, cids):
        out = frame_bgr.copy()
        for i, (x, y, bw, bh) in enumerate(boxes):
            cid = cids[i]
            conf = confs[i]
            name = self.classes[cid] if self.classes and cid < len(self.classes) else str(cid)
            cv2.rectangle(out, (x, y), (x + bw, y + bh), (0, 255, 255), 2)
            cv2.putText(out, f"{name.upper()} {conf:.0%}", (x, max(20, y - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
        return out

    def _person_present(self, cids) -> bool:
        return 0 in cids  # COCO: person=0

    def _largest_person_box(self, boxes, cids):
        person_boxes = [b for i, b in enumerate(boxes) if i < len(cids) and cids[i] == 0]
        if not person_boxes:
            return None
        return max(person_boxes, key=lambda b: b[2] * b[3])

    def _box_center(self, box):
        x, y, w, h = box
        return (x + (w / 2.0), y + (h / 2.0))

    def _distance_px(self, p1, p2) -> float:
        if (p1 is None) or (p2 is None):
            return 0.0
        dx = float(p1[0]) - float(p2[0])
        dy = float(p1[1]) - float(p2[1])
        return float((dx * dx + dy * dy) ** 0.5)

    def _extract_object_crop(self, frame_bgr, boxes, margin_percent=15):
        """Extrai crop do maior objeto detectado com margem de 15%."""
        if not boxes:
            return None
        
        # Pegar a maior caixa (área)
        largest_box = max(boxes, key=lambda b: b[2] * b[3])
        x, y, w, h = largest_box
        
        # Adicionar margem de 15%
        margin_w = int(w * margin_percent / 100)
        margin_h = int(h * margin_percent / 100)
        
        # Calcular novas coordenadas com margem
        x1 = max(0, x - margin_w)
        y1 = max(0, y - margin_h)
        x2 = min(frame_bgr.shape[1], x + w + margin_w)
        y2 = min(frame_bgr.shape[0], y + h + margin_h)
        
        # Extrair crop
        crop = frame_bgr[y1:y2, x1:x2]
        return crop if crop.size > 0 else None

    def _cleanup_old_photos(self):
        """Remove fotos antigas mantendo apenas as últimas max_photos_keep."""
        try:
            # Listar todas as fotos no diretório (incluindo crops)
            all_photos = sorted(self.foto_dir.glob("*.jpg"), key=lambda p: p.stat().st_mtime, reverse=True)
            
            if len(all_photos) <= self.max_photos_keep:
                return  # Não precisa limpar
            
            # Remover fotos mais antigas
            photos_to_remove = all_photos[self.max_photos_keep:]
            removed_count = 0
            
            for photo in photos_to_remove:
                try:
                    photo.unlink()
                    removed_count += 1
                except Exception as e:
                    self.log.log("WARN", f"Erro ao remover foto antiga {photo.name}: {e}", self.cam_id)
            
            if removed_count > 0:
                self.log.log("INFO", 
                    f"Limpeza automática | Removidas {removed_count} fotos antigas | "
                    f"Mantidas {len(all_photos) - removed_count}/{self.max_photos_keep} | "
                    f"v{APP_VERSION}", self.cam_id)
        
        except Exception as e:
            self.log.log("ERROR", 
                f"Erro na limpeza automática de fotos | "
                f"Tipo: {type(e).__name__} | "
                f"Erro: {str(e)}", self.cam_id)

    def _save_and_notify(self, frame_bgr_with_boxes, frame_bgr_clean, boxes, event_uid: str, shot_idx: int, person_count: int, conf_avg: float, detected_classes=None, alert_stage: str = "DETECÇÃO"):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_uid = (event_uid or "evt").replace(":", "-").replace("/", "-")
        filename = f"{ts}_CAM{self.cam_id}_EVT{safe_uid}_S{shot_idx}.jpg"
        filename_crop = f"{ts}_CAM{self.cam_id}_EVT{safe_uid}_S{shot_idx}_crop.jpg"

        # Limpar fotos antigas se necessário (manter apenas max_photos_keep)
        self._cleanup_old_photos()

        # Salvar foto geral (com boxes)
        path = self.foto_dir / filename
        cv2.imwrite(str(path), frame_bgr_with_boxes)
        
        # Extrair e salvar crop do objeto detectado
        path_crop = self.foto_dir / filename_crop
        crop = self._extract_object_crop(frame_bgr_clean, boxes)
        if crop is not None:
            cv2.imwrite(str(path_crop), crop)

        self.log.log(
            "INFO",
            "SHOT | "
            f"evt={event_uid} | shot={shot_idx}/{self.photos_per_event} | "
            f"pessoas={person_count} | conf_avg={conf_avg:.2f} | "
            f"arquivo={filename} | crop={filename_crop if crop is not None else 'N/A'} | v{APP_VERSION}",
            self.cam_id
        )

        if self.photo_callback:
            try:
                crop_path = str(path_crop) if crop is not None else None
                self.photo_callback(self.cam_id, str(path), ts, event_uid, shot_idx, crop_path)
            except Exception as e:
                self.log.log("ERROR", f"Erro no callback de foto: {e}", self.cam_id)

        if self.telegram_mode in ("all", "detections") and self.telegram.enabled:
            timestamp_formatted = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            conf_pct = (conf_avg * 100) if conf_avg > 0 else 0
            
            # Determinar texto da detecção
            if detected_classes:
                detection_text = ", ".join(detected_classes)
            else:
                detection_text = "pessoa"
            
            # Emoji de status baseado em confiança
            if conf_pct >= 70:
                confidence_emoji = "🟢"  # Verde - alta confiança
            elif conf_pct >= 50:
                confidence_emoji = "🟡"  # Amarelo - média confiança
            else:
                confidence_emoji = "🟠"  # Laranja - baixa confiança
            
            # Construir caption formatado (com cores via emojis)
            caption = (
                f"🟢 ALERTA {alert_stage}\n"
                f"{'━' * 8}\n"
                f"📹 Câmera {self.cam_id}\n"
                f"⏰ {timestamp_formatted}\n"
                f"🔍 Detectado: {detection_text}\n"
                f"{confidence_emoji} Confiança: {conf_pct:.1f}%\n"
                f"v{APP_VERSION}"
            )
            
            # Enviar fotos em grupo (geral + crop, se disponível)
            if crop is not None:
                # Enviar ambas as fotos na mesma mensagem (geral primeiro, crop depois)
                fotos_para_enviar = [str(path), str(path_crop)]
                ok = self.telegram.enviar_grupo_fotos(fotos_para_enviar, caption)
                if ok:
                    self.log.log("INFO", "Photos sent to Telegram (general + crop in group)", self.cam_id)
                else:
                    self.log.log("ERROR", "Falha ao enviar grupo de fotos Telegram.", self.cam_id)
            else:
                # Se não há crop, enviar apenas foto geral
                ok = self.telegram.enviar_foto(str(path), caption)
                if ok:
                    self.log.log("INFO", "General photo sent to Telegram", self.cam_id)
                else:
                    self.log.log("ERROR", "Falha ao enviar foto geral Telegram.", self.cam_id)

    # -------- Soft reconnect (watchdog) --------
    def request_soft_reconnect(self, reason: str = "watchdog"):
        self._pending_reconnect_reason = reason
        self.reconnect_event.set()

    def _soft_reconnect_now(self, reason: str) -> bool:
        now_mono = time.monotonic()
        if (now_mono - float(self._last_soft_reconnect_mono or 0.0)) < 5.0:
            return False

        self._last_soft_reconnect_mono = now_mono
        self.log.log("WARN", f"Soft reconnect solicitado ({reason}).", self.cam_id)

        try:
            if self.cap is not None:
                self.cap.release()
        except Exception as e:
            self.log.log("WARN", f"Erro ao liberar cap durante soft reconnect: {e}", self.cam_id)

        ok = self._connect()
        if ok:
            self._pending_shots = 0
            self._last_shot_time = 0.0
            self._last_event_time = 0.0
            self._presence_active = False
            self._presence_mid_sent = False
            self._presence_last_seen_mono = 0.0
            self._presence_enter_center = None
            self._presence_last_frame_draw = None
            self._presence_last_frame_clean = None
            self._presence_last_boxes = []
            self.last_frame_mono = 0.0
            self.last_frame_wall_ts = 0.0
            self.log.log("INFO", "Soft reconnect completed successfully", self.cam_id)
            return True

        self.log.log("ERROR", "Soft reconnect falhou.", self.cam_id)
        return False

    def stop(self) -> None:
        self.running = False

    def run(self):
        self.running = True
        try:
            while self.running and (not self._connect()):
                self.log.log("WARN", "Não conectou RTSP. Tentando novamente em 2s...", self.cam_id)
                time.sleep(2.0)

            self._log_detector_config()

            self.last_frame_timestamp = time.time()

            while self.running:
                if self.reconnect_event.is_set():
                    self.reconnect_event.clear()
                    reason = getattr(self, "_pending_reconnect_reason", "watchdog")
                    self._soft_reconnect_now(reason)

                ret, frame, err = self._safe_read()
                if err:
                    self.log.log("WARN", f"Falha em cap.read() ({err}). Tentando recuperar...", self.cam_id)

                if (not ret) or (frame is None) or (not hasattr(frame, "size")) or (frame.size == 0):
                    self._bad_reads += 1

                    if self._bad_reads in (1, 5, 15) or (self._bad_reads % 30 == 0):
                        self.log.log("WARN", f"Frame falhou ({self._bad_reads}). Tentando recuperar...", self.cam_id)

                    now_mono = time.monotonic()
                    if (now_mono - self._last_reconnect_try_mono) >= self._reconnect_backoff_s:
                        self._last_reconnect_try_mono = now_mono
                        try:
                            if self.cap is not None:
                                self.cap.release()
                        except Exception as e:
                            self.log.log("WARN", f"Erro ao liberar cap durante reconnect: {e}", self.cam_id)

                        ok = self._connect()
                        if ok:
                            self.log.log("INFO", "Reconnected after frame read failure", self.cam_id)
                            self._bad_reads = 0
                            self._reconnect_backoff_s = 5.0  # Reset para 5s
                        else:
                            self._reconnect_backoff_s = min(self._max_backoff_s, self._reconnect_backoff_s * 1.5)

                    time.sleep(0.05)
                    continue

                # frame OK
                self._bad_reads = 0
                self._reconnect_backoff_s = 5.0  # Reset para 5s

                now_mono = time.monotonic()
                now_wall = time.time()
                self.last_frame_mono = now_mono
                self.last_frame_wall_ts = now_wall
                self.last_frame_timestamp = now_wall
                if self.status == "online":
                    self.status = "receiving"

                # OTIMIZAÇÃO: Skip de processamento YOLO (reduz carga em 66% com skip=2)
                # Frame RAW é sempre enviado para UI, mas YOLO só processa 1 a cada (skip+1) frames
                self._frame_skip_counter += 1
                if self._frame_skip_counter <= self.skip_frames:
                    # Envia frame sem processamento para UI (visualização fluida)
                    if self.frame_callback:
                        try:
                            self.frame_callback(self.cam_id, frame)
                        except Exception as e:
                            self.log.log("ERROR", f"Erro no callback de frame: {e}", self.cam_id)
                    continue  # Pula processamento YOLO
                
                self._frame_skip_counter = 0  # Reset contador

                if frame.std() < 5.0:
                    continue

                boxes, confs, cids, inf_time = self._detect(frame)
                self.inf_times.append(inf_time)
                frame_draw = self._draw_boxes(frame, boxes, confs, cids)

                person_present = bool(boxes and self._person_present(cids))
                if person_present:
                    self._presence_last_seen_mono = now_mono
                    self._presence_last_frame_draw = frame_draw.copy()
                    self._presence_last_frame_clean = frame.copy()
                    self._presence_last_boxes = [list(b) for b in boxes]

                    largest_person = self._largest_person_box(boxes, cids)
                    person_center = self._box_center(largest_person) if largest_person is not None else None

                    if not self._presence_active and (now_mono - self._last_event_time) >= self.cooldown_s:
                        evt_ts = int(time.time())
                        self._event_uid = f"{self.cam_id}-{evt_ts}-{self.detections_total + 1}"
                        self._event_conf_avg = (sum(confs) / len(confs)) if confs else 0.0
                        self._presence_active = True
                        self._presence_mid_sent = False
                        self._presence_start_mono = now_mono
                        self._presence_enter_center = person_center
                        self._last_event_time = now_mono
                        self.detections_total += 1

                        person_count = sum(1 for cid in cids if cid == 0)
                        detected_class_names = []
                        for cid in set(cids):
                            if self.classes and cid < len(self.classes):
                                detected_class_names.append(self.classes[cid])
                        self._save_and_notify(
                            frame_draw, frame, boxes, self._event_uid, 1, person_count, self._event_conf_avg,
                            detected_class_names, alert_stage="ENTRADA"
                        )
                        self.log.log("INFO", f"EVENTO ENTRADA | evt={self._event_uid} | v{APP_VERSION}", self.cam_id)

                    if self._presence_active and (not self._presence_mid_sent):
                        elapsed = now_mono - self._presence_start_mono
                        move_px = self._distance_px(person_center, self._presence_enter_center)
                        if elapsed >= self.presence_mid_alert_after_s and move_px <= self.presence_min_move_px:
                            person_count = sum(1 for cid in cids if cid == 0)
                            detected_class_names = []
                            for cid in set(cids):
                                if self.classes and cid < len(self.classes):
                                    detected_class_names.append(self.classes[cid])
                            self._save_and_notify(
                                frame_draw, frame, boxes, self._event_uid, 2, person_count, self._event_conf_avg,
                                detected_class_names, alert_stage="MEIO"
                            )
                            self._presence_mid_sent = True
                            self.log.log("INFO", f"EVENTO MEIO | evt={self._event_uid} | v{APP_VERSION}", self.cam_id)
                elif self._presence_active:
                    since_seen = now_mono - self._presence_last_seen_mono
                    if since_seen >= self.presence_exit_timeout_s:
                        if self._presence_last_frame_draw is not None and self._presence_last_frame_clean is not None:
                            self._save_and_notify(
                                self._presence_last_frame_draw,
                                self._presence_last_frame_clean,
                                self._presence_last_boxes,
                                self._event_uid,
                                3,
                                0,
                                self._event_conf_avg,
                                ["saida"],
                                alert_stage="SAÍDA",
                            )
                        self.log.log("INFO", f"EVENTO SAÍDA | evt={self._event_uid} | v{APP_VERSION}", self.cam_id)
                        self._presence_active = False
                        self._presence_mid_sent = False
                        self._presence_start_mono = 0.0
                        self._presence_last_seen_mono = 0.0
                        self._presence_enter_center = None
                        self._presence_last_frame_draw = None
                        self._presence_last_frame_clean = None
                        self._presence_last_boxes = []

                if self.frame_callback:
                    try:
                        self.frame_callback(self.cam_id, frame_draw)
                    except Exception as e:
                        self.log.log("ERROR", f"Erro no callback de frame: {e}", self.cam_id)

                if len(self.inf_times) > 400:
                    self.inf_times.clear()

        finally:
            try:
                if self.cap is not None:
                    self.cap.release()
            except Exception:
                pass

# ----------------------------- UI -----------------------------
class InterfaceGrafica:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"AlertaIntruso v{APP_VERSION} — 4 Câmeras RTSP (YOLO)")
        self.root.geometry("1400x850")

        self.config_file = Path("config.ini")
        self.config = configparser.ConfigParser()

        self.log = LogManager("log.txt", max_size_mb=5)  # 5MB conforme padrão do guia

        # Queues precisam existir antes do callback do log
        self.frame_queue = queue.Queue()
        self.photo_queue = queue.Queue()
        self.log_queue = queue.Queue()

        self.log.add_callback(lambda line: self.log_queue.put(line))

        # Cabeçalho de inicialização padronizado (ESPECIFICACAO_LOGS.md)
        separator = "=" * 80
        self.log.log("INFO", separator)
        self.log.log("INFO", f"Application: AlertaIntruso v{APP_VERSION}")
        self.log.log("INFO", f"Python: {platform.python_version()}")
        self.log.log("INFO", f"OS: {platform.system()} {platform.release()}")
        self.log.log("INFO", f"OpenCV: {cv2.__version__}")
        self.log.log("INFO", f"Working Directory: {Path.cwd()}")
        self.log.log("INFO", separator)

        try:
            cv2.setLogCallback(lambda level, msg: self.log.log("INFO", f"OpenCV [{level}]: {msg.strip()}"))
        except Exception:
            self.log.log("WARN", "cv2.setLogCallback não disponível. Logs do OpenCV não serão capturados.")

        self.old_stderr = sys.stderr
        try:
            r, w = os.pipe()
            self.stderr_r = os.fdopen(r, "r")
            sys.stderr = os.fdopen(w, "w")
            threading.Thread(target=self._read_stderr, daemon=True).start()
        except Exception:
            self.log.log("WARN", "Falha ao redirecionar stderr. Prosseguindo sem captura.")

        self._load_or_create_config()
        self.cam_status_labels = {}
        self.cam_transport_labels = {}
        self.cam_rtsp_labels = {}
        self._apply_rtsp_transport_from_config()

        token = self.config["TELEGRAM"].get("bot_token", "")
        chat_id = self.config["TELEGRAM"].get("chat_id", "")
        self.telegram = TelegramBot(token, chat_id, self.log)
        self.log.set_telegram(self.telegram)

        self.detectors: Dict[int, RTSPObjectDetector] = {}
        self.threads: Dict[int, threading.Thread] = {}
        self.running = False

        # Watchdog (monotonic)
        self.watchdog_interval_ms = 2000
        self.watchdog_no_frame_s = 20.0  # Aumentado de 12s para 20s (rede instável)
        self.watchdog_restart_backoff_s = 10.0
        self._last_restart_mono: Dict[int, float] = {}

        self._last_daily_restart_date = None

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_video = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_video, text="Vídeo (Mosaico 2x2)")
        self._build_video_mosaic()
        self._apply_rtsp_transport_from_config()

        self.frame_config = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_config, text="Config")
        self._build_config_tab()

        self.frame_fotos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_fotos, text="Fotos")
        self._build_photos_tab()

        self.frame_logs = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_logs, text="Logs")
        self._build_logs_tab()

        self.frame_about = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_about, text="Sobre")
        self._build_about_tab()

        self._load_logs_tail()

        self._process_queues()
        self.log.log("INFO", "UI initialized successfully")

        self.root.after(600, self.start_system)
        self.root.after(self.watchdog_interval_ms, self._supervise_cameras)
        self.root.after(1500, self._daily_restart_tick)
        self.root.after(1000, self._update_camera_status)
        self.root.after(5000, self._check_system_events_buffer)  # Verificar buffer a cada 5s
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _read_stderr(self):
        try:
            for line in self.stderr_r:
                self.log.log("ERROR", f"STDERR: {line.strip()}")
        except Exception:
            pass

    # ---------------- CONFIG ----------------
    def _load_or_create_config(self):
        defaults = {
            "CAM1": {"enabled": "True", "rtsp_url": "rtsp://admin:senha@192.168.1.100:554/stream1"},
            "CAM2": {"enabled": "True", "rtsp_url": "rtsp://admin:senha@192.168.1.101:554/stream1"},
            "CAM3": {"enabled": "True", "rtsp_url": "rtsp://admin:senha@192.168.1.102:554/stream1"},
            "CAM4": {"enabled": "True", "rtsp_url": "rtsp://admin:senha@192.168.1.103:554/stream1"},
            "DETECTOR": {
                "cooldown": "2",
                "confidence_threshold": "0.5",
                "nms_threshold": "0.4",
                "photos_per_event": "2",
                "classes_enabled": "person",
                "min_capture_interval_s": "1.0",
                "presence_exit_timeout_s": "3.0",
                "presence_mid_alert_after_s": "20.0",
                "presence_min_move_px": "25.0",
                "skip_frames": "2",  # Pula 2 frames (processa 1 a cada 3) - melhora performance
                "input_size": "320",  # Resolução YOLO (320=rápido, 416=preciso, 608=lento)
                "rtsp_transport": "udp",  # UDP (padrão) ou TCP
            },
            "TELEGRAM": {
                "bot_token": "",
                "chat_id": "",
                "alert_mode": "detections",
            },
            "UI": {
                "show_tips": "True",
                "auto_scroll_logs": "True",
                "log_show_info": "True",
                "log_show_warn": "True",
                "log_show_error": "True",
            }
        }

        if not self.config_file.exists():
            for sec, vals in defaults.items():
                self.config[sec] = vals
            with open(self.config_file, "w", encoding="utf-8") as f:
                self.config.write(f)
            return

        self.config.read(self.config_file, encoding="utf-8")

        updated = False
        for sec, vals in defaults.items():
            if sec not in self.config:
                self.config[sec] = vals
                updated = True
            else:
                for k, v in vals.items():
                    if k not in self.config[sec]:
                        self.config[sec][k] = v
                        updated = True

        if updated:
            with open(self.config_file, "w", encoding="utf-8") as f:
                self.config.write(f)

    def _save_config(self):
        self.config["CAM1"]["enabled"] = str(bool(self.var_cam1.get()))
        self.config["CAM2"]["enabled"] = str(bool(self.var_cam2.get()))
        self.config["CAM3"]["enabled"] = str(bool(self.var_cam3.get()))
        self.config["CAM4"]["enabled"] = str(bool(self.var_cam4.get()))

        self.config["CAM1"]["rtsp_url"] = self.e_rtsp1.get().strip()
        self.config["CAM2"]["rtsp_url"] = self.e_rtsp2.get().strip()
        self.config["CAM3"]["rtsp_url"] = self.e_rtsp3.get().strip()
        self.config["CAM4"]["rtsp_url"] = self.e_rtsp4.get().strip()

        self.config["DETECTOR"]["cooldown"] = self.sp_cooldown.get().strip()
        self.config["DETECTOR"]["confidence_threshold"] = self.sp_conf.get().strip()
        self.config["DETECTOR"]["nms_threshold"] = self.sp_nms.get().strip()
        self.config["DETECTOR"]["photos_per_event"] = self.sp_photos.get().strip()
        self.config["DETECTOR"]["min_capture_interval_s"] = self.sp_min_capture.get().strip()
        self.config["DETECTOR"]["rtsp_transport"] = self.cb_rtsp_transport.get().strip().lower()
        self.config["DETECTOR"]["max_photos_keep"] = self.sp_max_photos.get().strip()

        enabled = []
        if self.var_person.get(): enabled.append("person")
        if self.var_car.get(): enabled.append("car")
        if self.var_bus.get(): enabled.append("bus")
        if self.var_truck.get(): enabled.append("truck")
        if self.var_motorcycle.get(): enabled.append("motorcycle")
        if self.var_bicycle.get(): enabled.append("bicycle")
        if self.var_dog.get(): enabled.append("dog")
        if self.var_cat.get(): enabled.append("cat")
        if self.var_bird.get(): enabled.append("bird")
        if self.var_horse.get(): enabled.append("horse")
        if not enabled:
            enabled = ["person"]
        self.config["DETECTOR"]["classes_enabled"] = ",".join(enabled)

        self.config["TELEGRAM"]["bot_token"] = self.e_token.get().strip()
        self.config["TELEGRAM"]["chat_id"] = self.e_chat.get().strip()
        self.config["TELEGRAM"]["alert_mode"] = self.cb_alert.get().strip()

        self.config["UI"]["show_tips"] = str(bool(self.var_show_tips.get()))
        self.config["UI"]["auto_scroll_logs"] = str(bool(self.var_auto_scroll.get()))
        self.config["UI"]["log_show_info"] = str(bool(self.var_log_info.get()))
        self.config["UI"]["log_show_warn"] = str(bool(self.var_log_warn.get()))
        self.config["UI"]["log_show_error"] = str(bool(self.var_log_error.get()))

        with open(self.config_file, "w", encoding="utf-8") as f:
            self.config.write(f)

    def _apply_rtsp_transport_from_config(self):
        transport = self.config["DETECTOR"].get("rtsp_transport", "udp")
        set_ffmpeg_capture_options(transport)
        self._update_transport_labels(transport)
        self._update_rtsp_labels_from_config()
        try:
            self.log.log("INFO", f"RTSP transport definido para {transport.upper()}")
        except Exception:
            pass

    def _update_transport_labels(self, transport: str) -> None:
        mode = (transport or "udp").strip().upper()
        if mode not in ("UDP", "TCP"):
            mode = "UDP"
        for cam_id, lbl in self.cam_transport_labels.items():
            try:
                lbl.config(text=f"({mode})")
            except Exception:
                pass

    def _update_rtsp_labels_from_config(self) -> None:
        for cam_id, lbl in self.cam_rtsp_labels.items():
            try:
                rtsp_url = self.config[f"CAM{cam_id}"].get("rtsp_url", "").strip()
                lbl.config(text=rtsp_url)
            except Exception:
                pass

    # ---------------- UI BUILD ----------------
    def _build_video_mosaic(self):
        self.frame_video.columnconfigure(0, weight=1, uniform="cam")
        self.frame_video.columnconfigure(1, weight=1, uniform="cam")
        self.frame_video.rowconfigure(0, weight=1, uniform="cam")
        self.frame_video.rowconfigure(1, weight=1, uniform="cam")

        self.cam_cells = {}
        self.cam_labels = {}
        self.cam_status_labels = {}
        self.cam_transport_labels = {}
        self.cam_rtsp_labels = {}
        self.cam_spinners = {}  # Spinners de loading
        self.cam_spinner_texts = {}  # Textos animados dos spinners
        self.cam_spinner_index = {}  # Índice atual da animação
        self.cam_spinner_status_labels = {}  # Labels com status texto do spinner
        self.cam_disabled_labels = {}  # Labels para câmeras desativadas

        positions = {1: (0, 0), 2: (0, 1), 3: (1, 0), 4: (1, 1)}
        for cam_id, (r, c) in positions.items():
            cell = ttk.Frame(self.frame_video)
            cell.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
            cell.grid_propagate(False)

            header = ttk.Frame(cell)
            header.pack(fill="x")
            # Status indicator (menor e à esquerda)
            status_frame = ttk.Frame(header)
            status_frame.pack(side="left", padx=(6, 2), pady=2)
            self.cam_status_labels[cam_id] = tk.Label(
                status_frame,
                text="●",
                font=("Arial", 6),
                fg="#00FF00",
                bd=0,
                padx=1,
                pady=0
            )
            self.cam_status_labels[cam_id].pack()

            ttk.Label(header, text=f"CAM{cam_id}", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 2), pady=2)

            # RTSP transport label
            transport = self.config["DETECTOR"].get("rtsp_transport", "udp").strip().upper()
            self.cam_transport_labels[cam_id] = ttk.Label(header, text=f"({transport})", foreground="#666666")
            self.cam_transport_labels[cam_id].pack(side="left", padx=(0, 6), pady=2)

            # RTSP URL label
            rtsp_url = self.config[f"CAM{cam_id}"].get("rtsp_url", "").strip()
            self.cam_rtsp_labels[cam_id] = ttk.Label(header, text=rtsp_url, foreground="#444444")
            self.cam_rtsp_labels[cam_id].pack(side="left", padx=(0, 6), pady=2)

            lbl = tk.Label(cell, bg="black")
            lbl.pack(fill="both", expand=True)

            # Overlay com spinner de loading
            spinner_overlay = tk.Label(lbl, bg="black", text="", font=("Arial", 24, "bold"), fg="#00FF00")
            spinner_overlay.place(relx=0.5, rely=0.45, anchor="center")
            self.cam_spinners[cam_id] = spinner_overlay
            self.cam_spinner_texts[cam_id] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            self.cam_spinner_index[cam_id] = 0

            # Status texto do spinner
            spinner_status = tk.Label(lbl, bg="black", text="", font=("Arial", 9), fg="#AAAAAA")
            spinner_status.place(relx=0.5, rely=0.55, anchor="center")
            self.cam_spinner_status_labels[cam_id] = spinner_status

            # Label para câmera desativada
            disabled_label = tk.Label(lbl, bg="black", text="", font=("Arial", 28, "bold"), fg="#555555")
            disabled_label.place(relx=0.5, rely=0.45, anchor="center")
            self.cam_disabled_labels[cam_id] = disabled_label

            self.cam_cells[cam_id] = cell
            self.cam_labels[cam_id] = lbl

    def _build_config_tab(self):
        # Armazenar referência de widgets para mostrar/esconder tooltips
        self.tip_widgets = []

        # Canvas com Scrollbar para Config (ocupa a maior parte)
        canvas = tk.Canvas(self.frame_config, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame_config, orient="vertical", command=canvas.yview)
        wrap = ttk.Frame(canvas)

        wrap.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=wrap, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mouse wheel scroll
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame para botões (fixo na base, não faz scroll)
        bottom_frame = ttk.Frame(self.frame_config)
        bottom_frame.pack(side="bottom", fill="x", padx=6, pady=6)

        # ========== CHECKBOX DE TIPS ==========
        tips_frame = ttk.Frame(wrap)
        tips_frame.pack(fill="x", pady=(0, 15), padx=5)

        self.var_show_tips = tk.BooleanVar(value=self.config["UI"].getboolean("show_tips", fallback=True))
        self.cb_tips = ttk.Checkbutton(
            tips_frame, text="Mostrar Dicas (Tips) dos campos",
            variable=self.var_show_tips,
            command=self._toggle_tips_visibility
        )
        self.cb_tips.pack(side="left")
        
        # Inicializar variável de auto-scroll dos logs
        self.var_auto_scroll = tk.BooleanVar(value=self.config["UI"].getboolean("auto_scroll_logs", fallback=True))

        ttk.Label(tips_frame, text="— Ative para exibir explicações de cada parâmetro", foreground="gray").pack(side="left", padx=10)

        # ========== CÂMERAS ==========
        rt = ttk.LabelFrame(wrap, text="Câmeras (ativar/desativar) + RTSP", padding=10)
        rt.pack(fill="x", pady=8)

        def cam_row(row, label, var_enable, entry):
            cb = ttk.Checkbutton(rt, text=label, variable=var_enable)
            cb.grid(row=row, column=0, sticky="w", padx=4)
            entry.grid(row=row, column=1, padx=6, pady=4, sticky="we")
            self._add_tooltip_to_widget(cb, CONFIGURATION_TIPS["cam_enabled"])
            self._add_tooltip_to_widget(entry, CONFIGURATION_TIPS["cam_rtsp"])

        self.var_cam1 = tk.BooleanVar(value=self.config["CAM1"].getboolean("enabled", fallback=True))
        self.var_cam2 = tk.BooleanVar(value=self.config["CAM2"].getboolean("enabled", fallback=True))
        self.var_cam3 = tk.BooleanVar(value=self.config["CAM3"].getboolean("enabled", fallback=True))
        self.var_cam4 = tk.BooleanVar(value=self.config["CAM4"].getboolean("enabled", fallback=True))

        self.e_rtsp1 = ttk.Entry(rt, width=100)
        self.e_rtsp2 = ttk.Entry(rt, width=100)
        self.e_rtsp3 = ttk.Entry(rt, width=100)
        self.e_rtsp4 = ttk.Entry(rt, width=100)

        cam_row(0, "CAM1", self.var_cam1, self.e_rtsp1)
        cam_row(1, "CAM2", self.var_cam2, self.e_rtsp2)
        cam_row(2, "CAM3", self.var_cam3, self.e_rtsp3)
        cam_row(3, "CAM4", self.var_cam4, self.e_rtsp4)

        rt.columnconfigure(1, weight=1)

        self.e_rtsp1.insert(0, self.config["CAM1"]["rtsp_url"])
        self.e_rtsp2.insert(0, self.config["CAM2"]["rtsp_url"])
        self.e_rtsp3.insert(0, self.config["CAM3"]["rtsp_url"])
        self.e_rtsp4.insert(0, self.config["CAM4"]["rtsp_url"])

        # ========== DETECTOR ==========
        det = ttk.LabelFrame(wrap, text="Detector", padding=10)
        det.pack(fill="x", pady=8)

        lbl_cooldown = ttk.Label(det, text="Cooldown (s):")
        lbl_cooldown.grid(row=0, column=0, sticky="w")
        self.sp_cooldown = ttk.Spinbox(det, from_=1, to=30, width=8)
        self.sp_cooldown.grid(row=0, column=1, padx=6, pady=4, sticky="w")
        self.sp_cooldown.set(self.config["DETECTOR"].get("cooldown", "2"))
        self._add_tooltip_to_widget(lbl_cooldown, CONFIGURATION_TIPS["cooldown"])
        self._add_tooltip_to_widget(self.sp_cooldown, CONFIGURATION_TIPS["cooldown"])

        lbl_conf = ttk.Label(det, text="Confiança:")
        lbl_conf.grid(row=0, column=2, sticky="w")
        self.sp_conf = ttk.Spinbox(det, from_=0.2, to=0.95, increment=0.05, width=8)
        self.sp_conf.grid(row=0, column=3, padx=6, pady=4, sticky="w")
        self.sp_conf.set(self.config["DETECTOR"].get("confidence_threshold", "0.5"))
        self._add_tooltip_to_widget(lbl_conf, CONFIGURATION_TIPS["confidence"])
        self._add_tooltip_to_widget(self.sp_conf, CONFIGURATION_TIPS["confidence"])

        lbl_nms = ttk.Label(det, text="NMS:")
        lbl_nms.grid(row=0, column=4, sticky="w")
        self.sp_nms = ttk.Spinbox(det, from_=0.2, to=0.95, increment=0.05, width=8)
        self.sp_nms.grid(row=0, column=5, padx=6, pady=4, sticky="w")
        self.sp_nms.set(self.config["DETECTOR"].get("nms_threshold", "0.4"))
        self._add_tooltip_to_widget(lbl_nms, CONFIGURATION_TIPS["nms"])
        self._add_tooltip_to_widget(self.sp_nms, CONFIGURATION_TIPS["nms"])

        lbl_photos = ttk.Label(det, text="Fotos por evento:")
        lbl_photos.grid(row=0, column=6, sticky="w")
        self.sp_photos = ttk.Spinbox(det, from_=1, to=10, width=6)
        self.sp_photos.grid(row=0, column=7, padx=6, pady=4, sticky="w")
        self.sp_photos.set(self.config["DETECTOR"].get("photos_per_event", "2"))
        self._add_tooltip_to_widget(lbl_photos, CONFIGURATION_TIPS["photos"])
        self._add_tooltip_to_widget(self.sp_photos, CONFIGURATION_TIPS["photos"])

        lbl_min_capture = ttk.Label(det, text="Intervalo mín. entre fotos (s):")
        lbl_min_capture.grid(row=1, column=0, sticky="w")
        self.sp_min_capture = ttk.Spinbox(det, from_=0.2, to=10.0, increment=0.1, width=8)
        self.sp_min_capture.grid(row=1, column=1, padx=6, pady=4, sticky="w")
        self.sp_min_capture.set(self.config["DETECTOR"].get("min_capture_interval_s", "1.0"))
        self._add_tooltip_to_widget(lbl_min_capture, CONFIGURATION_TIPS["min_capture"])
        self._add_tooltip_to_widget(self.sp_min_capture, CONFIGURATION_TIPS["min_capture"])

        lbl_transport = ttk.Label(det, text="RTSP Transport:")
        lbl_transport.grid(row=1, column=2, sticky="w")
        self.cb_rtsp_transport = ttk.Combobox(det, values=["udp", "tcp"], state="readonly", width=8)
        self.cb_rtsp_transport.grid(row=1, column=3, padx=6, pady=4, sticky="w")
        self.cb_rtsp_transport.set(self.config["DETECTOR"].get("rtsp_transport", "udp").lower())
        self._add_tooltip_to_widget(lbl_transport, CONFIGURATION_TIPS["rtsp_transport"])
        self._add_tooltip_to_widget(self.cb_rtsp_transport, CONFIGURATION_TIPS["rtsp_transport"])

        lbl_max_photos = ttk.Label(det, text="Máx. fotos manter:")
        lbl_max_photos.grid(row=1, column=4, sticky="w")
        self.sp_max_photos = ttk.Spinbox(det, from_=50, to=2000, increment=50, width=8)
        self.sp_max_photos.grid(row=1, column=5, padx=6, pady=4, sticky="w")
        self.sp_max_photos.set(self.config["DETECTOR"].get("max_photos_keep", "500"))
        self._add_tooltip_to_widget(lbl_max_photos, CONFIGURATION_TIPS["max_photos"])
        self._add_tooltip_to_widget(self.sp_max_photos, CONFIGURATION_TIPS["max_photos"])

        # ========== CLASSES ==========
        cls = ttk.LabelFrame(wrap, text="Classes (somente pessoa dispara alerta)", padding=10)
        cls.pack(fill="x", pady=8)

        enabled = set(x.strip() for x in self.config["DETECTOR"].get("classes_enabled", "person").split(",") if x.strip())

        self.var_person = tk.BooleanVar(value=("person" in enabled))
        self.var_car = tk.BooleanVar(value=("car" in enabled))
        self.var_bus = tk.BooleanVar(value=("bus" in enabled))
        self.var_truck = tk.BooleanVar(value=("truck" in enabled))
        self.var_motorcycle = tk.BooleanVar(value=("motorcycle" in enabled))
        self.var_bicycle = tk.BooleanVar(value=("bicycle" in enabled))
        self.var_dog = tk.BooleanVar(value=("dog" in enabled))
        self.var_cat = tk.BooleanVar(value=("cat" in enabled))
        self.var_bird = tk.BooleanVar(value=("bird" in enabled))
        self.var_horse = tk.BooleanVar(value=("horse" in enabled))

        cb_person = ttk.Checkbutton(cls, text="person", variable=self.var_person)
        cb_person.grid(row=0, column=0, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_person, CONFIGURATION_TIPS["person"])

        cb_car = ttk.Checkbutton(cls, text="car", variable=self.var_car)
        cb_car.grid(row=0, column=1, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_car, CONFIGURATION_TIPS["car"])

        cb_bus = ttk.Checkbutton(cls, text="bus", variable=self.var_bus)
        cb_bus.grid(row=0, column=2, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_bus, CONFIGURATION_TIPS["bus"])

        cb_truck = ttk.Checkbutton(cls, text="truck", variable=self.var_truck)
        cb_truck.grid(row=0, column=3, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_truck, CONFIGURATION_TIPS["truck"])

        cb_motorcycle = ttk.Checkbutton(cls, text="motorcycle", variable=self.var_motorcycle)
        cb_motorcycle.grid(row=0, column=4, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_motorcycle, CONFIGURATION_TIPS["motorcycle"])

        cb_bicycle = ttk.Checkbutton(cls, text="bicycle", variable=self.var_bicycle)
        cb_bicycle.grid(row=0, column=5, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_bicycle, CONFIGURATION_TIPS["bicycle"])

        cb_dog = ttk.Checkbutton(cls, text="dog", variable=self.var_dog)
        cb_dog.grid(row=1, column=0, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_dog, CONFIGURATION_TIPS["dog"])

        cb_cat = ttk.Checkbutton(cls, text="cat", variable=self.var_cat)
        cb_cat.grid(row=1, column=1, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_cat, CONFIGURATION_TIPS["cat"])

        cb_bird = ttk.Checkbutton(cls, text="bird", variable=self.var_bird)
        cb_bird.grid(row=1, column=2, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_bird, CONFIGURATION_TIPS["bird"])

        cb_horse = ttk.Checkbutton(cls, text="horse", variable=self.var_horse)
        cb_horse.grid(row=1, column=3, sticky="w", padx=6, pady=2)
        self._add_tooltip_to_widget(cb_horse, CONFIGURATION_TIPS["horse"])

        # ========== TELEGRAM ==========
        tg = ttk.LabelFrame(wrap, text="Telegram (persistente em config.ini)", padding=10)
        tg.pack(fill="x", pady=8)

        lbl_token = ttk.Label(tg, text="Bot Token:")
        lbl_token.grid(row=0, column=0, sticky="w")
        self.e_token = ttk.Entry(tg, width=60)
        self.e_token.grid(row=0, column=1, padx=6, pady=4, sticky="w")
        self.e_token.insert(0, self.config["TELEGRAM"].get("bot_token", ""))
        self._add_tooltip_to_widget(lbl_token, CONFIGURATION_TIPS["bot_token"])
        self._add_tooltip_to_widget(self.e_token, CONFIGURATION_TIPS["bot_token"])

        lbl_chat = ttk.Label(tg, text="Chat ID:")
        lbl_chat.grid(row=1, column=0, sticky="w")
        self.e_chat = ttk.Entry(tg, width=60)
        self.e_chat.grid(row=1, column=1, padx=6, pady=4, sticky="w")
        self.e_chat.insert(0, self.config["TELEGRAM"].get("chat_id", ""))
        self._add_tooltip_to_widget(lbl_chat, CONFIGURATION_TIPS["chat_id"])
        self._add_tooltip_to_widget(self.e_chat, CONFIGURATION_TIPS["chat_id"])

        lbl_alert = ttk.Label(tg, text="Alertas (fotos):")
        lbl_alert.grid(row=2, column=0, sticky="w")
        self.cb_alert = ttk.Combobox(tg, values=["all", "detections", "none"], state="readonly", width=12)
        self.cb_alert.grid(row=2, column=1, padx=6, pady=4, sticky="w")
        self.cb_alert.set(self.config["TELEGRAM"].get("alert_mode", "detections"))
        self._add_tooltip_to_widget(lbl_alert, CONFIGURATION_TIPS["alert_mode"])
        self._add_tooltip_to_widget(self.cb_alert, CONFIGURATION_TIPS["alert_mode"])

        self.btn_test_telegram = ttk.Button(tg, text="Testar envio", command=self._send_telegram_test)
        self.btn_test_telegram.grid(row=3, column=1, padx=6, pady=(6, 2), sticky="w")

        # ========== CONTROLES ==========
        ctrl = bottom_frame
        
        self.btn_save = ttk.Button(ctrl, text="Salvar (reinicia)", command=self.save_and_restart)
        self.btn_save.pack(side="left", padx=6)

        self.btn_reload = ttk.Button(ctrl, text="Recarregar (reinicia)", command=self.reload_and_restart)
        self.btn_reload.pack(side="left", padx=6)

        self.btn_start = ttk.Button(ctrl, text="Iniciar", command=self.start_system)
        self.btn_start.pack(side="left", padx=20)

        self.btn_stop = ttk.Button(ctrl, text="Parar", command=self.stop_system, state="disabled")
        self.btn_stop.pack(side="left", padx=6)

        self.lbl_status = ttk.Label(ctrl, text="Status: Parado", foreground="red")
        self.lbl_status.pack(side="left", padx=20)

    def _add_tooltip_to_widget(self, widget, tip_text: str):
        """Adiciona um tooltip que aparece/desaparece conforme o checkbox de tips"""
        self.tip_widgets.append((widget, tip_text))

    def _toggle_tips_visibility(self):
        """Alterna a visibilidade dos tooltips"""
        show_tips = self.var_show_tips.get()
        for widget, tip_text in self.tip_widgets:
            if show_tips:
                self._show_tooltip_on_hover(widget, tip_text)
            else:
                self._hide_tooltip(widget)

    def _show_tooltip_on_hover(self, widget, text):
        """Mostra tooltip ao passar mouse sobre widget"""
        def on_enter(event):
            if not self.var_show_tips.get():
                return
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1, wraplength=300, justify="left", font=("Arial", 9))
            label.pack()
            widget.tooltip = tooltip

            def on_leave(event):
                if hasattr(widget, "tooltip"):
                    try:
                        widget.tooltip.destroy()
                    except:
                        pass
                    widget.tooltip = None

            widget.bind("<Leave>", on_leave)

        widget.bind("<Enter>", on_enter)

    def _hide_tooltip(self, widget):
        """Esconde tooltip"""
        if hasattr(widget, "tooltip"):
            try:
                widget.tooltip.destroy()
            except:
                pass
            widget.tooltip = None

    def _build_photos_tab(self):
        self.photos_canvas = tk.Canvas(self.frame_fotos)
        self.photos_scroll = ttk.Scrollbar(self.frame_fotos, orient="vertical", command=self.photos_canvas.yview)
        self.photos_wrap = ttk.Frame(self.photos_canvas)

        self.photos_wrap.bind("<Configure>", lambda e: self.photos_canvas.configure(scrollregion=self.photos_canvas.bbox("all")))
        self.photos_canvas.create_window((0, 0), window=self.photos_wrap, anchor="nw")
        self.photos_canvas.configure(yscrollcommand=self.photos_scroll.set)

        self.photos_canvas.pack(side="left", fill="both", expand=True)
        self.photos_scroll.pack(side="right", fill="y")

        self.thumb_items = []

    def _build_logs_tab(self):
        # Frame superior para controles
        control_frame = ttk.Frame(self.frame_logs)
        control_frame.pack(fill="x", padx=6, pady=6)

        # Filtro de níveis
        self.var_log_info = tk.BooleanVar(value=self.config["UI"].getboolean("log_show_info", fallback=True))
        self.var_log_warn = tk.BooleanVar(value=self.config["UI"].getboolean("log_show_warn", fallback=True))
        self.var_log_error = tk.BooleanVar(value=self.config["UI"].getboolean("log_show_error", fallback=True))

        ttk.Label(control_frame, text="Níveis:").pack(side="left", padx=(0, 4))
        ttk.Checkbutton(control_frame, text="INFO", variable=self.var_log_info, command=self._refresh_logs_view).pack(side="left", padx=4)
        ttk.Checkbutton(control_frame, text="WARN", variable=self.var_log_warn, command=self._refresh_logs_view).pack(side="left", padx=4)
        ttk.Checkbutton(control_frame, text="ERROR", variable=self.var_log_error, command=self._refresh_logs_view).pack(side="left", padx=4)
        
        # Checkbox de auto-scroll
        self.cb_auto_scroll = ttk.Checkbutton(
            control_frame, text="Auto-scroll automático",
            variable=self.var_auto_scroll
        )
        self.cb_auto_scroll.pack(side="left", padx=4)
        
        # Botão limpar
        ttk.Button(control_frame, text="Limpar Logs", command=self._clear_logs).pack(side="left", padx=4)
        
        # Text widget com scroll
        self.text_logs = scrolledtext.ScrolledText(self.frame_logs, wrap=tk.WORD, font=("Courier", 9))
        self.text_logs.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Configurar cores para diferentes níveis de log
        self.text_logs.tag_config("ERROR", foreground="#FF0000")  # Vermelho
        self.text_logs.tag_config("WARN", foreground="#FF8C00")   # Laranja escuro

    def _build_about_tab(self):
        ttk.Label(self.frame_about, text=f"Versão: {APP_VERSION}", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.frame_about, text=f"Commit: {get_commit_code()}", font=("Arial", 10)).pack(pady=2)
        ttk.Label(self.frame_about, text="Autor: Fabio Bettio", font=("Arial", 10)).pack(pady=5)
        ttk.Label(self.frame_about, text="Data:           02/02/2026", font=("Arial", 10)).pack(pady=5)
        ttk.Label(self.frame_about, text="Licença: Uso educacional/experimental", font=("Arial", 10)).pack(pady=5)

        ttk.Label(
            self.frame_about,
            text=(
                "Projeto de monitoramento 24/7 de múltiplas câmeras RTSP com detecção "
                "de pessoas via YOLOv4-tiny (OpenCV DNN), alertas Telegram, logs detalhados "
                "e rastreabilidade de eventos."
            ),
            font=("Arial", 10),
            wraplength=520,
            justify="left"
        ).pack(pady=(10, 6))

        ttk.Label(
            self.frame_about,
            text="Recursos: detecção em tempo real, grupos por evento,  "
                 "controle de falsos positivos e captura persistente de fotos.",
            font=("Arial", 10),
            wraplength=520,
            justify="left"
        ).pack(pady=(0, 10))

        repo_url = "https://github.com/Espaco-CMaker/AlertaIntruso"
        link = tk.Label(self.frame_about, text=repo_url, fg="#1a73e8", cursor="hand2", font=("Arial", 10, "underline"))
        link.pack(pady=(2, 0))
        link.bind("<Button-1>", lambda e: webbrowser.open_new(repo_url))

    def _load_logs_tail(self):
        lf = Path("log.txt")
        if not lf.exists():
            return
        try:
            with open(lf, "r", encoding="utf-8") as f:
                lines = f.readlines()[-200:]
            for ln in lines:
                if not self._is_log_line_enabled(ln):
                    continue
                level = self._extract_log_level(ln)
                if level == "ERROR":
                    self.text_logs.insert(tk.END, ln, "ERROR")
                elif level == "WARN":
                    self.text_logs.insert(tk.END, ln, "WARN")
                else:
                    self.text_logs.insert(tk.END, ln)
            # Scroll automático apenas se checkbox estiver ativado
            if self.var_auto_scroll.get():
                self.text_logs.see(tk.END)
        except Exception:
            pass

    def _extract_log_level(self, line: str) -> str:
        try:
            parts = line.split("|")
            if len(parts) >= 2:
                return parts[1].strip().upper()
        except Exception:
            pass
        return ""

    def _is_log_line_enabled(self, line: str) -> bool:
        level = self._extract_log_level(line)
        if level == "ERROR":
            return bool(self.var_log_error.get())
        if level == "WARN":
            return bool(self.var_log_warn.get())
        if level == "INFO":
            return bool(self.var_log_info.get())
        return True

    def _refresh_logs_view(self):
        if not hasattr(self, "text_logs"):
            return
        try:
            self.text_logs.delete("1.0", tk.END)
            self._load_logs_tail()
        except Exception:
            pass

    def _clear_logs(self):
        try:
            # Limpar arquivo de log
            Path("log.txt").write_text("", encoding="utf-8")
        except Exception:
            pass

        # Limpar fila de logs pendentes
        try:
            while True:
                self.log_queue.get_nowait()
        except Exception:
            pass

        # Limpar tela
        try:
            self.text_logs.delete("1.0", tk.END)
        except Exception:
            pass

    # ---------------- QUEUES ----------------
    def _process_queues(self):
        try:
            while True:
                cam_id, frame_bgr = self.frame_queue.get_nowait()
                self._update_cam_frame(cam_id, frame_bgr)
                self._hide_spinner(cam_id)  # Esconder spinner quando tem frame
        except queue.Empty:
            pass

        try:
            while True:
                cam_id, foto_path, ts, event_uid, shot_idx, crop_path = self.photo_queue.get_nowait()
                self._add_thumbnail(cam_id, foto_path, ts, event_uid, shot_idx, crop_path)
        except queue.Empty:
            pass

        try:
            while True:
                line = self.log_queue.get_nowait()
                try:
                    if not self._is_log_line_enabled(line):
                        continue
                    # Detectar nível de log e aplicar cor
                    level = self._extract_log_level(line)
                    if level == "ERROR":
                        self.text_logs.insert(tk.END, line, "ERROR")
                    elif level == "WARN":
                        self.text_logs.insert(tk.END, line, "WARN")
                    else:
                        self.text_logs.insert(tk.END, line)
                    # Scroll automático apenas se checkbox estiver ativado
                    if self.var_auto_scroll.get():
                        self.text_logs.see(tk.END)
                except Exception:
                    pass
        except queue.Empty:
            pass

        self._update_spinners()  # Animar spinners
        self.root.after(40, self._process_queues)

    # ---------------- VIDEO RENDER ----------------
    def _update_cam_frame(self, cam_id: int, frame_bgr):
        lbl = self.cam_labels.get(cam_id)
        if not lbl:
            return

        w = lbl.winfo_width()
        h = lbl.winfo_height()
        if w < 20 or h < 20:
            return

        fh, fw = frame_bgr.shape[:2]
        aspect = fw / max(1, fh)

        if (w / max(1, h)) > aspect:
            nh = h
            nw = int(nh * aspect)
        else:
            nw = w
            nh = int(nw / aspect)

        frame_resized = cv2.resize(frame_bgr, (max(1, nw), max(1, nh)))
        rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(img)

        lbl.imgtk = imgtk
        lbl.configure(image=imgtk)

    def _clear_cam_frame(self, cam_id: int):
        """Remove imagem da câmera, deixando apenas fundo preto"""
        lbl = self.cam_labels.get(cam_id)
        if not lbl:
            return
        try:
            lbl.configure(image="")
            lbl.imgtk = None
        except Exception:
            pass

    def _hide_spinner(self, cam_id: int):
        """Esconde spinner quando câmera recebe frames"""
        if cam_id in self.cam_spinners:
            try:
                self.cam_spinners[cam_id].config(text="")
                self.cam_spinner_status_labels[cam_id].config(text="")
                self.cam_disabled_labels[cam_id].config(text="")
            except Exception:
                pass

    def _update_spinners(self):
        """Anima spinners de loading para câmeras offline/conectando"""
        status_messages = {
            "offline": "Iniciando stream...",
            "online": "Conectando...",
            "frozen": "Sem sinal",
            "receiving": ""
        }
        
        for cam_id in range(1, 5):
            if cam_id not in self.cam_spinners:
                continue
            
            # Verificar se câmera está desativada na config
            is_enabled = self.config[f"CAM{cam_id}"].getboolean("enabled", fallback=True)
            
            spinner = self.cam_spinners[cam_id]
            status_label = self.cam_spinner_status_labels[cam_id]
            disabled_label = self.cam_disabled_labels[cam_id]
            
            if not is_enabled:
                # Câmera desativada: limpar imagem e mostrar logo de desativação
                try:
                    self._clear_cam_frame(cam_id)
                    spinner.config(text="")
                    status_label.config(text="")
                    disabled_label.config(text="⊘")  # Símbolo de desativado
                    spinner.place_forget()
                    status_label.place_forget()
                    disabled_label.place(relx=0.5, rely=0.5, anchor="center")
                except Exception:
                    pass
                continue
            
            det = self.detectors.get(cam_id)
            if not det:
                continue

            status = getattr(det, "status", "offline")

            if status in ("offline", "online", "frozen"):
                # Câmera desconectada: limpar imagem e mostrar spinner + texto
                try:
                    self._clear_cam_frame(cam_id)
                    idx = self.cam_spinner_index.get(cam_id, 0)
                    frames = self.cam_spinner_texts.get(cam_id, [])
                    if frames:
                        spinner.config(text=frames[idx % len(frames)])
                        self.cam_spinner_index[cam_id] = (idx + 1) % len(frames)
                    status_label.config(text=status_messages.get(status, "Aguardando..."))
                    disabled_label.config(text="")
                    spinner.place(relx=0.5, rely=0.45, anchor="center")
                    status_label.place(relx=0.5, rely=0.55, anchor="center")
                    disabled_label.place_forget()
                except Exception:
                    pass
            else:
                try:
                    spinner.config(text="")
                    status_label.config(text="")
                    disabled_label.config(text="")
                    spinner.place_forget()
                    status_label.place_forget()
                    disabled_label.place_forget()
                except Exception:
                    pass

    def _update_camera_status(self):
        """Atualiza indicadores de status das câmeras (online, receiving, frozen)"""
        now = time.time()
        for cam_id in range(1, 5):
            if cam_id not in self.detectors:
                continue
            det = self.detectors[cam_id]
            status_label = self.cam_status_labels.get(cam_id)
            if not status_label:
                continue

            status = getattr(det, "status", "offline")
            last_frame_ts = getattr(det, "last_frame_timestamp", 0.0)
            time_since_frame = now - last_frame_ts if last_frame_ts > 0 else 999

            # Detectar se está congelado (sem frames por mais de 20 segundos)
            if time_since_frame > 20.0 and status == "receiving":
                status = "frozen"
                det.status = "frozen"

            # Cores e símbolos
            status_info = {
                "offline": ("⚫", "#666666", "Offline"),
                "online": ("🟡", "#CCAA00", "Online (sem dados)"),
                "receiving": ("🟢", "#00FF00", f"Recebendo ({time_since_frame:.0f}s atrás)"),
                "frozen": ("🔴", "#FF0000", f"Congelado ({time_since_frame:.0f}s sem frame)"),
            }

            symbol, color, tooltip_text = status_info.get(status, ("?", "#999999", "Desconhecido"))
            status_label.config(text=symbol, fg=color)
            status_label.tooltip = tooltip_text

        self.root.after(1000, self._update_camera_status)

    def _check_system_events_buffer(self):
        """Verifica e envia buffer de eventos de sistema periodicamente."""
        try:
            self.log.check_and_flush_buffer()
        except Exception:
            pass
        # Reagendar a cada 5 segundos
        self.root.after(5000, self._check_system_events_buffer)

    # ---------------- THUMBNAILS ----------------
    def _parse_thumb_dt(self, ts: str) -> datetime:
        try:
            return datetime.strptime(ts, "%Y%m%d_%H%M%S")
        except Exception:
            return datetime.now()

    def _get_or_create_group_by_uid(self, event_uid: str, dt: datetime):
        if not hasattr(self, "thumb_groups_by_uid"):
            self.thumb_groups_by_uid = {}
            self.thumb_groups_order = []
            self.last_day_shown = None

        uid = (event_uid or "evt")
        if uid in self.thumb_groups_by_uid:
            g = self.thumb_groups_by_uid[uid]
            g["last_dt"] = dt
            return g

        # Verificar se é um novo dia para adicionar separador
        current_day = dt.date()
        if self.last_day_shown is not None and current_day != self.last_day_shown:
            # Adicionar linha separadora entre dias
            row = 0
            separator = tk.Frame(self.photos_wrap, height=3, bg="black")
            separator.grid(row=row, column=0, sticky="ew", padx=0, pady=5)
            
            # Deslocar todos os grupos existentes
            for other_uid in self.thumb_groups_order:
                g_existing = self.thumb_groups_by_uid[other_uid]
                g_existing["row"] += 1
                g_existing["thumbs_frame"].master.grid(row=g_existing["row"], column=0, sticky="w", padx=8, pady=10)
            
            row = 1
        else:
            row = 0
        
        self.last_day_shown = current_day
        
        # Inserir novo grupo no INÍCIO (fotos mais novas primeiro)
        self.thumb_groups_order.insert(0, uid)
        
        # Atualizar row de todos os grupos existentes (deslocar para baixo)
        for other_uid in self.thumb_groups_order[1:]:
            g_existing = self.thumb_groups_by_uid[other_uid]
            g_existing["row"] += 1
            g_existing["thumbs_frame"].master.grid(row=g_existing["row"], column=0, sticky="w", padx=8, pady=10)

        g_frame = ttk.Frame(self.photos_wrap)
        g_frame.grid(row=row, column=0, sticky="w", padx=8, pady=10)

        header = ttk.Frame(g_frame)
        header.grid(row=0, column=0, sticky="w")

        ttk.Label(header, text=f"EVENTO {uid}", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 10))
        ttk.Label(header, text=dt.strftime("%d/%m %H:%M:%S"), font=("Arial", 9)).pack(side="left")

        thumbs = ttk.Frame(g_frame)
        thumbs.grid(row=1, column=0, sticky="w")

        g = {"uid": uid, "row": row, "start_dt": dt, "last_dt": dt, "thumbs_frame": thumbs, "next_col": 0}
        self.thumb_groups_by_uid[uid] = g
        return g

    def _add_thumbnail(self, cam_id: int, foto_path: str, ts: str, event_uid: str, shot_idx: int, crop_path: str = None):
        try:
            dt = self._parse_thumb_dt(ts)
            group = self._get_or_create_group_by_uid(event_uid, dt)

            # Criar célula para as imagens
            col = int(group["next_col"])
            cell = ttk.Frame(group["thumbs_frame"])
            cell.grid(row=0, column=col, padx=8, pady=6, sticky="w")

            # Frame para as duas imagens (geral e crop) lado a lado
            images_frame = ttk.Frame(cell)
            images_frame.pack()

            # Imagem geral
            img = Image.open(foto_path)
            img.thumbnail((220, 160))
            imgtk = ImageTk.PhotoImage(img)

            img_label = tk.Label(images_frame, image=imgtk, cursor="hand2")
            img_label.image = imgtk
            img_label.grid(row=0, column=0, padx=2)
            img_label.bind("<Button-1>", lambda e, p=foto_path: self._open_photo(p))

            # Imagem crop (se disponível)
            if crop_path and Path(crop_path).exists():
                img_crop = Image.open(crop_path)
                img_crop.thumbnail((110, 160))
                imgtk_crop = ImageTk.PhotoImage(img_crop)

                img_crop_label = tk.Label(images_frame, image=imgtk_crop, cursor="hand2")
                img_crop_label.image = imgtk_crop
                img_crop_label.grid(row=0, column=1, padx=2)
                img_crop_label.bind("<Button-1>", lambda e, p=crop_path: self._open_photo(p))

            ttk.Label(cell, text=f"CAM{cam_id} • S{shot_idx} • {dt.strftime('%H:%M:%S')}", font=("Arial", 9)).pack(pady=(4, 0))

            group["next_col"] = col + 1
            group["last_dt"] = dt

        except Exception as e:
            self.log.log("WARN", f"Falha miniatura: {e}")

    def _open_photo(self, foto_path: str):
        try:
            win = tk.Toplevel(self.root)
            win.title(Path(foto_path).name)

            img = Image.open(foto_path)

            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            max_w = int(sw * 0.85)
            max_h = int(sh * 0.85)

            if img.width > max_w or img.height > max_h:
                img.thumbnail((max_w, max_h))

            imgtk = ImageTk.PhotoImage(img)
            lbl = tk.Label(win, image=imgtk)
            lbl.image = imgtk
            lbl.pack()

            ttk.Button(win, text="Fechar", command=win.destroy).pack(pady=8)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ---------------- APPLY CONFIG TO DETECTOR ----------------
    def _apply_detector_config(self, det: RTSPObjectDetector):
        det.cooldown_s = float(self.config["DETECTOR"].get("cooldown", "2"))
        det.conf_th = float(self.config["DETECTOR"].get("confidence_threshold", "0.5"))
        det.nms_th = float(self.config["DETECTOR"].get("nms_threshold", "0.4"))
        det.telegram_mode = self.config["TELEGRAM"].get("alert_mode", "detections")
        det.photos_per_event = int(self.config["DETECTOR"].get("photos_per_event", "2"))
        det.min_capture_interval_s = float(self.config["DETECTOR"].get("min_capture_interval_s", "1.0"))
        det.presence_exit_timeout_s = float(self.config["DETECTOR"].get("presence_exit_timeout_s", "3.0"))
        det.presence_mid_alert_after_s = float(self.config["DETECTOR"].get("presence_mid_alert_after_s", "20.0"))
        det.presence_min_move_px = float(self.config["DETECTOR"].get("presence_min_move_px", "25.0"))
        det.skip_frames = int(self.config["DETECTOR"].get("skip_frames", "2"))
        det.input_size = int(self.config["DETECTOR"].get("input_size", "320"))
        det.max_photos_keep = int(self.config["DETECTOR"].get("max_photos_keep", "500"))

        name_to_id = {
            "person": 0, "bicycle": 1, "car": 2, "motorcycle": 3,
            "bus": 5, "truck": 7, "bird": 14, "cat": 15, "dog": 16, "horse": 17
        }
        enabled = set()
        raw = self.config["DETECTOR"].get("classes_enabled", "person")
        for token in raw.split(","):
            t = token.strip().lower()
            if t in name_to_id:
                enabled.add(name_to_id[t])
        if not enabled:
            enabled = {0}
        det.classes_enabled = enabled

    # ---------------- SYSTEM START/STOP ----------------
    def _enabled_cams(self):
        cams = []
        for cam_id in (1, 2, 3, 4):
            sec = f"CAM{cam_id}"
            on = self.config.getboolean(sec, "enabled", fallback=True)
            if on:
                cams.append(cam_id)
        return cams

    def _send_telegram_system_start(self, active_count: int):
        if not self.telegram.enabled:
            return
        mode = self.config["TELEGRAM"].get("alert_mode", "detections")
        if mode == "none":
            return
        msg = self.telegram.formatar_msg_inicio(active_count, APP_VERSION, get_commit_code())
        self.telegram.enviar_mensagem(msg)

    def _send_telegram_system_stop(self, total_detections: int):
        if not self.telegram.enabled:
            return
        mode = self.config["TELEGRAM"].get("alert_mode", "detections")
        if mode == "none":
            return
        msg = self.telegram.formatar_msg_encerramento(total_detections, APP_VERSION)
        self.telegram.enviar_mensagem(msg)

    def start_system(self):
        if self.running:
            return

        self._apply_rtsp_transport_from_config()

        token = self.config["TELEGRAM"].get("bot_token", "")
        chat_id = self.config["TELEGRAM"].get("chat_id", "")
        self.telegram = TelegramBot(token, chat_id, self.log)
        self.log.set_telegram(self.telegram)

        self.stop_system(silent=True)

        self.detectors.clear()
        self.threads.clear()

        urls = {
            1: self.config["CAM1"].get("rtsp_url", "").strip(),
            2: self.config["CAM2"].get("rtsp_url", "").strip(),
            3: self.config["CAM3"].get("rtsp_url", "").strip(),
            4: self.config["CAM4"].get("rtsp_url", "").strip(),
        }

        enabled_cams = self._enabled_cams()

        for cam_id in (1, 2, 3, 4):
            if cam_id not in enabled_cams:
                self.log.log("INFO", "Câmera desativada (checkbox).", cam_id)
                continue
            if not urls[cam_id]:
                self.log.log("WARN", "RTSP vazio. Detector não criado.", cam_id)
                continue

            det = RTSPObjectDetector(cam_id, urls[cam_id], self.log, self.telegram)
            self._apply_detector_config(det)

            det.frame_callback = lambda cid, fr, q=self.frame_queue: q.put((cid, fr))
            det.photo_callback = lambda cid, path, ts, event_uid, shot_idx, crop_path, q=self.photo_queue: q.put((cid, path, ts, event_uid, shot_idx, crop_path))

            th = threading.Thread(target=det.run, daemon=True)
            self.detectors[cam_id] = det
            self.threads[cam_id] = th
            th.start()

        self.running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.lbl_status.config(text="Status: Ativo", foreground="green")
        self.log.log("INFO", f"Sistema iniciado. Câmeras ativas: {len(self.detectors)}")
        self._send_telegram_system_start(active_count=len(self.detectors))

    def stop_system(self, silent: bool = False):
        total_detections = 0
        for det in list(self.detectors.values()):
            try:
                total_detections += int(getattr(det, "detections_total", 0))
            except Exception:
                pass

        for det in list(self.detectors.values()):
            try:
                det.stop()
            except Exception:
                pass

        for th in list(self.threads.values()):
            try:
                if th.is_alive():
                    th.join(timeout=0.5)
            except Exception:
                pass

        self.running = False

        if hasattr(self, "btn_start"):
            self.btn_start.config(state="normal")
        if hasattr(self, "btn_stop"):
            self.btn_stop.config(state="disabled")
        if hasattr(self, "lbl_status"):
            self.lbl_status.config(text="Status: Parado", foreground="red")

        if not silent:
            self.log.log("INFO", "Sistema parado.")
            self._send_telegram_system_stop(total_detections=total_detections)

        self.detectors.clear()
        self.threads.clear()

    # ---------------- RESTART HELPERS ----------------
    def _restart_single_camera(self, cam_id: int, reason: str = ""):
        now_mono = time.monotonic()
        last = float(self._last_restart_mono.get(cam_id, 0.0) or 0.0)
        if (now_mono - last) < self.watchdog_restart_backoff_s:
            return

        self._last_restart_mono[cam_id] = now_mono
        self.log.log("WARN", f"Hard restart câmera ({reason})", cam_id)

        det = self.detectors.get(cam_id)
        th = self.threads.get(cam_id)
        try:
            if det:
                det.stop()
        except Exception:
            pass
        try:
            if th and th.is_alive():
                th.join(timeout=0.6)
        except Exception:
            pass

        if cam_id not in self._enabled_cams():
            self.log.log("INFO", "Câmera está desativada. Não recriado.", cam_id)
            self.detectors.pop(cam_id, None)
            self.threads.pop(cam_id, None)
            return

        url = self.config[f"CAM{cam_id}"].get("rtsp_url", "").strip()
        if not url:
            self.log.log("WARN", "RTSP vazio. Não recriado.", cam_id)
            self.detectors.pop(cam_id, None)
            self.threads.pop(cam_id, None)
            return

        token = self.config["TELEGRAM"].get("bot_token", "")
        chat_id = self.config["TELEGRAM"].get("chat_id", "")
        self.telegram = TelegramBot(token, chat_id, self.log)

        try:
            new_det = RTSPObjectDetector(cam_id, url, self.log, self.telegram)
            self._apply_detector_config(new_det)

            new_det.frame_callback = lambda cid, fr, q=self.frame_queue: q.put((cid, fr))
            new_det.photo_callback = lambda cid, path, ts, event_uid, shot_idx, crop_path, q=self.photo_queue: q.put((cid, path, ts, event_uid, shot_idx, crop_path))

            new_th = threading.Thread(target=new_det.run, daemon=True)
            self.detectors[cam_id] = new_det
            self.threads[cam_id] = new_th
            new_th.start()

            self.log.log("INFO", "Hard restart OK.", cam_id)
        except Exception as e:
            self.log.log("ERROR", f"Falha ao recriar câmera: {e}", cam_id)

    def restart_system(self, reason: str = ""):
        self.log.log("WARN", f"Reiniciando sistema ({reason})")
        self.stop_system(silent=True)
        self.start_system()

    def save_and_restart(self):
        try:
            self._save_config()
            self._apply_rtsp_transport_from_config()
            self._update_rtsp_labels_from_config()
            self.log.log("INFO", "Config salva. Reiniciando...")
            self.restart_system(reason="config alterada")
        except Exception as e:
            self.log.log("ERROR", f"Falha ao salvar config: {e}")
            messagebox.showerror("Erro", str(e))

    def reload_and_restart(self):
        try:
            self._load_or_create_config()
            self._apply_rtsp_transport_from_config()
            self._update_rtsp_labels_from_config()
            self.log.log("INFO", "Config recarregada. Reiniciando...")
            self.restart_system(reason="config recarregada")
        except Exception as e:
            self.log.log("ERROR", f"Falha ao recarregar config: {e}")
            messagebox.showerror("Erro", str(e))

    def _send_telegram_test(self):
        token = self.e_token.get().strip()
        chat_id = self.e_chat.get().strip()

        if not token or not chat_id:
            messagebox.showwarning("Telegram", "Informe Bot Token e Chat ID para testar o envio.")
            return

        tg = TelegramBot(token, chat_id, self.log)
        if not tg.enabled:
            messagebox.showwarning("Telegram", "Bot Token ou Chat ID inválidos.")
            return

        try:
            ts = datetime.now()
            ts_str = ts.strftime("%d/%m/%Y %H:%M:%S")
            file_ts = ts.strftime("%Y%m%d_%H%M%S")

            img = Image.new("RGB", (640, 360), (0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.text((20, 20), "ALERTA TESTE", fill=(255, 255, 255))
            draw.text((20, 60), f"{ts_str}", fill=(200, 200, 200))
            draw.text((20, 100), "Simulação de detecção", fill=(200, 200, 200))

            foto_dir = Path("fotos")
            foto_dir.mkdir(exist_ok=True)
            foto_path = foto_dir / f"teste_telegram_{file_ts}.jpg"
            img.save(foto_path, "JPEG", quality=85)

            caption = (
                "🧪 TESTE DE DETECÇÃO\n"
                f"{'━' * 8}\n"
                f"📹 Câmera: TESTE\n"
                f"⏰ {ts_str}\n"
                f"👤 1 pessoa detectada\n"
                f"📊 Confiança: 99.0%\n"
                f"{'━' * 8}\n"
                f"v{APP_VERSION}"
            )

            ok = tg.enviar_foto(str(foto_path), caption)
            if ok:
                self.log.log("INFO", "Teste Telegram enviado com sucesso.")
                messagebox.showinfo("Telegram", "Teste enviado com sucesso!")
            else:
                self.log.log("WARN", "Falha ao enviar teste Telegram.")
                messagebox.showwarning("Telegram", "Falha ao enviar teste.")
        except Exception as e:
            self.log.log("ERROR", f"Erro no teste do Telegram: {e}")
            messagebox.showerror("Telegram", f"Erro ao enviar teste: {e}")

    # ---------------- WATCHDOG ----------------
    def _supervise_cameras(self):
        try:
            if self.running and self.detectors:
                now_mono = time.monotonic()

                for cam_id, det in list(self.detectors.items()):
                    last_mono = float(getattr(det, "last_frame_mono", 0.0) or 0.0)
                    if last_mono <= 0.0:
                        continue

                    delta = now_mono - last_mono
                    if delta > (self.watchdog_no_frame_s * 2):
                        self.log.log("WARN", f"Watchdog: sem frame {delta:.0f}s -> hard restart", cam_id)
                        self._restart_single_camera(cam_id, reason="persistiu sem frame")
                        continue

                    if delta > self.watchdog_no_frame_s:
                        self.log.log("WARN", f"Watchdog: sem frame {delta:.0f}s -> soft reconnect", cam_id)
                        try:
                            det.request_soft_reconnect(reason=f"sem frame {delta:.0f}s")
                        except Exception:
                            pass

        finally:
            self.root.after(self.watchdog_interval_ms, self._supervise_cameras)

    # ---------------- DAILY RESTART ----------------
    def _daily_restart_tick(self):
        try:
            now = datetime.now()
            today = now.strftime("%Y-%m-%d")

            if now.hour == 0 and now.minute == 0:
                if self._last_daily_restart_date != today:
                    self._last_daily_restart_date = today
                    if self.running:
                        self.restart_system(reason="reinicio diario 00:00")
                    else:
                        self.log.log("INFO", "Reinicio diário 00:00 (sistema estava parado).")
        finally:
            self.root.after(20000, self._daily_restart_tick)

    # ---------------- CLOSE ----------------
    def _on_close(self):
        try:
            self.stop_system(silent=False)
        except Exception:
            pass
        self.root.destroy()


# ----------------------------- MAIN -----------------------------
if __name__ == "__main__":
    try:
        os.environ["OPENCV_VIDEOIO_DEBUG"] = "0"
    except Exception:
        pass

    try:
        root = tk.Tk()
        app = InterfaceGrafica(root)
        root.mainloop()
    except Exception as e:
        import traceback
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(f"ERRO FATAL:\n{type(e).__name__}: {e}\n\n")
            f.write(traceback.format_exc())
        print(f"ERRO FATAL: {type(e).__name__}: {e}")
        traceback.print_exc()
        input("Pressione Enter para sair...")
        raise


