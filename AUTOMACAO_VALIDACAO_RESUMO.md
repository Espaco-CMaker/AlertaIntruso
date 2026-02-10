# Automação de Validação e Commit - AlertaIntruso

## 📌 Resumo

A automação garante que **README, CHANGELOG e Código estejam sempre sincronizados** antes de fazer push para o GitHub. Isso evita:

- ❌ Upload de documentação desatualizada
- ❌ Versões inconsistentes entre código e documentação
- ❌ Cabeçalhos de funções sem documentação
- ❌ Dados sensíveis (config.ini) no repositório

## 🔧 Componentes da Automação

### 1. **validate_documentation.py** (Validador Principal)
Executa validações antes do commit:
- ✅ Versões sincronizadas (código ↔ README ↔ CHANGELOG)
- ✅ README tem seção Changelog
- ✅ Cabeçalhos de funções documentados
- ✅ Versão em arquivos relevantes
- ✅ Seção "Sobre" completa

**Uso:**
```powershell
python validate_documentation.py
```

### 2. **push.ps1** (Script de Push Melhorado)
Integra validação antes de fazer push:
1. Executa validador (bloqueia se houver erros)
2. Verifica segurança (config.ini protegido)
3. Adiciona arquivos ao git
4. Faz commit
5. Faz push

**Uso:**
```powershell
.\push.ps1
```

### 3. **update_version_safe.py** (Atualizador de Versão)
Atualiza versão com segurança:
- Valida formato (X.Y.Z)
- Atualiza APP_VERSION
- Atualiza README
- Executa validações completas
- Faz commit automático (opcional)

**Uso:**
```powershell
python update_version_safe.py 4.5.8 --commit
```

### 4. **GUIA_VALIDACAO_COMMITS.md** (Documentação)
Guia completo sobre validações e troubleshooting.

## 🚀 Fluxo de Trabalho Recomendado

### Cenário 1: Correção Simples (Sem Mudança de Versão)

```powershell
# 1. Faça as mudanças no código
# Edite AlertaIntruso Claude+GPT.py

# 2. Teste as mudanças
python "AlertaIntruso Claude+GPT.py"

# 3. Faça push com validação automática
.\push.ps1
```

**Resultado:**
- ✅ Validações executadas
- ✅ Se OK → commit e push automático
- ❌ Se erro → mensagem clara do problema

---

### Cenário 2: Lançamento de Nova Versão

```powershell
# 1. Faça as mudanças no código
# Edite AlertaIntruso Claude+GPT.py

# 2. Atualize CHANGELOG.md manualmente
# Adicione:
# ## v4.5.8 (DD/MM/YYYY)
# ### Titulo
# - Feature 1
# - Fix 1

# 3. Atualize versão com validação
python update_version_safe.py 4.5.8 --commit

# 4. Faça push
.\push.ps1
```

**Resultado:**
- ✅ APP_VERSION = "4.5.8"
- ✅ README atualizado
- ✅ Commit criado automaticamente
- ✅ Push executado

---

### Cenário 3: Apenas Validar (Sem Commit Imediato)

```powershell
# Validar estado atual
python validate_documentation.py

# Ou fazer teste de push
.\push.ps1  # Irá parar antes do commit se houver erros
```

## 📊 Matriz de Decisão

```
┌─────────────────────────────────────────────────────────────────┐
│ O que você quer fazer?                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ✓ Fazer commit + push com validação   → .\push.ps1            │
│                                                                  │
│ ✓ Só validar                           → python validate_documentation.py
│                                                                  │
│ ✓ Atualizar versão + validar           → python update_version_safe.py v4.5.8
│                                                                  │
│ ✓ Atualizar versão + commit + validar → python update_version_safe.py v4.5.8 --commit
│                                                                  │
│ ✓ Depois fazer push                    → .\push.ps1            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## ✅ Checklist Automático

O `push.ps1` executa automaticamente:

- [x] Validação de versão (código ↔ README ↔ CHANGELOG)
- [x] Verificação de segurança (config.ini ignorado)
- [x] Validação de documentação (Changelog, Sobre)
- [x] Revisão de cabeçalhos (docstrings)
- [x] Sincronização de versão em arquivos relevantes
- [x] Staging de alterações
- [x] Commit com mensagem automática
- [x] Push para GitHub

## ⚠️ Tipos de Erro/Aviso

### 🛑 ERROS (Bloqueiam Push)

```
❌ Versões desincronizadas
   Solução: Execute python update_version_safe.py <versão>

❌ config.ini em git
   Solução: git rm --cached config.ini
            echo "config.ini" >> .gitignore
```

### ⚠️ AVISOS (Não Bloqueiam)

```
⚠️  Funções públicas sem docstring
   Solução: Adicione docstrings como boas práticas

⚠️  README sem seção Changelog
   Solução: Adicione ## Changelog Resumido com as mudanças recentes
