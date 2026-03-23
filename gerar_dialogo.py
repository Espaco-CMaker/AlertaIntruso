import os
import subprocess

# File paths
input_file = r"d:\IAGenMaster\2026\CMaker\Projetos\Alerta_de_Intruso\REFLEXOES_IA_CRIADOR.md"
output_file = r"d:\IAGenMaster\2026\CMaker\Projetos\Alerta_de_Intruso\Dialogo_Criador_IA.mp3"
temp_dir = r"d:\IAGenMaster\2026\CMaker\Projetos\Alerta_de_Intruso\temp_audio"

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Read the markdown file
with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

dialogues = []
lines = text.split('\n')
current_speaker = None
current_text = []

for line in lines:
    line = line.strip()
    if line.startswith("> **Criador:**"):
        if current_speaker and current_text:
            dialogues.append((current_speaker, " ".join(current_text)))
        current_speaker = "criador"
        current_text = []
    elif line.startswith("> **Máquina (Antigravity):**"):
        if current_speaker and current_text:
            dialogues.append((current_speaker, " ".join(current_text)))
        current_speaker = "maquina"
        current_text = []
    elif line.startswith(">") and current_speaker:
        cleaned = line[1:].strip()
        cleaned = cleaned.replace("*", "").replace('"', '').replace("'", "")
        if cleaned:
            # For edge-tts it's better to translate newlines to sentences
            current_text.append(cleaned)

if current_speaker and current_text:
    dialogues.append((current_speaker, " ".join(current_text)))

print(f"Total dialogues extracted: {len(dialogues)}")

audio_files = []

voice_criador = "pt-BR-AntonioNeural"
pitch_criador = "-10Hz"
rate_criador = "-5%"

voice_maquina = "pt-BR-FranciscaNeural"
pitch_maquina = "+10Hz"
rate_maquina = "+5%"

for i, (speaker, speech) in enumerate(dialogues):
    temp_mp3 = os.path.join(temp_dir, f"part_{i:03d}.mp3")
    temp_txt = os.path.join(temp_dir, f"part_{i:03d}.txt")
    audio_files.append(temp_mp3)
    
    with open(temp_txt, 'w', encoding='utf-8') as f:
        f.write(speech)

    if speaker == "criador":
        cmd = [
            "edge-tts",
            "--voice", voice_criador,
            f"--pitch={pitch_criador}",
            f"--rate={rate_criador}",
            "-f", temp_txt,
            "--write-media", temp_mp3
        ]
    else:
        cmd = [
            "edge-tts",
            "--voice", voice_maquina,
            f"--pitch={pitch_maquina}",
            f"--rate={rate_maquina}",
            "-f", temp_txt,
            "--write-media", temp_mp3
        ]
    print(f"[{i}] {speaker}: {speech[:60]}...")
    subprocess.run(cmd, check=True)

# Combine audio files
print("Combining audio files...")
file_list_path = os.path.join(temp_dir, "file_list.txt")
with open(file_list_path, 'w', encoding='utf-8') as f:
    for audio in audio_files:
        # Use forward slashes for ffmpeg!
        forward_slash_path = os.path.abspath(audio).replace('\\', '/')
        f.write(f"file '{forward_slash_path}'\n")

ffmpeg_cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", file_list_path, "-c", "copy", output_file
]
subprocess.run(ffmpeg_cmd, check=True)

print(f"Dialogue saved to {output_file}")

# Clean up
try:
    for i in range(len(dialogues)):
        os.remove(os.path.join(temp_dir, f"part_{i:03d}.mp3"))
        os.remove(os.path.join(temp_dir, f"part_{i:03d}.txt"))
    os.remove(file_list_path)
    os.rmdir(temp_dir)
except Exception as e:
    print("Warning during cleanup:", e)
