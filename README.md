# 🚀 Microsoft Fabric Workshop

![Microsoft Fabric](https://img.shields.io/badge/Microsoft%20Fabric-Analytics-blue?logo=microsoft)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Azure](https://img.shields.io/badge/Azure-Cloud-blue?logo=microsoft-azure)

Workshop completo sobre **Microsoft Fabric** com exemplos práticos, notebooks interativos e aplicações demonstrativas em **português brasileiro**.

## 📋 Índice

- [🎯 Sobre o Workshop](#-sobre-o-workshop)
- [🚀 Quick Start](#-quick-start)
- [📚 Workshops Disponíveis](#-workshops-disponíveis)
- [🛠️ Aplicações](#️-aplicações)
- [🏗️ Infraestrutura](#️-infraestrutura)
- [📖 Documentação](#-documentação)
- [🤝 Contribuição](#-contribuição)
- [⚠️ Disclaimer](#️-disclaimer)

## 🎯 Sobre o Workshop

Este repositório contém uma coleção completa de workshops práticos sobre **Microsoft Fabric**, cobrindo desde conceitos básicos até implementações avançadas. Todos os materiais estão em português brasileiro e foram projetados para aprendizado hands-on.

### 🎓 O que você vai aprender:
- **Fabric Lakehouse** - Arquitetura medallion (Bronze, Silver, Gold)
- **Data Agents** - IA integrada para consulta de dados
- **Data Warehouse** - Modelagem dimensional avançada
- **Real-time Analytics** - Processamento de streaming
- **Mirroring** - Sincronização de dados
- **Integração com Databricks** - Better together scenarios

## 🚀 Quick Start

### Pré-requisitos
- ✅ Acesso ao **Microsoft Fabric** (trial ou licenciado)
- ✅ **Python 3.11+** instalado
- ✅ **Git** para clonar o repositório
- ✅ **VS Code** com extensão Python (recomendado)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/Miyake-Diogo/MS-Fabric-Workshop.git
cd MS-Fabric-Workshop

# Instale dependências para workshops
cd workshops
pip install -e .

# Para desenvolvimento da aplicação databot
cd ../applications/databot
pip install -e .
```

### Primeiro Workshop
1. 📁 Navegue para `workshops/lakehouse/`
2. 📖 Leia a documentação em `docs/`
3. 🚀 Execute os notebooks na ordem: `01` → `02` → `03` → `04` → `05`

## 📚 Workshops Disponíveis

| Workshop | Status | Dificuldade | Duração | Descrição |
|----------|--------|-------------|---------|-----------|
| **[Lakehouse](workshops/lakehouse/)** | ✅ Completo | 🟢 Básico | ~3h | Arquitetura medallion com transformações ETL |
| **[Data Agents](workshops/data-agents/)** | ✅ Completo | 🟡 Intermediário | ~2h | IA conversacional para dados |
| **Data Warehouse** | 🚧 Em progresso | 🟡 Intermediário | ~4h | Modelagem dimensional |
| **Real-time Analytics** | 🚧 Em progresso | 🔴 Avançado | ~3h | KQL e streaming |
| **Mirroring** | 📅 Planejado | 🟢 Básico | ~2h | Sincronização de dados |
| **Databricks Integration** | 📅 Planejado | 🔴 Avançado | ~4h | Cenários integrados |

### 📊 Datasets Incluídos
- **AdventureWorks** - Dados de exemplo da Microsoft
- **Olist** - E-commerce brasileiro para casos reais
- **Dados sintéticos** - Para demonstrações específicas

## 🛠️ Aplicações

### DataBot 🤖
**Localização:** `applications/databot/`

ChatBot inteligente que integra **Fabric Data Agents** com **Azure AI Foundry** para consultas conversacionais de dados.

**Stack Tecnológico:**
- 🐍 **Backend:** Python + FastAPI + Semantic Kernel
- ⚛️ **Frontend:** TypeScript + React
- ☁️ **Cloud:** Azure Container Apps + Azure OpenAI
- 🧠 **IA:** GPT-4o-mini + Fabric Data Agents

**Recursos:**
- Interface de chat intuitiva
- Consultas em linguagem natural
- Integração com dados do Fabric
- Deploy automatizado no Azure

## 🏗️ Infraestrutura

### Templates Bicep
**Localização:** `infrastructure/bicep/`

Templates reutilizáveis para provisionar recursos Azure:
- 🏢 **Fabric Workspace** - Configuração completa do workspace
- 🧠 **AI Foundry Projects** - Setup de IA e modelos
- 📦 **Container Apps** - Deploy de aplicações
- 🔐 **Recursos Compartilhados** - Key Vault, Storage, etc.

### Scripts de Automação
**Localização:** `infrastructure/scripts/`

```powershell
# Setup completo do ambiente
.\setup-environment.ps1 -SubscriptionId "your-id" -Location "East US"

# Deploy do workshop
.\deploy-workshop.ps1 -Environment "dev"

# Limpeza de recursos
.\cleanup-resources.ps1 -ResourceGroupName "fabric-workshop-rg"
```

## 📖 Documentação

### 📁 Estrutura da Documentação
```
docs/
├── workshops/          # Tutoriais detalhados por workshop
├── architecture/       # Diagramas e explicações técnicas  
├── deployment/         # Guias de instalação e deploy
└── troubleshooting/    # Problemas comuns e soluções
```

### 🔗 Links Úteis
- **[Documentação Oficial do Fabric](https://learn.microsoft.com/pt-br/fabric/)**
- **[Tutoriais End-to-End](https://learn.microsoft.com/pt-br/fabric/fundamentals/end-to-end-tutorials)**
- **[Data Agents Preview](https://learn.microsoft.com/pt-br/fabric/data-science/data-agent-scenario)**

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. 🍴 Faça um fork do repositório
2. 🌟 Crie uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
3. 💾 Commit suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
4. 📤 Push para a branch: `git push origin feature/nova-funcionalidade`
5. 🔃 Abra um Pull Request

### 📋 Diretrizes
- Mantenha a documentação em português brasileiro
- Siga a estrutura de pastas estabelecida
- Inclua exemplos práticos e testáveis
- Adicione comentários explicativos no código

## ⚠️ Disclaimer

> **🚨 IMPORTANTE:** Este repositório contém exemplos educacionais e demonstrativos.
> 
> **❌ NÃO USE EM PRODUÇÃO** sem as devidas adaptações de segurança, performance e governança.

### 🔐 Considerações de Segurança
- Remova dados sensíveis antes de commits
- Use Azure Key Vault para secrets em produção
- Configure RBAC adequadamente
- Implemente monitoramento e alertas

### 🎯 Objetivo Educacional
Este workshop foi criado para fins de aprendizado e demonstração das capacidades do Microsoft Fabric em cenários realistas, mas simplificados.

---

<div align="center">

**💡 Dúvidas ou sugestões?**

[![Issues](https://img.shields.io/github/issues/Miyake-Diogo/MS-Fabric-Workshop)](https://github.com/Miyake-Diogo/MS-Fabric-Workshop/issues)
[![Discussions](https://img.shields.io/github/discussions/Miyake-Diogo/MS-Fabric-Workshop)](https://github.com/Miyake-Diogo/MS-Fabric-Workshop/discussions)

**Feito com ❤️ para a comunidade brasileira de dados**

</div>

