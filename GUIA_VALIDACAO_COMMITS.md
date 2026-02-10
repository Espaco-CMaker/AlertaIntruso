# Guia de Validação Automática de Commits

## 📋 Visão Geral

A automação de commit e push do AlertaIntruso agora inclui validações automáticas de documentação para garantir que:

1. **README.md** está sincronizado com o código quanto à versão
2. **README.md** reflete as mudanças recentes do CHANGELOG.md
3. **Cabeçalhos de funções** (docstrings) estão documentados
4. **Versão** aparece em locais relevantes (push.ps1, config.ini.example, etc.)
5. **Seção "Sobre"** contém informações completas (versão, data, autor)

## 🚀 Como Usar

### Fazendo Push com Validação

Execute o script de push que já inclui as validações:

```powershell
.\push.ps1
```

**Fluxo de execução:**

```
[0/7] Validando documentação (README vs CHANGELOG vs Codigo)
[1/7] Verificando status Git
[2/7] Validando segurança (config.ini)
[3/7] Adicionando arquivos
[4/7] Revisar arquivos
[5/7] Fazer commit
[6/7] Fazer push
[7/7] Validacao final
```

### Executando Validação Manualmente

Se preferir validar sem fazer push imediatamente:

```powershell
python validate_documentation.py
```

## ✅ O que é Validado

### 1. Sincronização de Versões

Verifica que a versão em `AlertaIntruso Claude+GPT.py`:
- Bate com a versão no README.md
- Bate com a versão mais recente no CHANGELOG.md

**Erro:**
```
❌ ERRO: Versões desincronizadas!
  - Código (main): v4.5.7
  - README: v4.5.5
  ➜ Atualize o README para v4.5.7
```

**Solução:** Edite o README para usar a versão correta ou atualize o código.

### 2. Documentação README

Verifica se o README contém:
- Seção `## Changelog` ou `## Changelog Resumido`
- Referência ao CHANGELOG completo

**Aviso:**
```
⚠️  AVISO: README não tem seção '## Changelog'
  ➜ Considere adicionar um resumo das mudanças recentes
```

### 3. Cabeçalhos de Funções

Identifica funções públicas (sem `_` prefixo) sem docstring.

**Aviso:**
```
⚠️  AVISO: Funções públicas sem docstring (5):
  ➜ packet_callback, request_soft_reconnect, run, on_mousewheel, cam_row
```

**Solução:** Adicione docstrings às funções públicas:

```python
def sua_funcao():
    """
    Descrição breve da função.
    
    Explique o que ela faz, parâmetros e retorno.
    """
    pass
```

### 4. Versão em Arquivos Relevantes

Verifica se arquivos importantes contêm a versão atual:
- `push.ps1`
- `config.ini.example`

### 5. Seção "Sobre"

Valida que o README possui:
- **Versão**: v X.X.X
- **Data**: DD/MM/YYYY
- **Autor**: Nome do autor

## 🔄 Workflow Recomendado

### Quando Fazer Mudanças

1. **Modifique o código** (AlertaIntruso Claude+GPT.py)
2. **Atualize APP_VERSION** se houver mudanças significativas
3. **Atualize CHANGELOG.md** com:
   - Versão
   - Data
   - Mudanças (Features, Fixes, etc.)
4. **Atualize README.md** se necessário:
   - Versão atual
   - Data
   - Resumo das mudanças recentes
   - Seção "Sobre"

### Exemplo de Commit com Validação

```powershell
# 1. Fazer as mudanças no código
# AlertaIntruso Claude+GPT.py: ...

# 2. Atualizar versão
# APP_VERSION = "4.5.8"

# 3. Atualizar CHANGELOG.md
# ## v4.5.8 (DD/MM/YYYY)
# - Feature nova
# - Fix importante

# 4. Atualizar README.md com seção Changelog Resumido

# 5. Executar push com validação
.\push.ps1
```

## ⚠️ O Que Impede o Push

### Erros Críticos (Bloqueia Push)

O push é interrompido se encontrar:

✗ Versões desincronizadas (código vs README vs CHANGELOG)  
✗ config.ini em git (deve estar em .gitignore)  

### Avisos (Permite Push)

O push continua mesmo com avisos:

⚠️ Funções públicas sem docstring  
⚠️ README faltando seção Changelog  
⚠️ Informações incompletas na seção "Sobre"  

## 🔍 Interpretando Relatórios

### Exemplo: Validação Bem-Sucedida

```
✅ Versões sincronizadas: v4.5.7
✅ Seção Changelog encontrada no README
✅ Versão/identificação presente em push.ps1
✅ Seção 'Sobre' com informações completas

✅ Verificações bem-sucedidas: 5
⚠️  Avisos (1):
  ⚠️  Funções públicas sem docstring (3)

✅ TODAS AS VALIDAÇÕES PASSARAM!
```

### Exemplo: Validação Falhando

```
❌ Erros (1):
  ❌ ERRO: Versões desincronizadas!
  - Código: v4.5.8
  - README: v4.5.7

⛔ FALHA NA VALIDAÇÃO
```

## 🛠️ Customizações

### Adicionar Nova Validação

Edite `validate_documentation.py` e adicione um novo método:

```python
def validate_algo_novo(self):
    """Valida algo específico do projeto"""
    print("\n🔍 Validando Algo Novo...")
    # implementação
    self.add_check("Validação bem-sucedida") 
```

Depois registre no método `run_all_validations()`:

```python
def run_all_validations(self):
    self.validate_version_consistency()
    self.validate_algo_novo()  # nova!
    # ... resto
```

### Customizar Limites

Edite os limites em `validate_documentation.py`:

```python
# Verificar em quantos arquivos a versão deve aparecer
critical_files = {
    'seu_arquivo.py': ['v{version}'],
}
```

## 📝 Checklist Pré-Push

Antes de executar `.\push.ps1`:

- [ ] Todas as mudanças foram testadas
- [ ] CHANGELOG.md foi atualizado
- [ ] APP_VERSION foi incrementada (se necessário)
- [ ] README.md reflete as mudanças recentes
- [ ] config.ini está em .gitignore (dados sensíveis protegidos)
- [ ] Não há dados sensíveis no repositório

## 🆘 Troubleshooting

### Erro: "Python não encontrado"

```powershell
python --version
```

Se não funcionar, configure o Python no PATH ou use o caminho completo:

```powershell
"C:\Python312\python.exe" validate_documentation.py
```

### Erro: "validate_documentation.py não encontrado"

Certifique-se de estar no diretório correto:

```powershell
cd "d:\#Projetos\AlertaIntruso"
ls validate_documentation.py
```

### Aviso: "Funções públicas sem docstring"

Não bloqueia push, mas considere adicionar docstrings. Use o refactoring do Pylance:

1. Abra o arquivo em VS Code
2. Selecione tudo (Ctrl+A)
3. Use Command Palette: "Python: Add Type Annotations" ou similar

## 📚 Referências

- [CHANGELOG.md](CHANGELOG.md) - Histórico completo de versões
- [README.md](README.md) - Documentação principal
- [validate_documentation.py](validate_documentation.py) - Script de validação
- [push.ps1](push.ps1) - Script de push automatizado

---

**Últimas atualizações:** 10/02/2026  
**Versão:** AlertaIntruso v4.5.7
