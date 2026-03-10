---
description: Validação de Versão Estável (Release Workflow)
---
# Validação de Versão Estável para Projetos Python (PyInstaller + Github)

Este workflow descreve o processo exato a seguir sempre que o usuário declarar uma versão local como "Estável" e solicitar a publicação/empacotamento de encerramento do ciclo.

## Objetivos e Regras
Qualquer transição de versão experimental (hotfix, dev, test) para versão de produção (main/stable) exige a documentação explícita nos arquivos de acompanhamento e o merge seguro no GitHub, além da compilação do executável.

// turbo-all
## 1. Atualização dos Documentos Oficiais (Arquivos YAML/MD)
- Leia a versão final estabelecida pelo usuário. Ex. `v6.0.9`.
- Escreva as notas unificadas do que foi feito no topo do arquivo `CHANGELOG.md`.
- No arquivo `README.md`, procure no topo pelas tags referentes à "Versão Atual" ou "Data" e substitua-as pela data local e versão corriqueira do dia. Atualize a seção de "Desenvolvimento > Versão" na base do documento.
- Substitua todo o log sumário no arquivo `STATUS.md`, informando a nova data e assinalando o documento como **Estável**, listando no mesmo as novas funções introduzidas ("Objetivos Alcançados").

## 2. Compilação do Executável (PyInstaller)
- Identifique a linguagem principal (se `.py`).
- Crie ou copie de base um arquivo de parametrização `.spec` que aponte para o novo executável: `<NomeDoApp>-v<Versao>.spec`.
- Se baseie num arquivo `spec` antigo existente no diretório raiz do projeto para entender os hooks ou requires. Exemplo: `AlertaIntruso-v6.0.9.spec` deve possuir `exe = EXE(name='AlertaIntruso-v6.0.9')`.
- Execute a compilação utilizando: `pyinstaller <NomeDoApp>-v<Versao>.spec`.
- Verifique se a pasta `dist/` gerou corretamente a aplicação Windows.

## 3. Versionamento Git e GitHub
- Certifique-se de consolidar as alterações de código e de documentação na branch corrente: `git add .` seguido de `git commit -m "chore: release vX.X.X (feature list)"`.
- Troque para o branch raiz do projeto (geralmente `main` ou `master`): `git checkout main`.
- Mescle as alterações recém aprovadas para estabilização (a branch anterior, ex: `hotfix/vY.Y.Y`): `git merge <antiga-branch>`.
- Publique a estabilização limpa para os repositórios remotos: `git push origin main`.
