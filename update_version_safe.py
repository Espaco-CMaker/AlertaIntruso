#!/usr/bin/env python3
"""
Script para atualizar versão + validar + fazer commit automaticamente
Usa as validações do validate_documentation.py
"""

import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from validate_documentation import DocumentationValidator

MAIN_FILE = Path("AlertaIntruso Claude+GPT.py")
README_FILE = Path("README.md")
CHANGELOG_FILE = Path("CHANGELOG.md")

class VersionUpdater:
    def __init__(self, new_version: str):
        self.new_version = new_version
        self.validator = DocumentationValidator()
        self.changes = []

    def validate_version_format(self):
        """Valida formato de versão X.Y.Z"""
        if not re.match(r'^\d+\.\d+\.\d+$', self.new_version):
            print(f"❌ ERRO: Formato de versão inválido: {self.new_version}")
            print(f"   Use formato X.Y.Z (ex: 4.5.8)")
            return False
        return True

    def update_app_version(self):
        """Atualiza APP_VERSION no arquivo principal"""
        try:
            with open(MAIN_FILE, 'r', encoding='utf-8') as f:
                content = f.read()

            old_version = re.search(r'APP_VERSION = ["\']([^"\']+)["\']', content)
            if not old_version:
                print("❌ ERRO: APP_VERSION não encontrada")
                return False

            old_ver = old_version.group(1)
            content = re.sub(
                r'APP_VERSION = ["\'][^"\']+["\']',
                f'APP_VERSION = "{self.new_version}"',
                content
            )

            with open(MAIN_FILE, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ APP_VERSION atualizada: {old_ver} → {self.new_version}")
            self.changes.append(MAIN_FILE)
            return True

        except Exception as e:
            print(f"❌ ERRO ao atualizar APP_VERSION: {e}")
            return False

    def update_readme_version(self):
        """Atualiza versão no README"""
        try:
            with open(README_FILE, 'r', encoding='utf-8') as f:
                content = f.read()

            today = datetime.now().strftime("%d/%m/%Y")

            # Atualizar cabeçalho: versão
            content = re.sub(
                r'Versão Atual:\s*[\d.]+',
                f'Versão Atual: {self.new_version}',
                content
            )

            # Atualizar seção Desenvolvimento
            content = re.sub(
                r'- \*\*Versão\*\*:\s*[\d.]+',
                f'- **Versão**: {self.new_version}',
                content
            )

            # Atualizar data
            content = re.sub(
                r'- \*\*Data\*\*:\s*\d{2}/\d{2}/\d{4}',
                f'- **Data**: {today}',
                content
            )

            with open(README_FILE, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ README atualizado: v{self.new_version} ({today})")
            self.changes.append(README_FILE)
            return True

        except Exception as e:
            print(f"❌ ERRO ao atualizar README: {e}")
            return False

    def run_validation(self):
        """Executa validação de documentação"""
        print("\n📋 Executando validação...")
        
        # Temporariamente capturar print do validador
        old_stdout = sys.stdout
        try:
            from io import StringIO
            sys.stdout = StringIO()
            
            if self.validator.validate_version_consistency():
                sys.stdout = old_stdout
                return True
            else:
                sys.stdout = old_stdout
                print("❌ Validação falhou!")
                return False
        except Exception as e:
            sys.stdout = old_stdout
            print(f"⚠️  Erro na validação: {e}")
            return True  # Continuar mesmo com erro

    def create_git_commit(self):
        """Faz commit das mudanças"""
        try:
            print("\n📦 Preparando commit...")

            # Stage alterações
            for file in self.changes:
                subprocess.run(['git', 'add', str(file)], check=True, capture_output=True)

            # Commit
            commit_msg = f"chore: atualiza versao para v{self.new_version}"
            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✅ Commit criado: {commit_msg}")
                return True
            else:
                if "nothing to commit" in result.stderr:
                    print("⚠️  Nenhuma mudança para fazer commit")
                    return True
                else:
                    print(f"❌ ERRO no commit: {result.stderr}")
                    return False

        except Exception as e:
            print(f"❌ ERRO ao fazer commit: {e}")
            return False

    def update_version(self, auto_commit: bool = False):
        """Função principal"""
        print("=" * 70)
        print(f" ATUALIZADOR DE VERSÃO - AlertaIntruso")
        print("=" * 70)
        print(f"\n📌 Nova versão: v{self.new_version}")
        print()

        # 1. Validar formato
        if not self.validate_version_format():
            return False

        # 2. Atualizar versão
        print("\n🔄 Atualizando arquivos...")
        if not self.update_app_version():
            return False
        if not self.update_readme_version():
            return False

        # 3. Validar
        print()
        full_validation = DocumentationValidator()
        if not full_validation.run_all_validations():
            return False

        # 4. Commit (opcional)
        if auto_commit:
            if not self.create_git_commit():
                return False
            print("\n✅ Versão atualizada e commitada com sucesso!")
        else:
            print("\n✅ Versão atualizada com sucesso!")
            print("\n💡 Próximos passos:")
            print("   1. Revise as mudanças: git diff")
            print("   2. Faça commit: git commit -am 'chore: atualiza versao'")
            print("   3. Ou execute push.ps1 para fazer push")

        return True


def main():
    if len(sys.argv) < 2:
        print("Uso: python update_version_safe.py <nova_versao> [--commit]")
        print("\nExemplos:")
        print("  python update_version_safe.py 4.5.8")
        print("  python update_version_safe.py 4.5.8 --commit")
        sys.exit(1)

    new_version = sys.argv[1]
    auto_commit = "--commit" in sys.argv

    updater = VersionUpdater(new_version)
    if updater.update_version(auto_commit=auto_commit):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
