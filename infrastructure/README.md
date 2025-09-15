# Infraestrutura como Código (IaC)

Esta seção contém templates e scripts para provisionar recursos Azure necessários para os workshops e aplicações.

## 📁 Estrutura

```
infrastructure/
├── README.md
├── bicep/
│   ├── fabric-workspace/
│   ├── ai-foundry/
│   ├── container-apps/
│   └── shared-resources/
├── terraform/ (planejado)
└── scripts/
    ├── setup-environment.ps1
    ├── deploy-workshop.ps1
    └── cleanup-resources.ps1
```

## 🚀 Templates Disponíveis

### Bicep Templates

#### 1. Fabric Workspace
**Localização:** `bicep/fabric-workspace/`
**Descrição:** Template para criar workspace do Microsoft Fabric com configurações básicas.

#### 2. AI Foundry
**Localização:** `bicep/ai-foundry/`
**Descrição:** Template para provisionar AI Foundry Projects com Azure OpenAI.

#### 3. Container Apps
**Localização:** `bicep/container-apps/`
**Descrição:** Template para deployment de aplicações em Azure Container Apps.

#### 4. Recursos Compartilhados
**Localização:** `bicep/shared-resources/`
**Descrição:** Recursos comuns como Key Vault, Storage Account, etc.

## 🛠️ Scripts de Automação

### Setup de Ambiente
```powershell
.\scripts\setup-environment.ps1 -SubscriptionId "your-sub-id" -ResourceGroupName "fabric-workshop-rg"
```

### Deploy Workshop Completo
```powershell
.\scripts\deploy-workshop.ps1 -Environment "dev" -Location "East US"
```

### Limpeza de Recursos
```powershell
.\scripts\cleanup-resources.ps1 -ResourceGroupName "fabric-workshop-rg"
```

## 🎯 Parâmetros Principais

Cada template aceita parâmetros personalizáveis:
- **location:** Região Azure
- **environment:** dev, test, prod
- **resourcePrefix:** Prefixo para nomenclatura
- **tags:** Tags para organização

## 📋 Pré-requisitos

- Azure CLI instalado e configurado
- PowerShell 7+
- Permissões adequadas na subscription Azure
- Bicep CLI (para templates Bicep)

## 🔧 Uso

1. **Clone o repositório e navegue para infrastructure/**
2. **Configure seus parâmetros em `parameters.json`**
3. **Execute o script de setup apropriado**
4. **Monitore o deployment via Azure Portal**

## 🤝 Contribuição

Para adicionar novos templates:
1. Siga a estrutura de pastas estabelecida
2. Inclua documentação específica
3. Adicione parâmetros configuráveis
4. Teste em ambiente de desenvolvimento