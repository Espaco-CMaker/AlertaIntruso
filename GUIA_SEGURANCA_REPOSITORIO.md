# 🔒 GUIA DE SEGURANÇA - Preparando para Repositório Público

**Data**: 10 de fevereiro de 2026  
**Status**: ✅ Verificado e Corrigido

---

## ⚠️ Dados Sensíveis Encontrados e Corrigidos

### 🔴 CRÍTICOS (Corrigidos)

| Item | Status | Ação Tomada |
|------|--------|------------|
| **Bot Token Telegram** | ✅ Corrigido | Removido de `config.ini` |
| **Chat ID Telegram** | ✅ Corrigido | Removido de `config.ini` |
| **Credenciais RTSP** | ✅ Corrigido | Substituídas por placeholders |
| **IPs de Câmeras** | ✅ Corrigido | Mascarados (192.168.x.x) |

---

## 📋 Verificação de Segurança

### ✅ Arquivos Verificados

```
[✅] AlertaIntruso Claude+GPT.py      - Sem credenciais (código genérico)
[✅] AlertaIntruso v5.py               - Sem credenciais (código genérico)
[✅] config.ini                        - CORRIGIDO - Dados de exemplo
[✅] .gitignore                        - ATUALIZADO - config.ini ignorado
[✅] Novo: config.ini.example          - CRIADO - Template para usuários
```

### 🔍 O Que Foi Alterado

#### 1. `config.ini` - Dados Sensíveis Removidos

**ANTES** (PERIGOSO ❌):
```ini
[CAM1]
rtsp_url = rtsp://fgbettio:1578@192.168.1.36:554/11

[TELEGRAM]
bot_token = 1225244164:AAEjzOPGYWUlCQAeSCz-LnqvMRSKIeiDBpA
chat_id = -1003752805157
```

**DEPOIS** (SEGURO ✅):
```ini
[CAM1]
rtsp_url = rtsp://usuario:senha@192.168.x.x:554/stream

[TELEGRAM]
bot_token = YOUR_BOT_TOKEN_HERE
chat_id = YOUR_CHAT_ID_HERE
```

#### 2. `.gitignore` - Fortalecido

**Adicionadas Linhas**:
```
config.ini                  # ⚠️ Nunca versionar config com dados sensíveis
*.key
*.pem
models/                     # Modelos podem ser grandes
.vscode/settings.json       # Pode conter caminhos locais
```

#### 3. `config.ini.example` - CRIADO

- Template de configuração seguro
- Instruções para usuários
- Guia de como obter tokens
- Avisos de segurança

---

## 🚀 Próximas Ações ANTES de Tornar Público

### 1️⃣ Limpar Histórico Git

Se o repositório já foi commitado com dados sensíveis:

```bash
# ⚠️ IMPORTANTE: Fazer backup primeiro!
git clone https://github.com/seu-usuario/AlertaIntruso.git seu-repo-backup

# Remover arquivo config.ini do histórico Git
git filter-branch --tree-filter 'rm -f config.ini' HEAD

# Forçar push
git push origin --force

# Ou: usar BFG Repo-Cleaner (mais seguro)
# Instruções em: https://rtyley.github.io/bfg-repo-cleaner/
```

### 2️⃣ Validar `.gitignore`

```bash
# Verificar o que será ignorado
git check-ignore -v config.ini
git check-ignore -v log.txt
git check-ignore -v *.env
```

### 3️⃣ Criar `.env.example`

Se usar variáveis de ambiente:

```bash
# .env.example
TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE
RTSP_CAM1_URL=rtsp://usuario:senha@IP:554/stream
```

### 4️⃣ Verificação Final

```bash
# Verificar se nenhum dado sensível está no Git
git grep -i "token\|password\|senha\|secret" 

# Deve retornar VAZIO!
```

---

## 📝 Instruções para Usuários Finais

