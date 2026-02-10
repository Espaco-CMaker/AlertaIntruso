#!/usr/bin/env python3
"""
Validador de Documentação - AlertaIntruso
Verifica se README, CHANGELOG e código estão sincronizados
"""

import re
import sys
from pathlib import Path
from datetime import datetime

MAIN_FILE = Path("AlertaIntruso Claude+GPT.py")
README_FILE = Path("README.md")
CHANGELOG_FILE = Path("CHANGELOG.md")

class DocumentationValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checks_passed = 0

    def add_error(self, msg):
        self.errors.append(f"❌ ERRO: {msg}")

    def add_warning(self, msg):
        self.warnings.append(f"⚠️  AVISO: {msg}")

    def add_check(self, msg):
        self.checks_passed += 1
        print(f"✅ {msg}")

    def get_version_from_main(self):
        """Extrai APP_VERSION do arquivo principal"""
        try:
            with open(MAIN_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'APP_VERSION = ["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
        except Exception as e:
            self.add_error(f"Não conseguiu ler {MAIN_FILE}: {e}")
        return None

    def get_version_from_readme(self):
        """Extrai versão do README"""
        try:
            with open(README_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            # Procura por "Versão Atual Baseada na: X.X.X"
            match = re.search(r'Versão Atual Baseada na:\s*([\d.]+)', content)
            if match:
                return match.group(1)
            # Fallback: procura por "**Versão**: X.X.X"
            match = re.search(r'\*\*Versão\*\*:\s*([\d.]+)', content)
            if match:
                return match.group(1)
        except Exception as e:
            self.add_error(f"Não conseguiu ler {README_FILE}: {e}")
        return None

    def get_version_from_changelog(self):
        """Extrai versão mais recente do CHANGELOG"""
        try:
            with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines[:20]:  # Procura nas primeiras linhas
                match = re.search(r'##\s+v([\d.]+)', line)
                if match:
                    return match.group(1)
        except Exception as e:
            self.add_error(f"Não conseguiu ler {CHANGELOG_FILE}: {e}")
        return None

    def get_latest_changelog_features(self):
        """Extrai as features da versão mais recente do CHANGELOG"""
        try:
            with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            # Extrai do primeiro ## v até o próximo ## v
            match = re.search(r'##\s+v[\d.]+[^\n]*\n(.*?)(?=##\s+v|$)', content, re.DOTALL)
            if match:
                return match.group(1).strip()
        except Exception as e:
            self.add_error(f"Não conseguiu extrair features do CHANGELOG: {e}")
        return None

    def validate_version_consistency(self):
        """Valida se as versões estão sincronizadas"""
        print("\n📋 Validando Versões...")
        
        version_main = self.get_version_from_main()
        version_readme = self.get_version_from_readme()
        version_changelog = self.get_version_from_changelog()

        if not version_main:
            self.add_error("APP_VERSION não encontrada em AlertaIntruso Claude+GPT.py")
            return False

        if not version_readme:
            self.add_error("Versão não encontrada no README.md")
            return False

        if not version_changelog:
            self.add_error("Versão não encontrada no CHANGELOG.md")
            return False

        # Verifica consistência
        if version_main != version_readme:
            self.add_error(
                f"Versões desincronizadas!\n"
                f"  - Código (main): v{version_main}\n"
                f"  - README: v{version_readme}\n"
                f"  ➜ Atualize o README para v{version_main}"
            )
            return False
        
        if version_main != version_changelog:
            self.add_error(
                f"Versão do CHANGELOG desincronizada!\n"
                f"  - Código: v{version_main}\n"
                f"  - CHANGELOG: v{version_changelog}"
            )
            return False

        self.add_check(f"Versões sincronizadas: v{version_main}")
        return True

    def validate_readme_has_changelog(self):
        """Valida se o README reflete as mudanças do CHANGELOG"""
        print("\n📚 Validando Documentação...")
        
        try:
            with open(README_FILE, 'r', encoding='utf-8') as f:
                readme = f.read()
            with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f:
                changelog = f.read()

            # Procura seção de Changelog no README
            if '## Changelog' not in readme:
                self.add_warning(
                    "README não tem seção '## Changelog'\n"
                    "  ➜ Considere adicionar um resumo das mudanças recentes"
                )
            else:
                # Verifica se as últimas mudanças estão no README
                latest_entry = re.search(r'###\s+v[\d.]+', readme)
                if latest_entry:
                    self.add_check("Seção Changelog encontrada no README")
                
        except Exception as e:
            self.add_error(f"Erro ao validar Changelog: {e}")
            return False

        return True

    def validate_function_headers(self):
        """Valida cabeçalhos de funções (docstrings)"""
        print("\n⚙️  Validando Cabeçalhos de Funções...")
        
        try:
            with open(MAIN_FILE, 'r', encoding='utf-8') as f:
                content = f.read()

            # Procura funções def sem docstring
            functions_without_docstring = []
            for match in re.finditer(r'def\s+(\w+)\s*\([^)]*\)\s*:', content):
                func_name = match.group(1)
                func_pos = match.end()
                
                # Verifica se há """ ou ''' logo após
                next_content = content[func_pos:func_pos+50]
                if not (next_content.strip().startswith('"""') or 
                        next_content.strip().startswith("'''")):
                    # Ignora funções privadas e mágicas
                    if not func_name.startswith('_'):
                        functions_without_docstring.append(func_name)

            if functions_without_docstring:
                self.add_warning(
                    f"Funções públicas sem docstring ({len(functions_without_docstring)}):\n"
                    f"  ➜ {', '.join(functions_without_docstring[:5])}"
                )
            else:
                self.add_check("Todas as funções públicas têm docstrings")

        except Exception as e:
            self.add_error(f"Erro ao validar funções: {e}")
            return False

        return True

    def validate_version_in_files(self):
        """Valida se a versão aparece em arquivos relevantes"""
        print("\n🔍 Validando Versão em Arquivos Relevantes...")
        
        version = self.get_version_from_main()
        if not version:
            return False

        critical_files = {
            'push.ps1': [f'v{version}', 'AlertaIntruso v'],
            'config.ini.example': ['# Versão:', 'config'],
        }

        all_good = True
        for file_path, patterns in critical_files.items():
            if not Path(file_path).exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                found = any(pattern in content for pattern in patterns)
                if found:
                    self.add_check(f"Versão/identificação presente em {file_path}")
                else:
                    self.add_warning(f"Versão pode estar desatualizada em {file_path}")
                    all_good = False
                    
            except Exception as e:
                self.add_warning(f"Não conseguiu ler {file_path}: {e}")

        return all_good

    def validate_about_section(self):
        """Valida se há seção 'Sobre' no README com informações corretas"""
        print("\n ℹ️  Validando Seção 'Sobre'...")
        
        try:
            with open(README_FILE, 'r', encoding='utf-8') as f:
                content = f.read()

            required_sections = {
                'Versão': r'Versão(?:\*\*)?:\s*[\d.]+',
                'Data': r'Data(?:\*\*)?:\s*\d{2}/\d{2}/\d{4}',
                'Autor': r'Autor(?:\*\*)?:\s*',
            }

            missing = []
            for section, pattern in required_sections.items():
                if not re.search(pattern, content):
                    missing.append(section)

            if missing:
                self.add_warning(
                    f"Seção 'Sobre' incompleta (faltam): {', '.join(missing)}\n"
                    f"  ➜ Adicione versão, data e autor"
                )
            else:
                self.add_check("Seção 'Sobre' com informações completas")

        except Exception as e:
            self.add_error(f"Erro ao validar seção 'Sobre': {e}")
            return False

        return True

    def run_all_validations(self):
        """Executa todas as validações"""
        print("=" * 70)
        print(" VALIDADOR DE DOCUMENTAÇÃO - AlertaIntruso")
        print("=" * 70)

        self.validate_version_consistency()
        self.validate_readme_has_changelog()
        self.validate_function_headers()
        self.validate_version_in_files()
        self.validate_about_section()

        self.print_summary()
        return len(self.errors) == 0

    def print_summary(self):
        """Imprime resumo de validações"""
        print("\n" + "=" * 70)
        print(" RESUMO DE VALIDAÇÕES")
        print("=" * 70)

        if self.checks_passed > 0:
            print(f"\n✅ Verificações bem-sucedidas: {self.checks_passed}")

        if self.warnings:
            print(f"\n⚠️  Avisos ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")

        if self.errors:
            print(f"\n❌ Erros ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
            print("\n⛔ FALHA NA VALIDAÇÃO")
            sys.exit(1)
        else:
            print("\n" + "=" * 70)
            print(" ✅ TODAS AS VALIDAÇÕES PASSARAM!")
            print("=" * 70)
            sys.exit(0)


if __name__ == "__main__":
    validator = DocumentationValidator()
    validator.run_all_validations()
