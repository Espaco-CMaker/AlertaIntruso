#!/usr/bin/env python3
"""
Automacao de aceite de versao para o projeto AlertaIntruso.

Fluxo principal:
1) Incrementa patch de X.Y.Z -> X.Y.(Z+1)
2) Atualiza versao no arquivo principal (cabecalho + APP_VERSION)
3) Atualiza CHANGELOG.md com entrada da nova versao
4) Garante exibicao de commit na aba Sobre (se ainda nao existir)
5) Gera novo .spec versionado e tenta build do executavel
6) Cria commit de release com texto do que foi modificado/alterado/corrigido
7) Faz push
8) Registra hash do commit de release no CHANGELOG em commit adicional
9) Faz push final
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

MAIN_FILE = Path("AlertaIntruso Claude+GPT.py")
CHANGELOG_FILE = Path("CHANGELOG.md")
README_FILE = Path("README.md")
STATUS_FILE = Path("STATUS.md")
RELEASES_URL = "https://github.com/Espaco-CMaker/AlertaIntruso/releases"


def run(cmd: List[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        check=check,
        text=True,
        capture_output=capture,
    )


def today_br() -> str:
    return dt.datetime.now().strftime("%d/%m/%Y")


def parse_version(ver: str) -> Tuple[int, int, int]:
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", ver.strip())
    if not m:
        raise ValueError(f"Versao invalida: {ver!r}")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def bump_patch(ver: str) -> str:
    x, y, z = parse_version(ver)
    return f"{x}.{y}.{z + 1}"


def get_current_version_from_main() -> str:
    content = MAIN_FILE.read_text(encoding="utf-8")
    m = re.search(r'APP_VERSION\s*=\s*"([^"]+)"', content)
    if not m:
        raise RuntimeError("APP_VERSION nao encontrada no arquivo principal.")
    return m.group(1)


def replace_once(pattern: str, repl: str, text: str, flags: int = 0) -> str:
    new_text, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n == 0:
        raise RuntimeError(f"Padrao nao encontrado: {pattern}")
    return new_text


def ensure_commit_in_about(content: str) -> str:
    if "def get_commit_code()" not in content:
        insert_after = 'MAX_THUMBS = 200\n'
        helper = """

