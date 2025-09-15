# 🔧 Pré-requisitos para Microsoft Fabric Workshop

## 📋 Visão Geral

Este documento lista todos os pré-requisitos necessários para executar os workshops do Microsoft Fabric com sucesso.

## ☁️ Recursos Azure Necessários

### Microsoft Fabric
- ✅ **Trial do Fabric** (60 dias gratuitos) ou
- ✅ **Fabric Capacity** (F2 ou superior recomendado)
- ✅ **Workspace** com permissões de Contributor/Admin

#### Como Obter:
1. Acesse [fabric.microsoft.com](https://fabric.microsoft.com)
2. Inicie trial gratuito ou configure capacidade
3. Crie workspace dedicado para workshops

### Azure AI Foundry Projects
- ✅ **Subscription Azure** ativa
- ✅ **Resource Group** dedicado
- ✅ **AI Foundry Hub** configurado
- ✅ **AI Project** criado

#### Como Configurar:
```bash
# Via Azure CLI
az group create --name fabric-workshop-rg --location eastus
az cognitiveservices account create --name fabric-ai-foundry --resource-group fabric-workshop-rg --kind AIServices --sku S0 --location eastus
```

### Azure OpenAI
- ✅ **Azure OpenAI Service** provisioned
- ✅ **GPT-4o-mini** model deployed
- ✅ **API keys** configuradas

#### Modelos Recomendados:
| Modelo | Uso | Deployment Name |
|--------|-----|-----------------|
| GPT-4o-mini | Chat geral | gpt-4o-mini |
| text-embedding-3-small | Embeddings | text-embedding-3-small |

## 💻 Ferramentas Locais

### Obrigatórias
- ✅ **Navegador moderno** (Chrome 120+, Edge 120+, Firefox 120+)
- ✅ **Python 3.11+** (para desenvolvimento local)
- ✅ **Git** (para clonar repositório)

### Recomendadas
- ✅ **VS Code** com extensões:
  - Python
  - Jupyter
  - Azure Tools
- ✅ **Azure CLI** (última versão)
- ✅ **PowerShell 7+** (para scripts de automação)

### Instalação via Winget (Windows):
```powershell
# Ferramentas essenciais
winget install Microsoft.VisualStudioCode
winget install Python.Python.3.11
winget install Git.Git
winget install Microsoft.AzureCLI
winget install Microsoft.PowerShell
```

## 🔐 Permissões e Acessos

### Microsoft Fabric
**Necessário:**
- Workspace Admin ou Contributor
- Capacidade para criar Lakehouse
- Permissões para upload de dados

**Verificação:**
1. Acesse seu workspace no Fabric
2. Teste criação de novo item
3. Confirme capacidade disponível

### Azure Subscription
**Necessário:**
- Contributor ou Owner na subscription
- Permissões para criar recursos
- Quota para Azure OpenAI

**Verificação:**
```bash
# Verificar permissões
az role assignment list --assignee $(az account show --query user.name -o tsv)

# Verificar quota OpenAI
az cognitiveservices account list-usage --name <openai-resource-name> --resource-group <rg-name>
```

## 📊 Dados e Datasets

### Incluídos no Repositório
- ✅ **AdventureWorks** (50MB) - Dados de exemplo Microsoft
- ✅ **Olist** (150MB) - Dados de e-commerce brasileiro  
- ✅ **Metadata** - Esquemas e documentação

### Requisitos de Armazenamento
- **Local:** ~500MB para repositório completo
- **Fabric:** ~1GB de capacidade para datasets
- **Backup:** Recomendado para dados importantes

## 🌐 Conectividade e Rede

### Requisitos de Rede
- ✅ **Internet estável** (download/upload)
- ✅ **Acesso a domínios:**
  - `*.fabric.microsoft.com`
  - `*.azure.com`
  - `*.openai.azure.com`
  - `*.github.com`

### Firewall/Proxy
Se sua organização usa firewall corporativo:
```
Liberar domínios:
- *.fabric.microsoft.com (porta 443)
- *.analysis.windows.net (porta 443)  
- *.azure.com (porta 443)
- *.openai.azure.com (porta 443)
```

## 🧠 Conhecimentos Técnicos

### Nível Básico (Obrigatório)
- ✅ **SQL** básico (SELECT, JOIN, WHERE)
- ✅ **Conceitos de BI** (dimensões, fatos)
- ✅ **Navegação** em portais web
- ✅ **Excel/CSV** manipulation

### Nível Intermediário (Recomendado)
- ✅ **Python** básico (pandas, notebooks)
- ✅ **Azure** conceitos gerais
- ✅ **Data Warehousing** (ETL, modelagem)
- ✅ **Power BI** (DAX, visualizações)

### Nível Avançado (Opcional)
- ✅ **PySpark** para transformações
- ✅ **Azure DevOps** para CI/CD
- ✅ **Terraform/Bicep** para IaC
- ✅ **Docker** para containerização

## ✅ Checklist de Verificação

### Antes de Começar
```
□ Microsoft Fabric workspace criado e acessível
□ Azure subscription ativa com permissões
□ Azure OpenAI service deployado
□ Python 3.11+ instalado localmente  
□ VS Code configurado com extensões
□ Git configurado para clonar repositórios
□ Repositório clonado localmente
□ Conectividade testada com Fabric portal
```

### Teste de Conectividade
```powershell
# Teste Azure CLI
az account show

# Teste Python
python --version
pip list | findstr pandas

# Teste Git  
git --version

# Teste acesso ao Fabric
# (Abrir browser em fabric.microsoft.com)
```

## 🆘 Resolução de Problemas

### Problemas Comuns

#### "Não consigo acessar o Fabric"
**Soluções:**
1. Verificar licença/trial ativo
2. Confirmar permissões no workspace
3. Testar com browser diferente
4. Limpar cache do browser

#### "Erro de quota no Azure OpenAI"
**Soluções:**
1. Verificar quota disponível:
   ```bash
   az cognitiveservices account list-usage --name <resource> --resource-group <rg>
   ```
2. Solicitar aumento de quota
3. Usar região alternativa

#### "Python dependencies não instalam"
**Soluções:**
1. Atualizar pip:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Usar virtual environment:
   ```bash
   python -m venv workshop-env
   workshop-env\Scripts\activate
   ```
3. Instalar com uv (mais rápido):
   ```bash
   pip install uv
   uv pip install -r requirements.txt
   ```

### Contatos de Suporte
- **Issues GitHub:** [Reportar problemas](https://github.com/Miyake-Diogo/MS-Fabric-Workshop/issues)
- **Discussions:** [Fazer perguntas](https://github.com/Miyake-Diogo/MS-Fabric-Workshop/discussions)
- **Microsoft Docs:** [Documentação oficial](https://learn.microsoft.com/fabric/)

## 📚 Recursos Adicionais

### Documentação Oficial
- [Microsoft Fabric Docs](https://learn.microsoft.com/fabric/)
- [Azure AI Foundry Docs](https://learn.microsoft.com/azure/ai-studio/)
- [Azure OpenAI Docs](https://learn.microsoft.com/azure/ai-services/openai/)

### Tutoriais de Preparação
- [Fabric Trial Setup](https://learn.microsoft.com/fabric/get-started/fabric-trial)
- [Azure OpenAI Quickstart](https://learn.microsoft.com/azure/ai-services/openai/quickstart)
- [Python Environment Setup](https://docs.python.org/3/tutorial/venv.html)

### Comunidade
- [Fabric Community](https://community.fabric.microsoft.com/)
- [Azure AI Community](https://techcommunity.microsoft.com/azure/ai)
- [Power BI Community](https://community.powerbi.com/)

---

**✅ Pronto para começar?** Se todos os itens do checklist estão marcados, você pode prosseguir para o [Setup Manual](manual-setup.md) ou [Deploy Automatizado](automated-deployment.md)!