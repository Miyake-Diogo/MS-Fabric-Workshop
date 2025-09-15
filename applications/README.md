# Aplicações Demonstrativas

Esta seção contém aplicações completas que demonstram o uso prático das funcionalidades do Microsoft Fabric.

## 🚀 Aplicações Disponíveis

### DataBot
**Localização:** `databot/`
**Descrição:** ChatBot inteligente integrado com Fabric Data Agents via AI Foundry Projects.

**Arquitetura:**
- **Backend:** Python + FastAPI + Semantic Kernel
- **Frontend:** TypeScript + React
- **Infraestrutura:** Azure Container Apps
- **AI:** Azure OpenAI (GPT-4o-mini) + Fabric Data Agents

**Recursos:**
- Interface conversacional para consulta de dados
- Integração com Data Agents do Fabric
- Deployment automatizado no Azure
- Desenvolvimento local com Docker

## 🛠️ Desenvolvimento

Cada aplicação possui:
- Documentação completa
- Scripts de desenvolvimento local
- Configuração de CI/CD
- Templates de infraestrutura

## 🚀 Deploy

As aplicações podem ser implantadas:
- **Localmente:** usando Docker Compose
- **Azure:** usando Bicep templates e scripts automatizados
- **CI/CD:** usando GitHub Actions (em desenvolvimento)

## 📁 Estrutura Padrão

```
application-name/
├── README.md
├── pyproject.toml
├── .env.example
├── docker-compose.yml
├── src/
│   ├── backend/
│   └── frontend/
├── infra/
├── docs/
└── scripts/
```

## 🤝 Contribuição

Para criar novas aplicações, siga a estrutura padrão e inclua:
- Documentação completa
- Configuração de desenvolvimento local
- Templates de infraestrutura
- Exemplos de uso