# 📊 Template: Workshop README

## 🎯 {WORKSHOP_NAME}

> **Descrição**: {WORKSHOP_DESCRIPTION}
> 
> **Objetivo**: {WORKSHOP_OBJECTIVE}
> 
> **Duração Estimada**: {ESTIMATED_DURATION}

---

## 🏗️ Arquitetura do Projeto

### 📋 Visão Geral
Este workshop implementa uma arquitetura **Medalhão (Medallion)** completa com **SCD Tipo 2** para rastreamento histórico de dados.

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│    Bronze   │───▶│    Silver    │───▶│    Gold     │
│ (Raw Data)  │    │ (Cleaned +   │    │ (Analytics  │
│             │    │  SCD Type 2) │    │  Ready)     │
└─────────────┘    └──────────────┘    └─────────────┘
```

### 🎨 Camadas de Dados

| Camada | Propósito | Características |
|--------|-----------|-----------------|
| **🥉 Bronze** | Ingestão de dados brutos | • Dados "como-são" do source<br>• Auditoria completa<br>• Particionamento por data |
| **🥈 Silver** | Limpeza e SCD Tipo 2 | • Validação de qualidade<br>• Regras de negócio<br>• Versionamento histórico |
| **🥇 Gold** | Analytics e BI | • Dimensões e fatos<br>• Chaves surrogate<br>• Business Intelligence |

---

## 📁 Estrutura do Projeto

```
{WORKSHOP_NAME}/
├── 📓 notebooks/               # Notebooks de processamento
│   ├── 01-bronze-ingestion.ipynb
│   ├── 02-silver-transformations.ipynb
│   ├── 03-gold-dimensions.ipynb
│   └── 04-gold-facts.ipynb
├── 📊 assets/                  # Recursos do workshop
│   ├── data/                   # Dados de exemplo
│   ├── images/                 # Diagramas e imagens
│   └── diagrams/               # Arquiteturas visuais
├── 🚀 pipelines/              # Pipelines de dados
│   └── data-pipeline.json
├── 📚 docs/                   # Documentação
│   ├── setup-guide.md
│   ├── troubleshooting.md
│   └── architecture.md
└── 🔧 scripts/               # Scripts utilitários
    ├── setup.py
    └── validate.py