def get_commit_code() -> str:
    \"\"\"Retorna hash curto do commit atual; fora do git retorna N/A.\"\"\"
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
"""
        if insert_after not in content:
            raise RuntimeError("Nao foi possivel inserir helper de commit (MAX_THUMBS nao encontrado).")
        content = content.replace(insert_after, insert_after + helper, 1)

    if "import subprocess" not in content:
        content = replace_once(r"(import\s+json\s*\n)", r"\1import subprocess\n", content)

    if 'text=f"Commit: {get_commit_code()}"' not in content:
        content = replace_once(
            r'(ttk\.Label\(self\.frame_about,\s*text=f"Vers[aã]o:\s*\{APP_VERSION\}".*?\)\.pack\(pady=10\)\n)',
            r'\1        ttk.Label(self.frame_about, text=f"Commit: {get_commit_code()}", font=("Arial", 10)).pack(pady=2)\n',
            content,
            flags=re.MULTILINE,
        )
    return content


def update_main_file(new_version: str, release_date: str, bullets: List[str]) -> None:
    content = MAIN_FILE.read_text(encoding="utf-8")

    content = replace_once(r"Vers[aã]o:\s+\d+\.\d+\.\d+", f"Versão:         {new_version}", content)
    content = replace_once(r"Data:\s+\d{2}/\d{2}/\d{4}", f"Data:           {release_date}", content)
    content = replace_once(r'APP_VERSION\s*=\s*"[^"]+"', f'APP_VERSION = "{new_version}"', content)

    content = ensure_commit_in_about(content)

    changelog_entry = [f"v{new_version} ({release_date}) [ACEITE] (linhas: 0)"]
    for b in bullets:
        changelog_entry.append(f"    - {b}")
    changelog_text = "\n".join(changelog_entry) + "\n\n"

    if f"v{new_version} ({release_date})" not in content:
        content = replace_once(
            r"(Changelog completo\s*\n=+\s*\n\s*)",
            r"\1" + changelog_text,
            content,
            flags=re.MULTILINE,
        )

    MAIN_FILE.write_text(content, encoding="utf-8")


def update_changelog_file(new_version: str, release_date: str, bullets: List[str]) -> None:
    content = CHANGELOG_FILE.read_text(encoding="utf-8")

    if f"## v{new_version} ({release_date})" in content:
        return

    lines = [f"## v{new_version} ({release_date})", "### ✅ Aceite de Versao"]
    for b in bullets:
        lines.append(f"- **ITEM**: {b}")
    lines.append("- **COMMIT**: pending")
    lines.append("")
    block = "\n".join(lines)

    header_pat = r"(^\ufeff?#\s+CHANGELOG\s+-\s+AlertaIntruso\s*\n\s*\n)"
    if re.search(header_pat, content, flags=re.MULTILINE):
        content = re.sub(header_pat, r"\1" + block + "\n", content, count=1, flags=re.MULTILINE)
    else:
        # Fallback defensivo para changelog fora do formato esperado
        content = block + "\n" + content
    CHANGELOG_FILE.write_text(content, encoding="utf-8")


def find_latest_spec() -> Optional[Path]:
    specs = sorted(Path(".").glob("AlertaIntruso-v*.spec"))
    if not specs:
        return None
    return specs[-1]


def create_versioned_spec(new_version: str) -> Path:
    target = Path(f"AlertaIntruso-v{new_version}.spec")
    if target.exists():
        return target

    src = find_latest_spec()
    if src is None:
        src = Path("AlertaIntruso.spec")
        if not src.exists():
            raise RuntimeError("Nenhum .spec encontrado para gerar executavel versionado.")

    text = src.read_text(encoding="utf-8")
    text = re.sub(r"name='AlertaIntruso-v[\d.]+'", f"name='AlertaIntruso-v{new_version}'", text)
    if "name='AlertaIntruso-v" not in text:
        text = re.sub(r"name='AlertaIntruso'", f"name='AlertaIntruso-v{new_version}'", text)
    target.write_text(text, encoding="utf-8")
    return target


def build_executable(spec_path: Path) -> Path:
    # tenta pyinstaller direto, depois modulo
    try:
        run(["pyinstaller", "--noconfirm", str(spec_path)], check=True, capture=True)
    except Exception:
        run([sys.executable, "-m", "PyInstaller", "--noconfirm", str(spec_path)], check=True, capture=True)

    exe_name = f"{spec_path.stem}.exe"
    exe_path = Path("dist") / exe_name
    if not exe_path.exists():
        raise RuntimeError(f"Build terminou mas executavel nao foi encontrado: {exe_path}")
    return exe_path


def make_release_commit_message(new_version: str, modificado: str, alterado: str, corrigido: str) -> str:
    parts: List[str] = []
    if modificado.strip():
        parts.append(f"modificado: {modificado.strip()}")
    if alterado.strip():
        parts.append(f"alterado: {alterado.strip()}")
    if corrigido.strip():
        parts.append(f"corrigido: {corrigido.strip()}")
    details = " | ".join(parts) if parts else "aceite da versao"
    return f"release(v{new_version}): {details}"


def ensure_clean_worktree() -> None:
    status = run(["git", "status", "--porcelain"], check=True, capture=True).stdout.strip()
    if status:
        raise RuntimeError(
            "Worktree nao esta limpa. Faça commit/stash antes de rodar o aceite automatizado."
        )


def stage_and_commit(msg: str, paths: List[Path]) -> str:
    add_cmd = ["git", "add"] + [str(p) for p in paths if p.exists()]
    run(add_cmd, check=True, capture=True)
    run(["git", "commit", "-m", msg], check=True, capture=True)
    commit = run(["git", "rev-parse", "--short", "HEAD"], check=True, capture=True).stdout.strip()
    return commit


def ensure_tag(tag_name: str) -> None:
    tag_exists = run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag_name}"],
        check=False,
        capture=True,
    ).returncode == 0
    if not tag_exists:
        run(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], check=True, capture=True)


def maybe_push_tag(do_push: bool, tag_name: str) -> None:
    if do_push:
        run(["git", "push", "origin", tag_name], check=True, capture=True)


def try_upload_asset_to_release(tag_name: str, exe_path: Optional[Path], do_push: bool) -> None:
    if not do_push or exe_path is None:
        return
    if not exe_path.exists():
        return

    gh_exists = run(["where", "gh"], check=False, capture=True).returncode == 0
    if not gh_exists:
        print("AVISO: gh CLI nao encontrado. Upload automatico de asset nao executado.")
        print(f"Suba manualmente o executavel em: {RELEASES_URL}/tag/{tag_name}")
        print(f"Arquivo: {exe_path}")
        return

    # Cria release se nao existir e faz upload do asset (sobrescrevendo se ja existir).
    view = run(["gh", "release", "view", tag_name], check=False, capture=True)
    if view.returncode != 0:
        run(
            ["gh", "release", "create", tag_name, "--title", f"AlertaIntruso {tag_name}", "--notes", f"Release automatizado {tag_name}"],
            check=True,
            capture=True,
        )
    run(["gh", "release", "upload", tag_name, str(exe_path), "--clobber"], check=True, capture=True)


def update_changelog_commit_hash(new_version: str, release_date: str, commit_hash: str) -> None:
    content = CHANGELOG_FILE.read_text(encoding="utf-8")
    section_pat = rf"(## v{re.escape(new_version)} \({re.escape(release_date)}\)[\s\S]*?- \*\*COMMIT\*\*: )pending"
    new_content, n = re.subn(section_pat, rf"\1{commit_hash}", content, count=1)
    if n == 0:
        # fallback: se ja existir COMMIT na secao, nao falha
        return
    CHANGELOG_FILE.write_text(new_content, encoding="utf-8")


def maybe_push(do_push: bool) -> None:
    if do_push:
        run(["git", "push"], check=True, capture=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Aceite automatizado de nova versao.")
    parser.add_argument("--modificado", default="", help="Resumo do que foi modificado.")
    parser.add_argument("--alterado", default="", help="Resumo do que foi alterado.")
    parser.add_argument("--corrigido", default="", help="Resumo do que foi corrigido.")
    parser.add_argument("--no-build", action="store_true", help="Nao gera executavel.")
    parser.add_argument("--no-push", action="store_true", help="Nao faz push no github.")
    parser.add_argument("--no-release-upload", action="store_true", help="Nao tenta upload do .exe no GitHub Release.")
    parser.add_argument("--allow-dirty", action="store_true", help="Permite rodar com worktree suja.")
    args = parser.parse_args()

    if not MAIN_FILE.exists():
        print(f"ERRO: arquivo principal nao encontrado: {MAIN_FILE}")
        return 1
    if not CHANGELOG_FILE.exists():
        print(f"ERRO: changelog nao encontrado: {CHANGELOG_FILE}")
        return 1

    try:
        if not args.allow_dirty:
            ensure_clean_worktree()

        current_version = get_current_version_from_main()
        new_version = bump_patch(current_version)
        release_date = today_br()

        bullets = []
        if args.modificado.strip():
            bullets.append(f"MODIFICADO: {args.modificado.strip()}")
        if args.alterado.strip():
            bullets.append(f"ALTERADO: {args.alterado.strip()}")
        if args.corrigido.strip():
            bullets.append(f"CORRIGIDO: {args.corrigido.strip()}")
        if not bullets:
            bullets.append("ACEITE da versao sem descricao adicional.")

        update_main_file(new_version, release_date, bullets)
        update_changelog_file(new_version, release_date, bullets)

        spec_path = create_versioned_spec(new_version)
        exe_path: Optional[Path] = None
        if not args.no_build:
            exe_path = build_executable(spec_path)

        release_msg = make_release_commit_message(
            new_version,
            args.modificado,
            args.alterado,
            args.corrigido,
        )
        release_hash = stage_and_commit(
            release_msg,
            [MAIN_FILE, CHANGELOG_FILE, spec_path, README_FILE, STATUS_FILE],
        )
        maybe_push(not args.no_push)
        tag_name = f"v{new_version}"
        ensure_tag(tag_name)
        maybe_push_tag(not args.no_push, tag_name)

        update_changelog_commit_hash(new_version, release_date, release_hash)
        doc_hash = stage_and_commit(
            f"docs(changelog): registra commit {release_hash} na v{new_version}",
            [CHANGELOG_FILE],
        )
        maybe_push(not args.no_push)
        if not args.no_release_upload:
            try_upload_asset_to_release(tag_name, exe_path, not args.no_push)

        print("OK: aceite concluido")
        print(f"Versao anterior: v{current_version}")
        print(f"Nova versao: v{new_version}")
        print(f"Spec: {spec_path}")
        if exe_path is not None:
            print(f"Executavel: {exe_path}")
            print(f"Releases: {RELEASES_URL}")
        print(f"Commit release: {release_hash}")
        print(f"Commit changelog: {doc_hash}")
        return 0
    except subprocess.CalledProcessError as e:
        print("ERRO em comando externo:")
        print(" ".join(e.cmd))
        if e.stderr:
            print(e.stderr.strip())
        return 2
    except Exception as e:
        print(f"ERRO: {e}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
