"""
================================================================================
ALERTAINTRUSO — ALARME INTELIGENTE POR VISÃO COMPUTACIONAL (RTSP • YOLO • MULTICAM)
================================================================================
Arquivo:        AlertaIntruso Claude+GPT.py
Projeto:        Sistema de Alarme Inteligente por Visão Computacional
Versão:         3.9.1
Data:           01/01/2026
Autor:          Fabio Bettio
Licença:        Uso educacional / experimental

================================================================================
Descrição geral
================================================================================
Aplicação desktop em Python (Tkinter) para monitoramento contínuo (24/7) de
múltiplas câmeras IP via RTSP, com detecção de pessoas utilizando OpenCV DNN
(YOLOv4-tiny). O sistema prioriza robustez operacional, tolerância a falhas
de stream, controle de falsos positivos e rastreabilidade completa de eventos
de movimento.

================================================================================
Arquitetura
================================================================================
- Uma thread dedicada por câmera (RTSPObjectDetector)
- Interface gráfica centralizada (Tkinter + ttk)
- Comunicação thread-safe via queue.Queue
- Watchdog ativo por câmera:
    • Soft reconnect (release + reopen RTSP)
    • Hard restart (recriação completa da thread)
- Backoff progressivo para reconexões RTSP
- Persistência via:
    • config.ini  (configurações)
    • log.txt     (logs rotativos e auditáveis)
    • fotos/      (evidências por evento)
    • models/     (modelos YOLO)

================================================================================
Fluxo de detecção e evento
================================================================================
1. Conexão RTSP resiliente (FFmpeg/OpenCV)
2. Leitura protegida de frames (tratamento de cv2.error e Exception)
3. Validação do frame (None, tamanho zero, baixa variância)
4. Inferência YOLOv4-tiny
5. Filtro por classes habilitadas
6. Análise espacial:
    • Evento somente se a pessoa cruza a linha central da imagem
7. Classificação do movimento:
    • Movimento SEM pessoa  → log informativo
    • Movimento COM pessoa  → geração de evento
8. Geração de EVENT_UID único
9. Captura de evidências (fotos espaçadas)
10. Notificação opcional (Telegram)
11. Atualização da interface gráfica (frame + miniaturas)

================================================================================
Gestão de eventos, IDs e logs
================================================================================
- EVENT_UID único e consistente por evento
- Agrupamento de fotos por EVENT_UID
- Logs registram explicitamente:
    • Inicialização do sistema com versão
    • Configuração efetiva do detector por câmera
    • Movimento sem pessoa (INFO)
    • Evento com pessoa (WARN)
    • Parâmetros ativos da detecção (conf, NMS, cooldown)
    • Métricas de performance (FPS, tempos de leitura e inferência)

================================================================================
Interface gráfica (abas)
================================================================================
Vídeo:
    - Mosaico 2x2
    - Redimensionamento proporcional automático
    - Overlays (bounding boxes, classe, confiança, timestamp)

Config:
    - RTSP por câmera
    - Enable / disable por câmera
    - Cooldown
    - Thresholds (confiança / NMS)
    - Classes habilitadas
    - Telegram (token, chat, modo)
    - Persistência em config.ini

Fotos:
    - Agrupamento por EVENT_UID
    - Uma linha por evento
    - Miniaturas lado a lado
    - Scroll vertical e horizontal
    - Timestamp visível

Logs:
    - Tempo real
    - Histórico local
    - Rotação automática

================================================================================
Resiliência RTSP / OpenCV
================================================================================
- Tratamento explícito de cv2.error, frames inválidos, erros H264 e timeouts FFmpeg
- Erros de decodificação NÃO encerram o sistema
- Sleeps controlados em falha para aliviar CPU
- Fail-safe: exceções não derrubam a aplicação principal

================================================================================
Conceitos aplicados
================================================================================
- Cooldown
- Backoff
- Watchdog
- Fail-safe
- Versionamento semântico

================================================================================
Changelog completo
================================================================================

v3.9.1 (01/01/2026)
    - Log detalhado de eventos de movimento com parâmetros ativos
    - Log explícito de inicialização informando versão
    - Ajustes finos de padronização de mensagens de log
    - Consolidação final da documentação de eventos e métricas

v3.9.0 (01/01/2026)
    - Marco de estabilização arquitetural
    - EVENT_UID definitivo e consistente
    - Agrupamento visual de fotos por evento
    - Scroll vertical e horizontal na aba Fotos
    - Estratégia de evento baseada em cruzamento da linha central
    - Redução significativa de falsos positivos
    - Watchdog estável para operação contínua

v3.8.6
    - Agrupamento inicial de miniaturas por evento
    - Ajustes finais de UI

v3.8.5
    - Evento apenas quando a pessoa cruza a linha central
    - Redução drástica de falsos positivos

v3.8.4
    - Reconexão RTSP robusta com backoff
    - Leitura tolerante a falhas
    - Watchdog por câmera
    - Reinício diário automático às 00:00

v3.8.3
    - Interface em abas consolidada
    - Mosaico 2x2 funcional
    - Mensagem Telegram única no start/stop

v3.8.2
    - Threads por câmera
    - Separação UI / processamento
    - Comunicação via Queue

v3.8.1
    - Primeira versão estável multi-RTSP
    - YOLOv4-tiny via OpenCV DNN

v3.8.0
    - Protótipo inicial
    - Detecção simples
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
from datetime import datetime
from pathlib import Path
import time
import platform
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
    "rtsp_transport;tcp|"
    "stimeout;8000000|"
    "rw_timeout;8000000|"
    "max_delay;300000|"
    "fflags;nobuffer|"
    "flags;low_delay|"
    "reorder_queue_size;0"
)



APP_VERSION = "3.9.1"
MAX_THUMBS = 200


# ----------------------------- Telegram -----------------------------
class TelegramBot:
    def __init__(self, token: str, chat_id: str, log: LogManager = None):
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
            return r.status_code == 200
        except Exception as e:
            if self.log:
                self.log.log("ERROR", f"Erro ao enviar mensagem Telegram: {e}")
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
            return r.status_code == 200
        except Exception as e:
            if self.log:
                self.log.log("ERROR", f"Erro ao enviar foto Telegram: {e}")
            return False


# ----------------------------- Log -----------------------------
class LogManager:
    def __init__(self, log_file="log.txt", max_size_mb=1):
        self.log_file = Path(log_file)
        self.max_size = max_size_mb * 1024 * 1024
        self.callbacks = []
        self._lock = threading.Lock()

    def add_callback(self, cb):
        self.callbacks.append(cb)

    def _rotate_if_needed(self):
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

    def log(self, level: str, msg: str, cam: int | None = None):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = f"[{ts}] [{level}]"
        if cam is not None:
            prefix += f" [CAM{cam}]"
        line = f"{prefix} {msg}\n"

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


# ----------------------------- Detector (1 câmera) -----------------------------
class RTSPObjectDetector:
    """
    Detector para 1 câmera.
    - Envia frames para UI via frame_callback(cam_id, frame_bgr)
    - Envia fotos para UI via photo_callback(cam_id, foto_path, timestamp_str)
    - Evento/alerta/foto: somente se "person" detectada
    - Watchdog usa soft reconnect via request_soft_reconnect()
    """
    def __init__(self, cam_id: int, rtsp_url: str, log: LogManager, telegram: TelegramBot, models_dir="models", foto_dir="fotos"):
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

        self.inf_times = []
        self.last_performance = {}

        # Config runtime
        self.cooldown_s = 2.0
        self.conf_th = 0.5
        self.nms_th = 0.4
        self.input_size = 416
        self.telegram_mode = "detections"  # all | detections | none
        self.photos_per_event = 2

        # Contadores / estado
        self.detections_total = 0
        self.last_frame_ts = 0.0  # atualizado quando um frame válido chega

        # Evento por pessoa
        self._last_event_time = 0.0
        self._pending_shots = 0
        self._event_uid = ""

        self._last_shot_time = 0.0
        self._min_shot_interval = 0.7  # segundos entre fotos do mesmo evento

        # Classes habilitadas (mas evento só dispara se person estiver presente)
        self.classes_enabled = {0}  # person

        # Soft reconnect trigger (watchdog)
        self.reconnect_event = threading.Event()
        self._last_soft_reconnect_ts = 0.0
        self._pending_reconnect_reason = "watchdog"

        # Robustez RTSP
        self._bad_reads = 0
        self._last_reconnect_try = 0.0
        self._reconnect_backoff_s = 2.0   # começa pequeno
        self._max_backoff_s = 20.0


        self._init_yolo()
    def _log_detector_config(self):
        try:
            cls_names = []
            if self.classes and isinstance(self.classes, list):
                for cid in sorted(self.classes_enabled):
                    if 0 <= cid < len(self.classes):
                        cls_names.append(self.classes[cid])
                    else:
                        cls_names.append(str(cid))
            else:
                cls_names = [str(cid) for cid in sorted(self.classes_enabled)]

            self.log.log(
                "INFO",
                "CONFIG DETECTOR | "
                f"cooldown={self.cooldown_s:.2f}s | "
                f"conf_th={self.conf_th:.2f} | nms_th={self.nms_th:.2f} | "
                f"input={self.input_size} | "
                f"photos_per_event={self.photos_per_event} | "
                f"min_shot_interval={self._min_shot_interval:.2f}s | "
                f"classes={','.join(cls_names)} | "
                f"telegram_mode={self.telegram_mode} | v{APP_VERSION}",
                self.cam_id
            )
        except Exception:
            pass


    def _safe_read(self):
        """
        Leitura robusta: cap.read() pode explodir com cv2.error (Unknown C++ exception).
        Retorna (ret, frame, err_str). Se falhou, ret=False e frame=None.
        """
        try:
            ret, frame = self.cap.read()
            return ret, frame, None
        except cv2.error as e:
            return False, None, f"cv2.error: {e}"
        except Exception as e:
            return False, None, f"Exception: {e}"

    def _download_if_missing(self, url: str, dst: Path, label: str):
        if dst.exists():
            return
        self.log.log("INFO", f"Baixando {label}...", self.cam_id)
        urllib.request.urlretrieve(url, dst)
        self.log.log("INFO", f"{label} OK.", self.cam_id)

    def _init_yolo(self):
        try:
            self.log.log("INFO", "Inicializando YOLO...", self.cam_id)

            weights_path = self.models_dir / "yolov4-tiny.weights"
            config_path  = self.models_dir / "yolov4-tiny.cfg"
            names_path   = self.models_dir / "coco.names"

            weights_url = "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights"
            config_url  = "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg"
            names_url   = "https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names"

            self._download_if_missing(weights_url, weights_path, "yolov4-tiny.weights")
            self._download_if_missing(config_url,  config_path,  "yolov4-tiny.cfg")
            self._download_if_missing(names_url,   names_path,   "coco.names")

            with open(names_path, "r", encoding="utf-8") as f:
                self.classes = [line.strip() for line in f.readlines()]

            self.net = cv2.dnn.readNetFromDarknet(str(config_path), str(weights_path))

            if cv2.cuda.getCudaEnabledDeviceCount() > 0:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                self.log.log("INFO", "CUDA ativado.", self.cam_id)
            else:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                self.log.log("INFO", "CPU ativado.", self.cam_id)

            layer_names = self.net.getLayerNames()
            unconnected = self.net.getUnconnectedOutLayers()
            unconnected = unconnected.flatten() if hasattr(unconnected, "flatten") else unconnected
            self.output_layers = [layer_names[i - 1] for i in unconnected]

            self.log.log("INFO", "YOLO pronto.", self.cam_id)
        except Exception as e:
            self.log.log("ERROR", f"Falha ao inicializar YOLO: {e}", self.cam_id)
            raise

    def _connect(self) -> bool:
        try:
            self.log.log("INFO", "Conectando RTSP...", self.cam_id)

            # libera cap antigo se existir (sem deixar lixo)
            try:
                if self.cap is not None:
                    self.cap.release()
            except Exception as e:
                self.log.log("WARN", f"Erro ao liberar cap antigo: {e}", self.cam_id)

            cap = cv2.VideoCapture()  # cria vazio

            # timeouts (nem toda build suporta, então try)
            try:
                cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)  # 5s abrir
                cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)  # 5s ler
            except Exception:
                pass

            # buffer mínimo
            try:
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            except Exception:
                pass

            # abre DEPOIS de configurar
            ok = cap.open(self.rtsp_url, cv2.CAP_FFMPEG)
            if not ok or (not cap.isOpened()):
                raise Exception("Não abriu stream RTSP")

            self.cap = cap
            self.log.log("INFO", "RTSP OK.", self.cam_id)
            return True

        except Exception as e:
            self.log.log("WARN", f"Falha RTSP: {e}", self.cam_id)
            return False


    def _detect(self, frame_bgr):
        start_inf = time.time()
        h, w = frame_bgr.shape[:2]
        blob = cv2.dnn.blobFromImage(frame_bgr, 1/255.0, (self.input_size, self.input_size), swapRB=True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        inf_time = time.time() - start_inf

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
                    x = int(cx - bw/2)
                    y = int(cy - bh/2)
                    boxes.append([x, y, bw, bh])
                    confs.append(conf)
                    cids.append(cid)

        idxs = cv2.dnn.NMSBoxes(boxes, confs, self.conf_th, self.nms_th)
        f_boxes, f_confs, f_cids = [], [], []
        if len(idxs) > 0:
            for i in idxs.flatten():
                f_boxes.append(boxes[i])
                f_confs.append(confs[i])
                f_cids.append(cids[i])
        inf_time = time.time() - start_inf
        return f_boxes, f_confs, f_cids, inf_time

    def _draw_boxes(self, frame_bgr, boxes, confs, cids):
        out = frame_bgr.copy()
        for i, (x, y, bw, bh) in enumerate(boxes):
            cid = cids[i]
            conf = confs[i]
            name = self.classes[cid] if self.classes and cid < len(self.classes) else str(cid)
            cv2.rectangle(out, (x, y), (x + bw, y + bh), (0, 255, 255), 2)
            cv2.putText(out, f"{name.upper()} {conf:.0%}", (x, max(20, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
        return out

    def _person_present(self, cids):
        return 0 in cids  # COCO: person=0

    def _save_and_notify(self, frame_bgr_with_boxes, event_uid: str, shot_idx: int, person_count: int, conf_avg: float):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_uid = (event_uid or "evt").replace(":", "-").replace("/", "-")
        filename = f"{ts}_CAM{self.cam_id}_EVT{safe_uid}_S{shot_idx}.jpg"

        path = self.foto_dir / filename
        cv2.imwrite(str(path), frame_bgr_with_boxes)

        self.log.log(
            "INFO",
            "SHOT | "
            f"evt={self._event_uid} | shot={shot_idx}/{self.photos_per_event} | "
            f"pessoas={person_count} | conf_avg={conf_avg:.2f} | "
            f"arquivo={filename} | v{APP_VERSION}",
            self.cam_id
        )


        if self.photo_callback:
            try:
                self.photo_callback(self.cam_id, str(path), ts, event_uid, shot_idx)
            except Exception as e:
                self.log.log("ERROR", f"Erro no callback de foto: {e}", self.cam_id)

        # Telegram: continua enviando foto em detections/all (start/stop ficam na UI)
        if self.telegram_mode in ("all", "detections") and self.telegram.enabled:
            caption = f"DETECCAO PESSOA | CAM{self.cam_id} | pessoas={person_count} | conf={conf_avg:.0%} | v{APP_VERSION}"
            ok = self.telegram.enviar_foto(str(path), caption)
            if ok:
                self.log.log("INFO", "Foto enviada Telegram.", self.cam_id)
            else:
                self.log.log("WARN", "Falha ao enviar foto Telegram.", self.cam_id)

    # -------- Soft reconnect (watchdog) --------
    def request_soft_reconnect(self, reason: str = "watchdog"):
        self._pending_reconnect_reason = reason
        self.reconnect_event.set()

    def _soft_reconnect_now(self, reason: str):
        now = datetime.now().timestamp()
        if (now - float(self._last_soft_reconnect_ts or 0.0)) < 5.0:
            return False

        self._last_soft_reconnect_ts = now
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
            self.last_frame_ts = 0.0
            self.log.log("INFO", "Soft reconnect OK.", self.cam_id)
            return True

        self.log.log("ERROR", "Soft reconnect falhou.", self.cam_id)
        return False

    def stop(self):
         self.running = False

    def stop(self):
    # Só sinaliza para sair do loop.
    # NÃO chama release aqui pra não colidir com cap.read()
        self.running = False


    def run(self):
        self.running = True
        try:
            # 1) Conectar (respeitando stop)
            while self.running and (not self._connect()):
                self.log.log("WARN", "Não conectou RTSP. Tentando novamente em 2s...", self.cam_id)
                time.sleep(2.0)
            # RTSP OK -> loga config efetiva
            self._log_detector_config()
            frame_count = 0
            start_time = time.time()

            # 2) Loop principal
            while self.running:
                # watchdog solicitou soft reconnect
                if self.reconnect_event.is_set():
                    self.reconnect_event.clear()
                    reason = getattr(self, "_pending_reconnect_reason", "watchdog")
                    self._soft_reconnect_now(reason)

                # leitura segura
                ret, frame, err = self._safe_read()
                if err:
                    self.log.log("WARN", f"Falha em cap.read() ({err}). Tentando recuperar...", self.cam_id)

                # frame inválido => backoff + reconnect
                if (not ret) or (frame is None) or (not hasattr(frame, "size")) or (frame.size == 0):
                    self._bad_reads += 1

                    if self._bad_reads in (1, 5, 15) or (self._bad_reads % 30 == 0):
                        self.log.log("WARN", f"Frame falhou ({self._bad_reads}). Tentando recuperar...", self.cam_id)

                    now_ts = datetime.now().timestamp()
                    if (now_ts - self._last_reconnect_try) >= self._reconnect_backoff_s:
                        self._last_reconnect_try = now_ts

                        # reconecta (a própria thread faz release)
                        try:
                            if self.cap is not None:
                                self.cap.release()
                        except Exception as e:
                            self.log.log("WARN", f"Erro ao liberar cap durante reconnect: {e}", self.cam_id)

                        ok = self._connect()
                        if ok:
                            self.log.log("INFO", "Reconectou após falha de frame.", self.cam_id)
                            self._bad_reads = 0
                            self._reconnect_backoff_s = 2.0
                        else:
                            self._reconnect_backoff_s = min(self._max_backoff_s, self._reconnect_backoff_s * 1.5)

                    time.sleep(0.05)
                    continue

                # frame OK
                self._bad_reads = 0
                self._reconnect_backoff_s = 2.0

                self.last_frame_ts = datetime.now().timestamp()
                frame_count += 1
                now = self.last_frame_ts

                # descarta frame "lixo"
                if frame.std() < 5.0:
                    continue

                # detecção
                boxes, confs, cids, inf_time = self._detect(frame)
                self.inf_times.append(inf_time)
                frame_draw = self._draw_boxes(frame, boxes, confs, cids)
     
                if boxes and (not self._person_present(cids)):
                    now_ts = time.time()

                    # evita spam de log
                    if (now_ts - getattr(self, "_last_nonperson_log", 0.0)) > 5.0:
                        self._last_nonperson_log = now_ts

                        conf_avg = (sum(confs) / len(confs)) if confs else 0.0

                        self.log.log(
                            "INFO",
                            "MOVIMENTO SEM PESSOA | "
                            f"boxes={len(boxes)} | "
                            f"conf_avg={conf_avg:.2f} | "
                            f"classes_detectadas={set(cids)} | "
                            f"conf_th={self.conf_th:.2f} | nms_th={self.nms_th:.2f} | "
                            f"cooldown={self.cooldown_s:.2f}s | v{APP_VERSION}",
                            self.cam_id
                        )


                # evento apenas se pessoa
                if boxes and self._person_present(cids):
                    if (now - self._last_event_time) >= self.cooldown_s and self._pending_shots <= 0:
                        evt_ts = int(now)  # base temporal do evento
                        self._event_uid = f"{self.cam_id}-{evt_ts}-{self.detections_total+1}"  # único
                        self._pending_shots = int(max(1, self.photos_per_event))
                        self._last_event_time = now
                        self._last_shot_time = 0.0
                        person_count = sum(1 for cid in cids if cid == 0)
                        conf_avg = (sum(confs) / len(confs)) if confs else 0.0

                        # extras úteis
                        best_conf = max(confs) if confs else 0.0
                        total_boxes = len(boxes)

                        self.log.log(
                            "WARN",
                            "EVENTO MOVIMENTO/DETECCAO | "
                            f"evt={self._event_uid} | pessoas={person_count} | boxes={total_boxes} | "
                            f"conf_avg={conf_avg:.2f} | conf_max={best_conf:.2f} | "
                            f"cooldown={self.cooldown_s:.2f}s | conf_th={self.conf_th:.2f} | nms_th={self.nms_th:.2f} | "
                            f"photos={self._pending_shots} | min_shot_interval={self._min_shot_interval:.2f}s | v{APP_VERSION}",
                            self.cam_id
                        )


                # fotos pendentes
                if self._pending_shots > 0:
                    if (now - self._last_shot_time) >= self._min_shot_interval:
                        person_count = sum(1 for cid in cids if cid == 0)
                        conf_avg = (sum(confs) / len(confs)) if confs else 0.0
                        shot_idx = (int(self.photos_per_event) - int(self._pending_shots) + 1)
                        self._save_and_notify(frame_draw, self._event_uid, shot_idx, person_count, conf_avg)

                        self._pending_shots -= 1
                        self._last_shot_time = now

                # UI callback
                if self.frame_callback:
                    try:
                        self.frame_callback(self.cam_id, frame_draw)
                    except Exception as e:
                        self.log.log("ERROR", f"Erro no callback de frame: {e}", self.cam_id)

                if frame_count % 200 == 0:
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed if elapsed > 0 else 0
                    if PSUTIL_AVAILABLE:
                        cpu_percent = psutil.cpu_percent(interval=None)
                        ram_percent = psutil.virtual_memory().percent
                    else:
                        cpu_percent = 0.0
                        ram_percent = 0.0
                    avg_inf = sum(self.inf_times) / len(self.inf_times) if self.inf_times else 0
                    gpu_info = "CUDA" if cv2.cuda.getCudaEnabledDeviceCount() > 0 else "CPU"
                    self.last_performance = {'fps': fps, 'cpu': cpu_percent, 'ram': ram_percent, 'inf_time': avg_inf, 'gpu': gpu_info}
                    self.log.log("INFO", f"PERFORMANCE | Frames: {frame_count} | FPS: {fps:.2f} | CPU: {cpu_percent:.1f}% | RAM: {ram_percent:.1f}% | InfTime: {avg_inf:.3f}s | GPU: {gpu_info} | v{APP_VERSION}", self.cam_id)
                    self.inf_times.clear()

        finally:
            # 3) Cleanup garantido: aqui é o lugar seguro de liberar o cap
            try:
                if self.cap is not None:
                    self.cap.release()
            except Exception as e:
                self.log.log("WARN", f"Erro ao liberar cap no cleanup: {e}", self.cam_id)

            self.log.log("INFO", "Thread encerrada.", self.cam_id)



# ----------------------------- UI -----------------------------
class InterfaceGrafica:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"AlertaIntruso v{APP_VERSION} — 4 Câmeras RTSP (YOLO)")
        self.root.geometry("1400x850")

        self.config_file = Path("config.ini")
        self.config = configparser.ConfigParser()

        

        self.log = LogManager("log.txt", max_size_mb=1)
        self.log.add_callback(lambda line: self.ui_log_queue.put(line))
        self.log.log("INFO",f"Inicializando sistema | AlertaIntruso v{APP_VERSION} | Python {platform.python_version()} | OpenCV {cv2.__version__}"
)

        # Capturar logs do OpenCV (incluindo FFmpeg)
        try:
            cv2.setLogCallback(lambda level, msg: self.log.log("INFO", f"OpenCV [{level}]: {msg.strip()}"))
        except AttributeError:
            self.log.log("WARN", "cv2.setLogCallback não disponível nesta versão do OpenCV. Logs do OpenCV não serão capturados.")

        # Capturar stderr para logs de FFmpeg não capturados pelo OpenCV
        self.old_stderr = sys.stderr
        r, w = os.pipe()
        self.stderr_r = os.fdopen(r, 'r')
        sys.stderr = os.fdopen(w, 'w')
        threading.Thread(target=self._read_stderr, daemon=True).start()



        self._load_or_create_config()

        # Telegram
        token = self.config["TELEGRAM"].get("bot_token", "")
        chat_id = self.config["TELEGRAM"].get("chat_id", "")
        self.telegram = TelegramBot(token, chat_id, self.log)

        # Detectors
        self.detectors = {}     # cam_id -> RTSPObjectDetector
        self.threads = {}       # cam_id -> Thread
        self.running = False

        # Queues
        self.frame_queue = queue.Queue()
        self.photo_queue = queue.Queue()
        self.log_queue = queue.Queue()


        # Watchdog settings
        self.watchdog_interval_ms = 2000
        self.watchdog_no_frame_s = 12.0
        self.watchdog_restart_backoff_s = 10.0
        self._last_restart_ts = {}  # cam_id -> ts

        # Daily restart
        self._last_daily_restart_date = None  # "YYYY-MM-DD"

        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # ABA VÍDEO
        self.frame_video = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_video, text="Vídeo (Mosaico 2x2)")
        self._build_video_mosaic()

        # ABA CONFIG
        self.frame_config = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_config, text="Config")
        self._build_config_tab()

        # ABA FOTOS
        self.frame_fotos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_fotos, text="Fotos")
        self._build_photos_tab()

        # ABA LOGS
        self.frame_logs = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_logs, text="Logs")
        self._build_logs_tab()

        self._load_logs_tail()

        self.root.after(1000, self._update_performance)

        self._process_queues()
        self.log.log("INFO", f"Interface pronta v{APP_VERSION}")

        # Autostart
        self.root.after(600, self.start_system)

        # Watchdog loop + daily restart loop
        self.root.after(self.watchdog_interval_ms, self._supervise_cameras)
        self.root.after(1500, self._daily_restart_tick)

        # Fechamento
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _read_stderr(self):
        try:
            for line in self.stderr_r:
                self.log.log("WARN", f"STDERR: {line.strip()}")
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
            },
            "TELEGRAM": {
                "bot_token": "",
                "chat_id": "",
                "alert_mode": "detections",  # all | detections | none
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
        # Camera enable + RTSP
        self.config["CAM1"]["enabled"] = str(bool(self.var_cam1.get()))
        self.config["CAM2"]["enabled"] = str(bool(self.var_cam2.get()))
        self.config["CAM3"]["enabled"] = str(bool(self.var_cam3.get()))
        self.config["CAM4"]["enabled"] = str(bool(self.var_cam4.get()))

        self.config["CAM1"]["rtsp_url"] = self.e_rtsp1.get().strip()
        self.config["CAM2"]["rtsp_url"] = self.e_rtsp2.get().strip()
        self.config["CAM3"]["rtsp_url"] = self.e_rtsp3.get().strip()
        self.config["CAM4"]["rtsp_url"] = self.e_rtsp4.get().strip()

        # Detector
        self.config["DETECTOR"]["cooldown"] = self.sp_cooldown.get().strip()
        self.config["DETECTOR"]["confidence_threshold"] = self.sp_conf.get().strip()
        self.config["DETECTOR"]["nms_threshold"] = self.sp_nms.get().strip()
        self.config["DETECTOR"]["photos_per_event"] = self.sp_photos.get().strip()

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

        # Telegram
        self.config["TELEGRAM"]["bot_token"] = self.e_token.get().strip()
        self.config["TELEGRAM"]["chat_id"] = self.e_chat.get().strip()
        self.config["TELEGRAM"]["alert_mode"] = self.cb_alert.get().strip()

        with open(self.config_file, "w", encoding="utf-8") as f:
            self.config.write(f)

    # ---------------- UI BUILD ----------------
    def _build_video_mosaic(self):
        self.frame_video.columnconfigure(0, weight=1, uniform="cam")
        self.frame_video.columnconfigure(1, weight=1, uniform="cam")
        self.frame_video.rowconfigure(0, weight=1, uniform="cam")
        self.frame_video.rowconfigure(1, weight=1, uniform="cam")

        self.cam_cells = {}
        self.cam_labels = {}

        positions = {1: (0, 0), 2: (0, 1), 3: (1, 0), 4: (1, 1)}
        for cam_id, (r, c) in positions.items():
            cell = ttk.Frame(self.frame_video)
            cell.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
            cell.grid_propagate(False)

            header = ttk.Frame(cell)
            header.pack(fill="x")
            ttk.Label(header, text=f"CAM{cam_id}", font=("Arial", 10, "bold")).pack(side="left", padx=6, pady=2)

            lbl = tk.Label(cell, bg="black")
            lbl.pack(fill="both", expand=True)

            self.cam_cells[cam_id] = cell
            self.cam_labels[cam_id] = lbl

    def _build_config_tab(self):
        wrap = ttk.Frame(self.frame_config)
        wrap.pack(fill="both", expand=True, padx=10, pady=10)

        # RTSP + Enable
        rt = ttk.LabelFrame(wrap, text="Câmeras (ativar/desativar) + RTSP", padding=10)
        rt.pack(fill="x", pady=8)

        def cam_row(row, label, var_enable, entry):
            ttk.Checkbutton(rt, text=label, variable=var_enable).grid(row=row, column=0, sticky="w", padx=4)
            entry.grid(row=row, column=1, padx=6, pady=4, sticky="we")

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

        # Detector
        det = ttk.LabelFrame(wrap, text="Detector", padding=10)
        det.pack(fill="x", pady=8)

        ttk.Label(det, text="Cooldown (s):").grid(row=0, column=0, sticky="w")
        self.sp_cooldown = ttk.Spinbox(det, from_=1, to=30, width=8)
        self.sp_cooldown.grid(row=0, column=1, padx=6, pady=4, sticky="w")
        self.sp_cooldown.set(self.config["DETECTOR"].get("cooldown", "2"))

        ttk.Label(det, text="Confiança:").grid(row=0, column=2, sticky="w")
        self.sp_conf = ttk.Spinbox(det, from_=0.2, to=0.95, increment=0.05, width=8)
        self.sp_conf.grid(row=0, column=3, padx=6, pady=4, sticky="w")
        self.sp_conf.set(self.config["DETECTOR"].get("confidence_threshold", "0.5"))

        ttk.Label(det, text="NMS:").grid(row=0, column=4, sticky="w")
        self.sp_nms = ttk.Spinbox(det, from_=0.2, to=0.95, increment=0.05, width=8)
        self.sp_nms.grid(row=0, column=5, padx=6, pady=4, sticky="w")
        self.sp_nms.set(self.config["DETECTOR"].get("nms_threshold", "0.4"))

        ttk.Label(det, text="Fotos por evento:").grid(row=0, column=6, sticky="w")
        self.sp_photos = ttk.Spinbox(det, from_=1, to=10, width=6)
        self.sp_photos.grid(row=0, column=7, padx=6, pady=4, sticky="w")
        self.sp_photos.set(self.config["DETECTOR"].get("photos_per_event", "2"))

        # Classes
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

        ttk.Checkbutton(cls, text="person", variable=self.var_person).grid(row=0, column=0, sticky="w", padx=6, pady=2)
        ttk.Checkbutton(cls, text="car", variable=self.var_car).grid(row=0, column=1, sticky="w", padx=6, pady=2)
        ttk.Checkbutton(cls, text="bus", variable=self.var_bus).grid(row=0, column=2, sticky="w", padx=6, pady=2)
        ttk.Checkbutton(cls, text="truck", variable=self.var_truck).grid(row=0, column=3, sticky="w", padx=6, pady=2)
        ttk.Checkbutton(cls, text="motorcycle", variable=self.var_motorcycle).grid(row=0, column=4, sticky="w", padx=6, pady=2)
        ttk.Checkbutton(cls, text="bicycle", variable=self.var_bicycle).grid(row=0, column=5, sticky="w", padx=6, pady=2)
        ttk.Checkbutton(cls, text="dog", variable=self.var_dog).grid(row=1, column=0, sticky="w", padx=6, pady=2)
        ttk.Checkbutton(cls, text="cat", variable=self.var_cat).grid(row=1, column=1, sticky="w", padx=6, pady=2)
        ttk.Checkbutton(cls, text="bird", variable=self.var_bird).grid(row=1, column=2, sticky="w", padx=6, pady=2)
        ttk.Checkbutton(cls, text="horse", variable=self.var_horse).grid(row=1, column=3, sticky="w", padx=6, pady=2)

        # Telegram
        tg = ttk.LabelFrame(wrap, text="Telegram (persistente em config.ini)", padding=10)
        tg.pack(fill="x", pady=8)

        ttk.Label(tg, text="Bot Token:").grid(row=0, column=0, sticky="w")
        self.e_token = ttk.Entry(tg, width=60); self.e_token.grid(row=0, column=1, padx=6, pady=4, sticky="w")
        self.e_token.insert(0, self.config["TELEGRAM"].get("bot_token", ""))

        ttk.Label(tg, text="Chat ID:").grid(row=1, column=0, sticky="w")
        self.e_chat = ttk.Entry(tg, width=60); self.e_chat.grid(row=1, column=1, padx=6, pady=4, sticky="w")
        self.e_chat.insert(0, self.config["TELEGRAM"].get("chat_id", ""))

        ttk.Label(tg, text="Alertas (fotos):").grid(row=2, column=0, sticky="w")
        self.cb_alert = ttk.Combobox(tg, values=["all", "detections", "none"], state="readonly", width=12)
        self.cb_alert.grid(row=2, column=1, padx=6, pady=4, sticky="w")
        self.cb_alert.set(self.config["TELEGRAM"].get("alert_mode", "detections"))

        # Controles
        ctrl = ttk.Frame(wrap)
        ctrl.pack(fill="x", pady=10)

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
        self.text_logs = scrolledtext.ScrolledText(self.frame_logs, wrap=tk.WORD, font=("Courier", 9))
        self.text_logs.pack(fill="both", expand=True, padx=6, pady=6)
        ttk.Button(self.frame_logs, text="Limpar", command=lambda: self.text_logs.delete("1.0", tk.END)).pack(pady=4)

    def _build_performance_tab(self):
        self.perf_labels = {}
        for cam in range(1, 5):
            ttk.Label(self.frame_performance, text=f"Câmera {cam}", font=("Arial", 12, "bold")).grid(row=cam-1, column=0, padx=10, pady=5, sticky="w")
            self.perf_labels[cam] = {
                'fps': ttk.Label(self.frame_performance, text="FPS: --", font=("Arial", 10)),
                'cpu': ttk.Label(self.frame_performance, text="CPU: --%", font=("Arial", 10)),
                'ram': ttk.Label(self.frame_performance, text="RAM: --%", font=("Arial", 10)),
                'inf_time': ttk.Label(self.frame_performance, text="InfTime: --s", font=("Arial", 10)),
                'gpu': ttk.Label(self.frame_performance, text="GPU: --", font=("Arial", 10)),
            }
            col = 1
            for key in ['fps', 'cpu', 'ram', 'inf_time', 'gpu']:
                self.perf_labels[cam][key].grid(row=cam-1, column=col, padx=10, pady=2, sticky="w")
                col += 1
        # Global
        ttk.Label(self.frame_performance, text="Sistema", font=("Arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.global_labels = {
            'cpu': ttk.Label(self.frame_performance, text="CPU: --%", font=("Arial", 10)),
            'ram': ttk.Label(self.frame_performance, text="RAM: --%", font=("Arial", 10)),
        }
        self.global_labels['cpu'].grid(row=4, column=1, padx=10, pady=2, sticky="w")
        self.global_labels['ram'].grid(row=4, column=2, padx=10, pady=2, sticky="w")

    def _update_performance(self):
        try:
            global_cpu = 0.0
            global_ram = 0.0
            count = 0
            for cam in range(1, 5):
                if cam in self.detectors and hasattr(self.detectors[cam], 'last_performance'):
                    perf = self.detectors[cam].last_performance
                    fps = perf.get('fps', 0)
                    cpu = perf.get('cpu', 0)
                    ram = perf.get('ram', 0)
                    inf_time = perf.get('inf_time', 0)
                    gpu = perf.get('gpu', 'CPU')
                    
                    # Update labels with color
                    self.perf_labels[cam]['fps'].config(text=f"FPS: {fps:.2f}", foreground='red' if fps < 10 else 'green')
                    self.perf_labels[cam]['cpu'].config(text=f"CPU: {cpu:.1f}%", foreground='red' if cpu > 80 else 'green')
                    self.perf_labels[cam]['ram'].config(text=f"RAM: {ram:.1f}%", foreground='red' if ram > 80 else 'green')
                    self.perf_labels[cam]['inf_time'].config(text=f"InfTime: {inf_time:.3f}s", foreground='red' if inf_time > 0.1 else 'green')
                    self.perf_labels[cam]['gpu'].config(text=f"GPU: {gpu}", foreground='blue')
                    
                    global_cpu += cpu
                    global_ram += ram
                    count += 1
                else:
                    for key in self.perf_labels[cam]:
                        self.perf_labels[cam][key].config(text=f"{key.upper()}: --", foreground='gray')
            
            if count > 0:
                global_cpu /= count
                global_ram /= count
            self.global_labels['cpu'].config(text=f"CPU: {global_cpu:.1f}%", foreground='red' if global_cpu > 80 else 'green')
            self.global_labels['ram'].config(text=f"RAM: {global_ram:.1f}%", foreground='red' if global_ram > 80 else 'green')
        except Exception as e:
            self.log.log("ERROR", f"Erro ao atualizar performance: {e}")
        
        self.root.after(1000, self._update_performance)

    # ---------------- LOG UI ----------------
    def _log_to_ui(self, line: str):
        try:
            self.log_queue.put_nowait(line)
        except Exception:
            pass

    def _load_logs_tail(self):
        lf = Path("log.txt")
        if not lf.exists():
            return
        try:
            with open(lf, "r", encoding="utf-8") as f:
                lines = f.readlines()[-200:]
            for ln in lines:
                self.text_logs.insert(tk.END, ln)
            self.text_logs.see(tk.END)
        except Exception:
            pass

    # ---------------- QUEUES ----------------
    def _process_queues(self):
        # frames
        try:
            while True:
                cam_id, frame_bgr = self.frame_queue.get_nowait()
                self._update_cam_frame(cam_id, frame_bgr)
        except queue.Empty:
            pass

        # fotos
        try:
            while True:
                cam_id, foto_path, ts, event_uid, shot_idx = self.photo_queue.get_nowait()
                self._add_thumbnail(cam_id, foto_path, ts, event_uid, shot_idx)

        except queue.Empty:
            pass

        # logs (AGORA SEGURO)
        try:
            while True:
                line = self.log_queue.get_nowait()
                try:
                    self.text_logs.insert(tk.END, line)
                    self.text_logs.see(tk.END)
                except Exception:
                    pass
        except queue.Empty:
            pass

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

    # ---------------- THUMBNAILS ----------------
    def _parse_thumb_dt(self, ts: str) -> datetime:
        try:
            return datetime.strptime(ts, "%Y%m%d_%H%M%S")
        except Exception:
            return datetime.now()

    def _get_or_create_group_by_uid(self, event_uid: str, dt: datetime):
        if not hasattr(self, "thumb_groups_by_uid"):
            self.thumb_groups_by_uid = {}   # uid -> group
            self.thumb_groups_order = []    # uids na ordem que apareceram

        uid = (event_uid or "evt")
        if uid in self.thumb_groups_by_uid:
            g = self.thumb_groups_by_uid[uid]
            g["last_dt"] = dt
            return g

        # novo grupo = nova linha
        row = len(self.thumb_groups_order)
        self.thumb_groups_order.append(uid)

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

    def _add_thumbnail(self, cam_id: int, foto_path: str, ts: str, event_uid: str, shot_idx: int):
        try:
            dt = self._parse_thumb_dt(ts)
            group = self._get_or_create_group_by_uid(event_uid, dt)

            img = Image.open(foto_path)
            img.thumbnail((220, 160))
            imgtk = ImageTk.PhotoImage(img)

            col = int(group["next_col"])

            cell = ttk.Frame(group["thumbs_frame"])
            cell.grid(row=0, column=col, padx=8, pady=6, sticky="w")

            img_label = tk.Label(cell, image=imgtk, cursor="hand2")
            img_label.image = imgtk
            img_label.pack()
            img_label.bind("<Button-1>", lambda e, p=foto_path: self._open_photo(p))

            ttk.Label(
                cell,
                text=f"CAM{cam_id} • S{shot_idx} • {dt.strftime('%H:%M:%S')}",
                font=("Arial", 9)
            ).pack(pady=(4, 0))

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
        self.telegram.enviar_mensagem(f"SISTEMA INICIADO v{APP_VERSION} | cams_ativas={active_count}")

    def _send_telegram_system_stop(self, total_detections: int):
        if not self.telegram.enabled:
            return
        mode = self.config["TELEGRAM"].get("alert_mode", "detections")
        if mode == "none":
            return
        self.telegram.enviar_mensagem(f"SISTEMA ENCERRADO v{APP_VERSION} | deteccoes={total_detections}")

    def start_system(self):
        if self.running:
            return

        # atualizar Telegram do config
        token = self.config["TELEGRAM"].get("bot_token", "")
        chat_id = self.config["TELEGRAM"].get("chat_id", "")
        self.telegram = TelegramBot(token, chat_id, self.log)

        # parar qualquer resquício
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
            det.photo_callback = lambda cid, path, ts, event_uid, shot_idx, q=self.photo_queue: q.put((cid, path, ts, event_uid, shot_idx))


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

    def stop_system(self, silent=False):
        total_detections = 0
        for cam_id, det in list(self.detectors.items()):
            try:
                total_detections += int(getattr(det, "detections_total", 0))
            except Exception:
                pass

        for cam_id, det in list(self.detectors.items()):
            try:
                det.stop()
            except Exception:
                pass

        for cam_id, th in list(self.threads.items()):
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

        # limpa refs
        self.detectors.clear()
        self.threads.clear()

    # ---------------- RESTART HELPERS ----------------
    def _restart_single_camera(self, cam_id: int, reason: str = ""):
        now = datetime.now().timestamp()
        last = float(self._last_restart_ts.get(cam_id, 0.0) or 0.0)
        if (now - last) < self.watchdog_restart_backoff_s:
            return

        self._last_restart_ts[cam_id] = now

        self.log.log("WARN", f"Hard restart câmera ({reason})", cam_id)

        # parar detector atual
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

        # recriar se ainda estiver habilitada
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

        # telegram atual
        token = self.config["TELEGRAM"].get("bot_token", "")
        chat_id = self.config["TELEGRAM"].get("chat_id", "")
        self.telegram = TelegramBot(token, chat_id, self.log)

        try:
            new_det = RTSPObjectDetector(cam_id, url, self.log, self.telegram)
            self._apply_detector_config(new_det)
            new_det.frame_callback = lambda cid, fr, q=self.frame_queue: q.put((cid, fr))
            new_det.photo_callback = lambda cid, path, ts, q=self.photo_queue: q.put((cid, path, ts))

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

    # ---------------- SAVE/RELOAD ----------------
    def save_and_restart(self):
        try:
            self._save_config()
            self.log.log("INFO", "Config salva. Reiniciando...")
            self.restart_system(reason="config alterada")
        except Exception as e:
            self.log.log("ERROR", f"Falha ao salvar config: {e}")
            messagebox.showerror("Erro", str(e))

    def reload_and_restart(self):
        try:
            self._load_or_create_config()
            self.log.log("INFO", "Config recarregada. Reiniciando...")
            self.restart_system(reason="config recarregada")
        except Exception as e:
            self.log.log("ERROR", f"Falha ao recarregar config: {e}")
            messagebox.showerror("Erro", str(e))


    # ---------------- WATCHDOG ----------------
    def _supervise_cameras(self):
        try:
            if self.running and self.detectors:
                now = datetime.now().timestamp()

                for cam_id, det in list(self.detectors.items()):
                    last = float(getattr(det, "last_frame_ts", 0.0) or 0.0)
                    if last <= 0.0:
                        # ainda não recebeu frame; dá um tempo após start
                        continue

                    delta = now - last
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

            # reinicia só 1x por dia, exatamente na virada (00:00)
            if now.hour == 0 and now.minute == 0:
                if self._last_daily_restart_date != today:
                    self._last_daily_restart_date = today
                    if self.running:
                        self.restart_system(reason="reinicio diario 00:00")
                    else:
                        self.log.log("INFO", "Reinicio diário 00:00 (sistema estava parado).")
        finally:
            # checa a cada ~20s
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

    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()