```

## 📝 Exemplos de Uso Real

### Exemplo 1: Fix Rápido

```powershell
# Arquivo: AlertaIntruso Claude+GPT.py
# Mudança: Corrige bug na linha 500

PS> .\push.ps1

# Resultado:
# [0/7] Validando documentação... ✅
# [1/7] Verificando status Git... ✅
# [2/7] Validando segurança... ✅
# [3/7] Adicionando arquivos... ✅
# [4/7] Arquivos a serem commitados... (mostra lista)
# [5/7] Fazendo commit... ✅
# [6/7] Fazendo push... ✅
# [7/7] Validacao final... ✅
# PUSH CONCLUIDO COM SUCESSO!
```

### Exemplo 2: Atualizar Versão

```powershell
PS> python update_version_safe.py 4.5.8 --commit

# Resultado:
# 📌 Nova versão: v4.5.8
# ✅ APP_VERSION atualizada: 4.5.7 → 4.5.8
# ✅ README atualizado: v4.5.8 (10/02/2026)
# 📋 Executando validação...
# ✅ Versões sincronizadas: v4.5.8
# ✅ TODAS AS VALIDAÇÕES PASSARAM!
# ✅ Commit criado: chore: atualiza versao para v4.5.8
# ✅ Versão atualizada e commitada com sucesso!
```

### Exemplo 3: Erro de Validação

```powershell
PS> .\push.ps1

# Resultado:
# [0/7] Validando documentação...
# ❌ ERRO: Versões desincronizadas!
#   - Código (main): v4.5.8
#   - README: v4.5.7
#   ➜ Atualize o README para v4.5.8
# 
# FALHA NA VALIDACAO DE DOCUMENTACAO!
# Corrija os erros acima antes de fazer push

# Solução:
# python update_version_safe.py 4.5.8
# .\push.ps1  # Tente novamente
```

## 🔍 Como Funciona Internamente

### Validação de Versão

```
1. Lê APP_VERSION do arquivo principal
2. Lê versão do README
3. Lê versão mais recente do CHANGELOG
4. Compara: todos devem bater
```

### Validação de Documentação

```
1. Procura seção ## Changelog ou ## Changelog Resumido
2. Verifica se há referência ao CHANGELOG.md
3. Avalia se as mudanças recentes estão documentadas
```

### Validação de Funções

```
1. Procura todas as funções def público (sem _)
2. Verifica se têm """ ou '''
3. Lista aquelas que não têm docstring
```

### Validação de Segurança

```
1. Testa: git check-ignore config.ini
2. Se não ignore → erro e parada
3. Se ignore → OK
```

## 🛠️ Manutenção da Automação

### Atualizar Validações

Edite `validate_documentation.py` e adicione novos métodos:

```python
def validate_algo_novo(self):
    """Sua validação aqui"""
    print("\n🔍 Validando algo novo...")
    
    if tudo_ok:
        self.add_check("Validação bem-sucedida")
        return True
    else:
        self.add_error("Descrição do erro")
        return False

# Registre em run_all_validations():
def run_all_validations(self):
    self.validate_version_consistency()
    self.validate_readme_has_changelog()
    self.validate_function_headers()
    self.validate_version_in_files()
    self.validate_about_section()
    self.validate_algo_novo()  # ← Adicione seu novo
```

### Customizar Mensagens

As mensagens de validação usam emojis para clareza:

- ✅ = Sucesso
- ❌ = Erro (bloqueia)
- ⚠️  = Aviso (continua)
- 📋 = Ação em progresso
- 🔍 = Validação

### Debug

Para debug detalhado:

```powershell
# Executar validador com traceback
python -u validate_documentation.py

# Ver detalhes do git
git status -v

# Simular push sem fazer realmente
git push --dry-run origin main
```

## 📚 Referências Rápidas

| Comando | Descrição |
|---------|-----------|
| `python validate_documentation.py` | Validar apenas |
| `.\push.ps1` | Validar + Commit + Push |
| `python update_version_safe.py 4.5.8` | Atualizar versão |
| `python update_version_safe.py 4.5.8 --commit` | Atualizar + Commit |
| `git status` | Ver mudanças |
| `git diff` | Ver diferenças |
| `git log --oneline -5` | Últimos 5 commits |

## 🎯 Objetivos Alcançados

✅ **README sempre atualizado** - Sincronização automática com versão  
✅ **CHANGELOG refletido** - Mudanças documentadas  
✅ **Cabeçalhos validados** - Funções documentadas  
✅ **Versão consistente** - Bate em código, README, CHANGELOG  
✅ **Segurança garantida** - config.ini protegido  
✅ **Workflow automatizado** - Um comando para validar + commit + push  

---

**Última atualização:** 10/02/2026  
**Versão do Sistema:** AlertaIntruso v4.5.7  
**Autor do Guia:** GitHub Copilot