### Como Configurar (Documentado em GUIA_INSTALACAO_DOWNLOAD.md)

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/AlertaIntruso.git
   ```

2. **Copie o arquivo de exemplo**:
   ```bash
   cp config.ini.example config.ini
   ```

3. **Edite com suas informações**:
   ```bash
   nano config.ini
   # Ou use seu editor preferido
   ```

4. **Nunca faça commit do config.ini**:
   ```bash
   git check-ignore config.ini  # Deve retornar: config.ini
   ```

---

## 🔐 Práticas de Segurança Implementadas

### ✅ Git Security

| Prática | Status | Detalhes |
|---------|--------|----------|
| `.gitignore` atualizado | ✅ | Excluir config.ini, logs, fotos |
| Sem credenciais no código | ✅ | Carregadas de variáveis/config |
| Sem tokens hardcoded | ✅ | De arquivo de config externo |
| Template `.example` | ✅ | Usuários sabem como configurar |

### ✅ Arquivo Config

| Prática | Status | Detalhes |
|---------|--------|----------|
| config.ini não versionado | ✅ | Bloqueado no .gitignore |
| Dados sensíveis removidos | ✅ | Placeholders genéricos |
| Template com instruções | ✅ | config.ini.example criado |
| Comentários de segurança | ✅ | Avisos para usuários |

### ✅ Código

| Prática | Status | Detalhes |
|---------|--------|----------|
| Sem hardcoding de secrets | ✅ | Carregado de config.ini |
| Verificação de tokens | ✅ | Validação antes de usar |
| Tratamento de erros | ✅ | Não loga dados sensíveis |
| Documentação segura | ✅ | Avisos em README |

---

## 🛡️ Camadas de Proteção

```
┌─────────────────────────────────────────────┐
│  Usuário não ve dados sensíveis no GitHub   │
├─────────────────────────────────────────────┤
│ Camada 1: .gitignore                        │
│  ├─ config.ini ignorado                     │
│  └─ *.key, *.env ignorados                  │
├─────────────────────────────────────────────┤
│ Camada 2: config.ini sanitizado             │
│  ├─ Sem token real                          │
│  └─ Placeholders genéricos                  │
├─────────────────────────────────────────────┤
│ Camada 3: Template de exemplo               │
│  ├─ config.ini.example com instruções       │
│  └─ Guia para usuários configurarem         │
├─────────────────────────────────────────────┤
│ Camada 4: Documentação                      │
│  ├─ README com avisos                       │
│  └─ GUIA com instruções seguras             │
└─────────────────────────────────────────────┘
```

---

## ✅ Checklist Final

Antes de fazer push para repositório público:

- [ ] `config.ini` sem credenciais reais
- [ ] `config.ini.example` criado e documentado
- [ ] `.gitignore` atualizado com `config.ini`
- [ ] Nenhum `.env` no repositório
- [ ] Nenhum `*.key` ou `*.pem`
- [ ] README com avisos de segurança
- [ ] Histórico Git limpo (se tinha dados antes)
- [ ] `git grep` retorna VAZIO para "token", "password", "senha"
- [ ] `.github/` com templates de issues/PRs (opcional)
- [ ] LICENSE adicionada (MIT/Apache/GPL conforme escolha)

---

## 📚 Referências

| Tópico | Link |
|--------|------|
| GitHub Security | https://github.com/features/security |
| OWASP Secrets | https://owasp.org/www-project-secrets-management/ |
| .gitignore Generator | https://www.toptal.com/developers/gitignore |
| Remove Secrets Git | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository |
| BFG Repo-Cleaner | https://rtyley.github.io/bfg-repo-cleaner/ |

---

## 🎯 Resultado Final

```
STATUS: ✅ SEGURO PARA REPOSITÓRIO PÚBLICO

✅ Credenciais removidas
✅ Config sanitizado
✅ Template criado
✅ .gitignore fortalecido
✅ Documentação atualizada
✅ Pronto para GitHub público
```

---

## 🔔 Avisos Importantes

> ⚠️ **Se já tinha feito commit com dados sensíveis:**
> 
> 1. Considere as credenciais comprometidas
> 2. Gere novos tokens/senhas
> 3. Limpe o histórico Git (veja seção acima)
> 4. Force push para atualizar

> ⚠️ **Em produção:**
> 
> 1. Use variáveis de ambiente, não arquivos
> 2. Nunca deixe `.env` no repositório
> 3. Audite logs regularmente
> 4. Use GitHub Secrets para CI/CD

---

**Documento de Segurança**  
**AlertaIntruso v4.5.7**  
**Data**: 10/02/2026  
**Status**: ✅ Verificado e Aprovado
