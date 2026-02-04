# AlertaIntruso v5 - Versão Experimental

## ⚠️ STATUS: DESENVOLVIMENTO INDEPENDENTE

Esta é a versão experimental v5 do AlertaIntruso, desenvolvida em paralelo à versão estável v4.

### 📌 Informações do Branch
- **Branch**: `dev/v5-experimental`
- **Base**: v4.3.19 (estável)
- **Versão Atual**: 5.0.0-alpha
- **Objetivo**: Mudanças arquiteturais intensas e features avançadas

### 🔀 Estrutura do Repositório

```
main (branch)
└── AlertaIntruso Claude+GPT.py  → v4.3.19 (ESTÁVEL)
└── config.ini
└── CHANGELOG.md
└── STATUS.md
└── RELEASE.md

dev/v5-experimental (branch)
└── AlertaIntruso Claude+GPT.py  → v4.3.19 (ESTÁVEL - mantido)
└── AlertaIntruso v5.py          → v5.0.0-alpha (EXPERIMENTAL)
└── README_v5.md                 → Este arquivo
└── config_v5.ini                → Configuração isolada da v5
```

### 🎯 Objetivos da v5

1. **Arquitetura Modular**: Separar componentes em módulos independentes
2. **Performance Melhorada**: Otimizações de processamento e memória
3. **Features Avançadas**: Novas funcionalidades experimentais
4. **Código Limpo**: Refatoração completa para melhor manutenibilidade
5. **Testes**: Sistema de testes automatizados

### 🚀 Como Usar

#### Executar v4 (Estável):
```powershell
python "AlertaIntruso Claude+GPT.py"
```

#### Executar v5 (Experimental):
```powershell
python "AlertaIntruso v5.py"
```

### 📝 Desenvolvimento

#### Mudar para v5:
```bash
git checkout dev/v5-experimental
```

#### Voltar para v4:
```bash
git checkout main
```

#### Ver diferenças:
```bash
git diff main..dev/v5-experimental
```

### 🔧 Configuração Isolada

A v5 usa arquivo de configuração separado (`config_v5.ini`) para não interferir com a v4 estável.

### ⚠️ Avisos Importantes

- **NÃO USE EM PRODUÇÃO**: Esta é uma versão experimental
- **Bugs esperados**: A v5 pode ter instabilidades
- **Breaking changes**: Compatibilidade com v4 não garantida
- **Use a v4 para produção**: A v4.3.19 é a versão estável recomendada

### 📊 Roadmap v5

- [ ] Refatoração modular (separar classes em arquivos)
- [ ] Sistema de plugins
- [ ] API REST para controle remoto
- [ ] Dashboard web
- [ ] Suporte a mais modelos YOLO (v5, v8, etc)
- [ ] Gravação de vídeo sob demanda
- [ ] Zonas de detecção customizáveis
- [ ] Integração com bancos de dados

### 🤝 Contribuindo

Este é um projeto experimental. Feedback e sugestões são bem-vindos!

### 📄 Licença

Uso educacional / experimental

---

**Última atualização**: 02/02/2026
**Versão**: 5.0.0-alpha
