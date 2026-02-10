# 🚀 SCRIPTS DE PUSH - AlertaIntruso v4.5.7

Criei 2 scripts para fazer o commit e push automaticamente.

---

## 📋 Opção 1: Script PowerShell (Recomendado)

### Como Executar:

1. **Abra PowerShell** como Administrador
2. **Navegue até o diretório** (opcional):
   ```powershell
   cd d:\#Projetos\AlertaIntruso
   ```

3. **Execute o script**:
   ```powershell
   .\push.ps1
   ```

### Se der erro de permissão:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\push.ps1
```

### Depois volte a restrição:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser
```

---

## 📋 Opção 2: Script Batch (Windows CMD)

### Como Executar:

1. **Abra CMD ou PowerShell**
2. **Navegue até o diretório**:
   ```cmd
   cd d:\#Projetos\AlertaIntruso
   ```

3. **Execute o script**:
   ```cmd
   push.bat
   ```

---

## 🎯 O Que os Scripts Fazem

### Passo a Passo Automático:

```
[1/6] Verifica status Git
      ↓
[2/6] Valida segurança (config.ini deve estar ignorado)
      ↓
[3/6] Adiciona arquivos para commit
      ↓
[4/6] Mostra arquivos que serão commitados
      ↓
[5/6] Faz o commit com mensagem detalhada
      ↓
[6/6] Faz o push para https://github.com/Espaco-CMaker/AlertaIntruso
      ↓
✅ SUCESSO! Repositório atualizado
```

---

## ✅ Arquivos que Serão Commitados

```
12+ novos arquivos:
  ✅ RESUMO_DOWNLOADS.md
  ✅ PAGINA_DOWNLOADS.html
  ✅ SUMARIO_EXECUTIVO.md
  ✅ GUIA_INSTALACAO_DOWNLOAD.md
  ✅ ESPECIFICACAO_TECNICA.json
  ✅ config.ini.example
  ✅ GUIA_SEGURANCA_REPOSITORIO.md
  ✅ VERIFICACAO_SEGURANCA_RESUMO.md
  ✅ CHECKLIST_PRE_PUSH.md
  ✅ GUIA_GIT_PUSH.md
  ✅ LISTA_ARQUIVOS_GERADOS.txt
  ✅ INICIO_AQUI.md

1 arquivo modificado:
  ✅ .gitignore (fortalecido)

IMPORTANTE: config.ini NÃO será commitado (está ignorado)
```

---

## 🔐 Validações de Segurança

Os scripts automaticamente:

✅ Verificam se config.ini está sendo ignorado  
✅ Validam que nenhum dado sensível será enviado  
✅ Mostram exatamente o que será commitado  
✅ Fazem pausa antes de cada etapa crítica  

---

## 📊 Resultado Esperado

Após executar o script:

```
[OK] config.ini esta protegido
[3/6] Adicionando arquivos para commit...
[4/6] Arquivos a serem commitados:
      modified:   .gitignore
      new file:   RESUMO_DOWNLOADS.md
      new file:   PAGINA_DOWNLOADS.html
      ... (mais arquivos)
[5/6] Fazendo commit...
[6/6] Fazendo push para GitHub...

============================================================================
 PUSH CONCLUIDO COM SUCESSO!
============================================================================

Seu repositorio foi atualizado!
Link: https://github.com/Espaco-CMaker/AlertaIntruso
```

---

## 🚀 Próximas Ações

Após o push bem-sucedido:

1. Acesse https://github.com/Espaco-CMaker/AlertaIntruso
2. Verifique se todos os arquivos aparecem
3. Compartilhe o link com usuários
4. (Opcional) Configure GitHub Pages para PAGINA_DOWNLOADS.html

---

## 🆘 Troubleshooting

### Erro: "fatal: authentication failed"

**Solução 1**: Usar GitHub CLI
```powershell
gh auth login
```

**Solução 2**: Usar GitHub Desktop
- Instale: https://desktop.github.com/
- Faça login
- Sincronize branches

### Erro: "not a git repository"

```powershell
git init
git remote add origin https://github.com/Espaco-CMaker/AlertaIntruso.git
```

### Erro: "config.ini not ignored"

```powershell
git rm --cached config.ini
git add .gitignore
git commit -m "fix: remove config.ini from tracking"
```

---

## 📚 Referência Rápida

| Script | Comando | Linguagem |
|--------|---------|-----------|
| push.ps1 | `.\push.ps1` | PowerShell |
| push.bat | `push.bat` | Batch (CMD) |

**Ambos fazem a mesma coisa**, escolha o que preferir!

---

**Status**: ✅ Pronto para executar  
**Data**: 10/02/2026  
**Versão**: 4.5.7

Boa sorte! 🎉
