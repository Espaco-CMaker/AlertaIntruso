# Checklist de Atualização de Versão

Este documento detalha o processo para atualizar a versão do AlertaIntruso de forma consistente.

## � Regra de Versionamento Semântico (X.Y.Z)

> **REGRA OBRIGATÓRIA**: O assistente (IA) só pode incrementar automaticamente o **Z (PATCH)**.
> Os dígitos **X (MAJOR)** e **Y (MINOR)** só devem ser alterados sob **comando explícito do usuário**.

| Dígito | Nome  | Quem altera       | Quando                                      |
|--------|-------|-------------------|---------------------------------------------|
| X      | MAJOR | Usuário (manual)  | Reescrita, mudança de arquitetura, breaking  |
| Y      | MINOR | Usuário (manual)  | Novo recurso relevante, mudança funcional    |
| Z      | PATCH | IA (automático)   | Bugfix, ajuste, melhoria incremental         |

---

## 📋 Checklist Obrigatório para Cada Versão

### ✅ Procedimento de Aceite (sempre que validar uma versão)
- [ ] Incrementar **PATCH** (último dígito Z apenas)
- [ ] Atualizar docs: CHANGELOG.md, README.md, STATUS.md, RELEASE.md
- [ ] Gerar executável versionado: `AlertaIntruso-vX.Y.Z.exe`
- [ ] Atualizar Git (add/commit/push) com código + docs + `.spec` (sem versionar `.exe`)
- [ ] Publicar executável nos assets da release no GitHub

### 1. Cabeçalho do Programa (AlertaIntruso Claude+GPT.py)
- [ ] Atualizar versão em: `Versão:         X.Y.Z`
- [ ] Atualizar data em: `Data:           DD/MM/YYYY`
- [ ] Atualizar status em: `Status:         ESTÁVEL` (ou apropriado)

**Localização**: Linhas 1-12 (bloco docstring inicial)

```python
"""
================================================================================
ALERTAINTRUSO — ALARME INTELIGENTE POR VISÃO COMPUTACIONAL (RTSP • YOLO • MULTICAM)
================================================================================
Arquivo:        AlertaIntruso Claude+GPT.py
Projeto:        Sistema de Alarme Inteligente por Visão Computacional
Versão:         X.Y.Z  ← ATUALIZAR
Data:           DD/MM/YYYY  ← ATUALIZAR
Autor:          Fabio Bettio
Licença:        Uso educacional / experimental
Status:         ESTÁVEL  ← ATUALIZAR SE NECESSÁRIO
```

### 2. Constante APP_VERSION
- [ ] Atualizar `APP_VERSION = "X.Y.Z"`

### 2.1. Título da Janela
- [ ] Garantir que o título da janela usa a versão atual (`APP_VERSION`)

**Localização**: [AlertaIntruso Claude+GPT.py](AlertaIntruso%20Claude+GPT.py#L1363)

```python
self.root.title(f"AlertaIntruso v{APP_VERSION} — 4 Câmeras RTSP (YOLO)")
```

**Localização**: Procurar por `APP_VERSION = ` (normalmente por volta da linha 185)

```python
APP_VERSION = "X.Y.Z"  ← ATUALIZAR
```

### 3. Changelog no Cabeçalho
- [ ] Adicionar nova entrada de versão no topo do changelog
- [ ] Incluir data, tipo de mudança e descrição
- [ ] Listar features, bugfixes ou melhorias

**Localização**: Linhas após `Changelog completo` (aproximadamente linha 24-50)

```python
v4.5.0 (04/02/2026) [TIPO - DESCRIÇÃO] (linhas: XX)
    - Mudança 1
    - Mudança 2
    - Mudança 3
```

### 4. Git - Commit e Push
- [ ] `git add AlertaIntruso Claude+GPT.py`
- [ ] `git commit -m "feat/fix/docs(vX.Y.Z): Descrição da mudança"`
- [ ] `git push origin main`

### 5. Executável (se aplicável)
- [ ] Gerar novo executável: `.\.venv\Scripts\python.exe -m PyInstaller --onefile --windowed --name "AlertaIntruso-vX.Y.Z" "AlertaIntruso Claude+GPT.py"`
- [ ] Aguardar ~15 minutos para conclusão
- [ ] Verificar se `dist\AlertaIntruso-vX.Y.Z.exe` foi criado (tamanho ~70MB)
- [ ] **NÃO** adicionar `.exe` no Git (`dist\*.exe`)
- [ ] `git add AlertaIntruso-vX.Y.Z.spec`
- [ ] `git commit -m "build(vX.Y.Z): atualizar spec da versão"`
- [ ] `git push origin main`
- [ ] Criar/atualizar release `vX.Y.Z` no GitHub
- [ ] Fazer upload do asset `dist\AlertaIntruso-vX.Y.Z.exe` na release

---

## 📌 Tipos de Versão

### Nomenclatura Semântica: MAJOR.MINOR.PATCH

- **MAJOR** (ex: **4**.5.0): Mudanças significativas que podem quebrar compatibilidade
- **MINOR** (ex: 4.**5**.0): Novas features compatíveis
- **PATCH** (ex: 4.5.**0**): Bugfixes e correções

### Exemplos de Incremento

| Situação | De | Para | Tipo |
|----------|----|----|------|
| Nova feature principal | 4.3.20 | 4.4.0 | MINOR |
| Bugfix crítico | 4.3.20 | 4.3.21 | PATCH |
| Múltiplas features | 4.3.20 | 4.4.0 | MINOR |
| Manutenção/melhoria | 4.4.0 | 4.5.0 | MINOR |

---

## 🔍 Verificação Final

Antes de fazer `git push`, executar:

```powershell
# 1. Verificar se arquivo foi modificado
git status

# 2. Ver diferenças
git diff AlertaIntruso Claude+GPT.py | head -50

# 3. Verificar se versão está correta
Select-String "APP_VERSION" "AlertaIntruso Claude+GPT.py"

# 4. Verificar último commit
git log --oneline -1
```

---

## 📝 Exemplo Completo de Atualização

### Preparação
```powershell
# Abrir o arquivo para edição
code "AlertaIntruso Claude+GPT.py"
```

### Editar (4 locais):

1. **Cabeçalho (linha ~7)**
   ```
   Versão:         4.5.0
   Data:           04/02/2026
   Status:         ESTÁVEL
   ```

2. **APP_VERSION (linha ~185)**
   ```python
   APP_VERSION = "4.5.0"
   ```

3. **Changelog (linha ~24)**
   ```
   v4.5.0 (04/02/2026) [FEATURE - DESCRIÇÃO]
       - Feature 1
       - Feature 2
   ```

4. **Código/Features** (conforme necessário)

### Commit
```powershell
git add "AlertaIntruso Claude+GPT.py"
git commit -m "feat(v4.5.0): Descrição completa da mudança"
git push origin main
```

---

## ⚠️ Erros Comuns a Evitar

- ❌ Atualizar só a constante `APP_VERSION` sem atualizar o cabeçalho
- ❌ Esquecer de adicionar entrada no changelog
- ❌ Usar data errada no cabeçalho
- ❌ Não fazer push após commit
- ❌ Gerar executável antes de confirmar que o código está correto

---

## 📌 Última Atualização

- **Versão**: 4.5.5
- **Data**: 04/02/2026
- **Próxima revisão**: Conforme necessário

---

**Criado em**: 04/02/2026 | **Status**: Ativo