```

---

## 🚀 Primeiros Passos

### 1. 📋 Pré-requisitos

- [ ] **Microsoft Fabric**: Workspace ativo
- [ ] **Lakehouse**: Criado e configurado
- [ ] **Compute**: Spark pool disponível
- [ ] **Dados**: Dataset {DATASET_NAME} carregado

### 2. 🔧 Configuração Inicial

1. **Clone/Download** este workshop
2. **Configure** variáveis no notebook de configuração
3. **Execute** notebooks na ordem sequencial
4. **Valide** resultados em cada camada

### 3. 📓 Ordem de Execução

| Ordem | Notebook | Tempo Estimado | Descrição |
|-------|----------|----------------|-----------|
| 1️⃣ | `01-bronze-ingestion.ipynb` | ~15 min | Carregar dados brutos |
| 2️⃣ | `02-silver-transformations.ipynb` | ~25 min | Limpeza + SCD Tipo 2 |
| 3️⃣ | `03-gold-dimensions.ipynb` | ~20 min | Criar dimensões |
| 4️⃣ | `04-gold-facts.ipynb` | ~20 min | Criar fatos |

---

## 🎯 Objetivos de Aprendizado

Ao completar este workshop, você será capaz de:

- [ ] **Implementar** arquitetura Medalhão no Microsoft Fabric
- [ ] **Aplicar** SCD Tipo 2 para versionamento histórico  
- [ ] **Criar** dimensões e fatos otimizados
- [ ] **Configurar** particionamento e performance
- [ ] **Validar** qualidade dos dados em cada camada
- [ ] **Monitorar** pipelines de dados

---

## 📊 Dataset: {DATASET_NAME}

### 🎯 Contexto do Negócio
{BUSINESS_CONTEXT}

### 📋 Entidades Principais
{MAIN_ENTITIES}

### 🔗 Relacionamentos
{ENTITY_RELATIONSHIPS}

---

## 🏗️ Padrões SCD Tipo 2

### 📅 Versionamento Histórico
- **Effective Date**: Início da validade
- **End Date**: Fim da validade (9999-12-31 para registros correntes)
- **Is Current**: Flag booleana para registro atual
- **Version**: Número sequencial da versão

### 🔑 Chaves Surrogate
- **Formato**: `DimensaoSK` (ex: `DimCustomerSK`)
- **Tipo**: Integer sequencial único
- **Unknown**: ID -1 para tratamento de chaves órfãs

### 🎯 Business Intelligence
- **Atributos Derivados**: Calculados automaticamente
- **Categorização**: Segmentação inteligente
- **Métricas**: KPIs pré-calculados

---

## ⚡ Otimizações de Performance

### 📂 Particionamento
```python
# Exemplo de particionamento otimizado
.partitionBy("effective_year", "data_source")
```

### 🚀 Z-Ordering
```python
# Otimização para consultas frequentes
OPTIMIZE table_name ZORDER BY (natural_key, effective_date)
```

### 💾 Compactação
```python
# Compactação automática Delta Lake
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
```

---

## 🔍 Validações e Qualidade

### ✅ Testes de Integridade
- **Unicidade**: Chaves surrogate únicas
- **Consistência**: Datas válidas em SCD Tipo 2
- **Completude**: Registros Unknown disponíveis
- **Relacionamentos**: Integridade referencial

### 📊 Métricas de Qualidade
- **Score de Qualidade**: % de registros válidos
- **Cobertura**: % de dados sem valores nulos
- **Duplicação**: % de registros duplicados
- **Conformidade**: % aderente às regras de negócio

---

## 🚨 Troubleshooting

### ❌ Problemas Comuns

| Problema | Solução |
|----------|---------|
| **Erro de Schema** | Verificar compatibilidade entre Bronze e Silver |
| **Performance Lenta** | Revisar particionamento e Z-ordering |
| **Dados Duplicados** | Verificar lógica de SCD Tipo 2 |
| **Chaves Órfãs** | Confirmar registros Unknown nas dimensões |

### 🆘 Onde Buscar Ajuda
- **Documentação**: `/docs/troubleshooting.md`
- **Logs**: Verificar logs do Spark para detalhes
- **Comunidade**: {COMMUNITY_LINKS}

---

## 📈 Próximos Passos

### 🎯 Extensões Sugeridas
1. **Streaming**: Implementar processamento em tempo real
2. **ML**: Adicionar modelos de machine learning
3. **Governança**: Implementar data lineage
4. **Alertas**: Configurar monitoramento proativo

### 🔄 Atualizações Incrementais
1. **Novos Dados**: Como processar updates incrementais
2. **Schema Evolution**: Gerenciar mudanças de schema
3. **Histórico**: Manter versões antigas das dimensões

---

## 👥 Contribuições

Contribuições são bem-vindas! Por favor:

1. **Fork** este repositório
2. **Crie** uma branch para sua feature
3. **Implemente** seguindo os padrões estabelecidos
4. **Teste** com dados de exemplo
5. **Submeta** um Pull Request

### 📝 Guidelines de Contribuição
- Seguir padrões SCD Tipo 2 estabelecidos
- Documentar mudanças no código
- Incluir testes de validação
- Atualizar documentação conforme necessário

---

## 📚 Recursos Adicionais

### 🔗 Links Úteis
- [Microsoft Fabric Documentation](https://docs.microsoft.com/fabric)
- [Delta Lake Guide](https://delta.io/docs)
- [SCD Type 2 Best Practices](link-to-scd-guide)
- [Data Warehousing Patterns](link-to-patterns)

### 📖 Bibliografia
- {REFERENCE_1}
- {REFERENCE_2}
- {REFERENCE_3}

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 📧 Contato

**Mantenedor**: {MAINTAINER_NAME}  
**Email**: {MAINTAINER_EMAIL}  
**Workshop**: {WORKSHOP_NAME}  
**Versão**: {VERSION}  
**Última Atualização**: {LAST_UPDATE}

---

💡 **Dica**: Sempre teste com dados pequenos antes de processar datasets grandes!