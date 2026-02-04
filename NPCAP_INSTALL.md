# Como Corrigir: "WARNING: No libpcap provider available"

## 📋 Sobre o Problema

O warning `WARNING: No libpcap provider available ! pcap won't be used` aparece quando:
- A biblioteca **Scapy** está instalada no Python, MAS
- O **Npcap** (driver de captura de rede para Windows) não está instalado no sistema

## 🎯 Impacto no AlertaIntruso

- ✅ O sistema **funciona normalmente** sem o Npcap
- ⚠️ O **bitrate real** não será capturado (será calculado internamente)
- 📊 A aba **Performance** mostrará bitrate estimado ao invés do valor real capturado via RTP

## 🔧 Como Corrigir (Windows)

### Passo 1: Baixar o Npcap

1. Acesse: **https://npcap.com/**
2. Clique em **"Download"** na página principal
3. Baixe a versão mais recente (ex: `npcap-1.79.exe`)

### Passo 2: Instalar o Npcap

1. Execute o instalador como **Administrador**
2. **IMPORTANTE**: Marque a opção:
   ```
   ☑ Install Npcap in WinPcap API-compatible Mode
   ```
3. Deixe as outras opções padrão
4. Clique em **"Install"**
5. Reinicie o computador se solicitado

### Passo 3: Verificar Instalação

Após instalar, execute o AlertaIntruso e verifique o log no início:

#### ✅ Com Npcap instalado corretamente:
```
INFO | Scapy DISPONÍVEL | Captura RTP ativa para bitrate real
```

#### ⚠️ Sem Npcap:
```
WARN | Scapy NÃO disponível | Bitrate calculado internamente (sem captura RTP)
```

#### ⚠️ Com Scapy mas sem Npcap:
```
WARN | Scapy instalado MAS libpcap NÃO disponível | SOLUÇÃO: Instale Npcap...
```

## 🐧 Linux / macOS

No Linux/macOS, o problema é diferente:

### Linux (Ubuntu/Debian):
```bash
sudo apt-get install libpcap-dev
pip install scapy
```

### Linux (Fedora/RHEL):
```bash
sudo dnf install libpcap-devel
pip install scapy
```

### macOS:
```bash
brew install libpcap
pip install scapy
```

## 📝 Notas Técnicas

1. **Scapy vs Npcap**: 
   - Scapy é a biblioteca Python
   - Npcap é o driver de baixo nível para captura de pacotes

2. **Compatibilidade WinPcap**:
   - Npcap substitui o antigo WinPcap (descontinuado)
   - Modo compatível garante funcionamento com Scapy

3. **Permissões**:
   - Npcap requer privilégios de administrador
   - Pode exigir reinicialização do Windows

4. **Firewall**:
   - Alguns firewalls podem bloquear captura de pacotes
   - Permita o AlertaIntruso no firewall se necessário

## 🔍 Diagnóstico Rápido

Execute este comando Python para testar:

```python
try:
    from scapy.all import sniff, get_if_list
    print("✅ Scapy OK")
    print(f"Interfaces: {get_if_list()}")
except ImportError:
    print("❌ Scapy não instalado: pip install scapy")
except Exception as e:
    print(f"⚠️ Scapy instalado mas problema: {e}")
    print("SOLUÇÃO: Instalar Npcap de https://npcap.com/")
```

## ❓ FAQ

**P: Preciso mesmo instalar o Npcap?**
R: Não é obrigatório. O sistema funciona sem ele, mas o bitrate será estimado.

**P: O Npcap é seguro?**
R: Sim. É desenvolvido pela Nmap Project e usado por milhões de usuários.

**P: Posso desinstalar depois?**
R: Sim. Use "Adicionar ou Remover Programas" do Windows.

**P: O warning vai sumir?**
R: Sim. Após instalar corretamente, o warning não aparecerá mais.

## 📚 Links Úteis

- Npcap Official: https://npcap.com/
- Scapy Documentation: https://scapy.readthedocs.io/
- GitHub Npcap: https://github.com/nmap/npcap
- WinPcap (antigo): https://www.winpcap.org/ (descontinuado)

---
**Última atualização**: 04/02/2026
**Versão AlertaIntruso**: 4.5.1+
