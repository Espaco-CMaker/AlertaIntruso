#!/usr/bin/env python3
"""
Utilitário para atualizar versão em todos os arquivos do projeto.
Lê APP_VERSION de AlertaIntruso Claude+GPT.py e atualiza:
- Cabeçalho do docstring
- Changelog
- Data
- Commits no Git
"""

import re
import subprocess
from pathlib import Path
from datetime import datetime

MAIN_FILE = Path("AlertaIntruso Claude+GPT.py")

def get_current_version():
    """Extrai APP_VERSION do arquivo principal"""
    with open(MAIN_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'APP_VERSION = ["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return None

def get_version_parts(version):
    """Extrai major.minor.patch da versão"""
    parts = version.split('.')
    return {'major': parts[0], 'minor': parts[1], 'patch': parts[2] if len(parts) > 2 else '0'}

def update_header_and_metadata():
    """Atualiza cabeçalho do docstring e metadados"""
    version = get_current_version()
    if not version:
        print("❌ Não foi possível extrair APP_VERSION")
        return False
    
    with open(MAIN_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Atualizar cabeçalho do docstring: Versão
    content = re.sub(
        r'Versão:\s+[\d.]+[^\n]*',
        f'Versão:         {version}',
        content
    )
    
    # Atualizar cabeçalho: Data
    content = re.sub(
        r'Data:\s+\d{2}/\d{2}/\d{4}',
        f'Data:           {today}',
        content
    )
    
    # Atualizar cabeçalho: base version
    parts = get_version_parts(version)
    prev_patch = str(int(parts['patch']) - 1) if int(parts['patch']) > 0 else '0'
    prev_version = f"{parts['major']}.{parts['minor']}.{prev_patch}"
    
    content = re.sub(
        r'\(base v[\d.]+\)',
        f'(base v{prev_version})',
        content,
        count=1  # Apenas na primeira ocorrência (cabeçalho)
    )
    
    with open(MAIN_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Cabeçalho atualizado: v{version} ({today})")
    return True

def create_git_commit(changelog_entry: str):
    """Cria commit no Git com a versão atualizada"""
    try:
        version = get_current_version()
        
        # git add .
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        print("✅ Arquivos adicionados ao staging")
        
        # git commit
        commit_msg = f"v{version} - {changelog_entry}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
        print(f"✅ Commit criado: {commit_msg}")
        
        # git push
        result = subprocess.run(['git', 'push'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Enviado para GitHub")
            return True
        else:
            print(f"⚠️ Erro ao fazer push: {result.stderr}")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no Git: {e}")
        return False

def update_version(changelog_entry: str = "Atualização de versão"):
    """Função principal de atualização"""
    version = get_current_version()
    
    if not version:
        print("❌ Não foi possível extrair APP_VERSION")
        return False
    
    print(f"\n📦 Atualizando para v{version}...")
    
    if update_header_and_metadata():
        create_git_commit(changelog_entry)
        print(f"\n✅ Versão {version} atualizada com sucesso!")
        return True
    
    return False

if __name__ == "__main__":
    import sys
    
    changelog = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Atualização"
    update_version(changelog)
