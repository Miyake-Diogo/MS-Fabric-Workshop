# 📋 Templates para Workshops Microsoft Fabric

## 🎯 Visão Geral

Esta pasta contém templates reutilizáveis para acelerar a criação de novos workshops seguindo as melhores práticas estabelecidas no projeto Olist.

## 📁 Estrutura de Templates

```
templates/
├── notebooks/                    # Templates de notebooks Jupyter
│   ├── bronze-ingestion.template.ipynb
│   ├── silver-transformations.template.ipynb
│   ├── gold-dimensions.template.ipynb
│   ├── gold-facts.template.ipynb
│   └── data-validation.template.ipynb
├── infrastructure/               # Templates de infraestrutura
│   ├── lakehouse-setup.bicep
│   ├── data-pipeline.json
│   └── environment.template.yml
├── documentation/               # Templates de documentação
│   ├── workshop-readme.template.md
│   ├── architecture-guide.template.md
│   └── troubleshooting.template.md
└── scripts/                    # Scripts utilitários
    ├── setup-workshop.ps1
    ├── validate-data.py
    └── generate-sample-data.py
```

## 🔧 Como Usar os Templates

### 1. Criar Novo Workshop

```bash
# Copiar template base
cp -r templates/workshop-base workshops/meu-novo-workshop

# Personalizar configurações
cd workshops/meu-novo-workshop
./scripts/setup-workshop.ps1 -WorkshopName "MeuNovoWorkshop"
```

### 2. Personalizar Notebooks

1. **Bronze Layer**: Adapte o template para sua fonte de dados
2. **Silver Layer**: Configure regras de negócio específicas
3. **Gold Layer**: Defina dimensões e fatos do seu domínio

### 3. Configurar Infraestrutura

1. Adapte os templates Bicep para seus recursos
2. Configure pipelines de dados específicos
3. Ajuste variáveis de ambiente

## 📚 Guias de Personalização

### 🏗️ Template de Arquitetura Medalhão

Todos os templates seguem a arquitetura medalhão com:

- **Bronze**: Dados brutos com mínimo processamento
- **Silver**: Dados limpos com SCD Tipo 2
- **Gold**: Dimensões e fatos para análise

### 🔄 Padrões SCD Tipo 2

Templates incluem implementação completa de:

- Versionamento histórico
- Chaves surrogate otimizadas
- Metadados de auditoria
- Validações de qualidade

### ⚡ Otimizações de Performance

- Particionamento inteligente
- Z-Ordering por chaves principais
- Cache para dados frequentemente acessados
- Compactação Delta Lake automática

## 🎨 Personalização por Domínio

### 🛒 E-commerce (Baseado em Olist)
- Dimensões: Customer, Product, Seller, Date
- Fatos: Sales, Reviews, Inventory
- Métricas: Revenue, Satisfaction, Performance

### 🏥 Healthcare
- Dimensões: Patient, Provider, Treatment, Date
- Fatos: Visits, Procedures, Outcomes
- Métricas: Quality, Cost, Efficiency

### 💰 Finance
- Dimensões: Account, Product, Channel, Date
- Fatos: Transactions, Balances, Risk
- Métricas: ROI, Risk Score, Growth

## 🔍 Checklist de Validação

- [ ] Dados carregados corretamente na Bronze
- [ ] Transformações Silver aplicam SCD Tipo 2
- [ ] Dimensões Gold têm registros "Unknown"
- [ ] Fatos têm integridade referencial
- [ ] Performance otimizada com particionamento
- [ ] Documentação atualizada
- [ ] Testes de qualidade passando

## 🚀 Próximos Passos

1. **Escolha um template** baseado no seu domínio
2. **Personalize** com seus dados e regras de negócio
3. **Teste** com dados de exemplo
4. **Documente** especificidades do seu workshop
5. **Compartilhe** com a comunidade

---

💡 **Dica**: Sempre teste templates com dados pequenos antes de aplicar em datasets grandes!