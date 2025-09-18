# 🏗️ Guia de Arquitetura: Microsoft Fabric Workshop

## 📋 Visão Geral Arquitetural

Este documento descreve os padrões arquiteturais estabelecidos para workshops Microsoft Fabric, focando na implementação de **SCD Tipo 2** e melhores práticas de **Data Engineering**.

---

## 🎯 Princípios Fundamentais

### 1. 🏛️ Arquitetura Medalhão
```
📥 Source Systems  →  🥉 Bronze  →  🥈 Silver  →  🥇 Gold  →  📊 Analytics
     Raw Data         Ingestion    Cleaned      Star Schema   Reports & ML
```

### 2. 🔄 SCD Tipo 2 (Slowly Changing Dimensions)
- **Versionamento Histórico**: Preserva todo o histórico de mudanças
- **Auditoria Completa**: Rastreia quando e como os dados mudaram
- **Performance Otimizada**: Chaves surrogate para joins eficientes

### 3. ⚡ Performance por Design
- **Particionamento Inteligente**: Por data e dimensões principais
- **Z-Ordering**: Otimização para consultas frequentes  
- **Compactação Delta**: Manutenção automática de arquivos

---

## 🥉 Camada Bronze: Ingestão

### 🎯 Objetivo
Capturar dados brutos exatamente como recebidos do sistema de origem.

### 📋 Características
- **Fidelidade**: Dados "como-são" sem transformações
- **Auditoria**: Metadados completos de rastreabilidade
- **Flexibilidade**: Suporte a múltiplos formatos (CSV, JSON, Parquet)
- **Tolerância**: Aceita dados com problemas para análise posterior

### 🏗️ Estrutura Padrão
```python
bronze_schema = {
    # Colunas originais (preservadas integralmente)
    "original_columns": "*",
    
    # Metadados de auditoria
    "processing_timestamp": "timestamp",
    "processing_date": "date", 
    "source_system": "string",
    "file_name": "string",
    "ingestion_method": "string",
    "record_hash": "string"
}
```

### 📊 Particionamento Bronze
```python
# Padrão recomendado
.partitionBy("processing_date", "source_system")

# Para volumes altos
.partitionBy("processing_date", "source_system", "data_type")
```

---

## 🥈 Camada Silver: Transformação + SCD Tipo 2

### 🎯 Objetivo
Limpar, validar e aplicar SCD Tipo 2 para rastreamento histórico.

### 📋 Características
- **Qualidade**: Validações e limpeza de dados
- **Consistência**: Regras de negócio aplicadas
- **Versionamento**: SCD Tipo 2 completo
- **Performance**: Otimizado para consultas analíticas

### 🏗️ Estrutura SCD Tipo 2
```python
scd2_schema = {
    # Chave natural (business key)
    "natural_key": "string",
    
    # Dados de negócio (podem mudar)
    "business_attributes": "...",
    
    # Controle SCD Tipo 2
    "effective_date": "date",      # Início da validade
    "end_date": "date",            # Fim da validade (9999-12-31 para correntes)
    "is_current": "boolean",       # Flag de registro corrente
    "version": "integer",          # Número da versão
    
    # Auditoria
    "created_date": "timestamp",
    "updated_date": "timestamp",
    
    # Particionamento
    "effective_year": "integer",
    "effective_month": "integer"
}
```

### 🔄 Lógica SCD Tipo 2
```python
def apply_scd2_logic(new_data, existing_data, scd_columns):
    """
    1. Identificar mudanças nos scd_columns
    2. Expirar registros antigos (is_current = false, end_date = hoje-1)
    3. Inserir novos registros (version = version_anterior + 1)
    4. Manter registros inalterados
    """
```

### 📊 Particionamento Silver
```python
# Otimizado para consultas temporais
.partitionBy("effective_year", "is_current")

# Para volumes muito altos
.partitionBy("effective_year", "effective_month", "entity_type")
```

---

## 🥇 Camada Gold: Star Schema

### 🎯 Objetivo
Criar estrutura dimensional otimizada para analytics e BI.

### 📋 Características
- **Star Schema**: Dimensões e fatos claramente separados
- **Chaves Surrogate**: Performance otimizada para joins
- **Business Intelligence**: Atributos derivados pré-calculados
- **Registros Unknown**: Tratamento de chaves órfãs

### 🏗️ Estrutura de Dimensões
```python
dimension_schema = {
    # Chave surrogate (primary key)
    "DimensionSK": "integer",
    
    # Chave natural (business key)
    "natural_key": "string",
    "business_key": "string",
    
    # Atributos de negócio
    "business_attributes": "...",
    
    # Atributos derivados (BI)
    "derived_attributes": "...",
    
    # Controle SCD Tipo 2 (herdado do Silver)
    "effective_date": "date",
    "end_date": "date", 
    "is_current": "boolean",
    "version": "integer",
    
    # Metadados
    "dimension_name": "string",
    "source_system": "string",
    "processing_date": "date"
}
```

### 🏗️ Estrutura de Fatos
```python
fact_schema = {
    # Chaves surrogate das dimensões
    "DimCustomerSK": "integer",
    "DimProductSK": "integer", 
    "DimDateSK": "integer",
    "DimSellerSK": "integer",
    
    # Chaves degeneradas (se aplicável)
    "order_id": "string",
    "transaction_id": "string",
    
    # Métricas (measures)
    "quantity": "decimal",
    "unit_price": "decimal",
    "total_amount": "decimal",
    "discount_amount": "decimal",
    
    # Métricas derivadas
    "net_amount": "decimal",
    "profit_margin": "decimal",
    
    # Metadados
    "fact_name": "string",
    "processing_date": "date"
}
```

### 📊 Particionamento Gold
```python
# Dimensões: por effective_year
.partitionBy("effective_year")

# Fatos: por data da transação
.partitionBy("transaction_year", "transaction_month")

# Z-Ordering para performance
OPTIMIZE table_name ZORDER BY (primary_dimension_sk, date_sk)
```

---

## 🔑 Padrões de Chaves

### 🎯 Chaves Surrogate
```python
# Geração de chaves surrogate otimizada
def generate_surrogate_key(df, dimension_name):
    window_spec = Window.orderBy("natural_key", "effective_date", "version")
    return df.withColumn(
        f"{dimension_name}SK",
        row_number().over(window_spec)
    )
```

### ❓ Registros Unknown
```python
# Padrão para registros Unknown
UNKNOWN_RECORD = {
    "DimensionSK": -1,
    "natural_key": "UNKNOWN",
    "business_key": "UNKNOWN", 
    "name": "Unknown",
    "effective_date": "1900-01-01",
    "end_date": "9999-12-31",
    "is_current": True,
    "version": 1
}
```

---

## 🚀 Otimizações de Performance

### 📂 Estratégias de Particionamento

| Camada | Estratégia | Benefício |
|--------|------------|-----------|
| Bronze | `processing_date` | Filtragem por período de ingestão |
| Silver | `effective_year + is_current` | Consultas SCD Tipo 2 eficientes |
| Gold Dim | `effective_year` | Consultas históricas otimizadas |
| Gold Fact | `transaction_date` | Análises por período |

### ⚡ Z-Ordering

```python
# Dimensões: otimizar por chaves principais
OPTIMIZE DimCustomer ZORDER BY (customer_id, effective_date)

# Fatos: otimizar por chaves mais consultadas
OPTIMIZE FactSales ZORDER BY (DimCustomerSK, DimDateSK)
```

### 💾 Compactação e Manutenção

```python
# Configurações recomendadas
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.maxFileSize", "134217728")  # 128MB
```

---

## 📊 Padrões de Qualidade

### ✅ Validações Bronze
- **Completude**: Todos os arquivos processados
- **Integridade**: Hashes de registros únicos
- **Rastreabilidade**: Metadados de auditoria completos

### ✅ Validações Silver
- **Qualidade**: Dados limpos e válidos
- **Consistência**: Regras de negócio aplicadas
- **SCD Integridade**: Versões e datas consistentes

### ✅ Validações Gold
- **Unicidade**: Chaves surrogate únicas
- **Relacionamentos**: Integridade referencial
- **Unknown Records**: Disponíveis em todas as dimensões

---

## 🔄 Padrões de Processamento

### 🎯 Batch Processing
```python
# Padrão para processamento batch
def process_batch_scd2(table_name, processing_date):
    # 1. Carregar novos dados
    # 2. Identificar mudanças  
    # 3. Aplicar SCD Tipo 2
    # 4. Validar qualidade
    # 5. Salvar com otimizações
```

### ⚡ Streaming Processing
```python
# Padrão para streaming (opcional)
def process_streaming_scd2(stream_df):
    return stream_df.writeStream \
        .foreachBatch(lambda batch, epoch: process_scd2_batch(batch, epoch)) \
        .outputMode("append") \
        .start()
```

---

## 🎨 Convenções de Nomenclatura

### 📋 Tabelas
```
# Padrão: {layer}_{entity_name}
bronze_customers
silver_customers  
DimCustomer       # Gold dimensions em PascalCase
FactSales         # Gold facts em PascalCase
```

### 🔑 Colunas
```
# Chaves surrogate: {DimensionName}SK
DimCustomerSK, DimProductSK

# Chaves naturais: {entity}_id
customer_id, product_id

# SCD Tipo 2: padrão fixo
effective_date, end_date, is_current, version

# Metadados: prefixo claro
processing_date, source_system, created_date
```

### 📁 Caminhos
```
# Estrutura padronizada
/lakehouse/default/Tables/
├── bronze/
│   ├── customers/
│   ├── products/
│   └── orders/
├── silver/
│   ├── customers/
│   ├── products/
│   └── orders/
└── gold/
    ├── DimCustomer/
    ├── DimProduct/
    └── FactSales/
```

---

## 🚨 Padrões de Erro e Recovery

### ❌ Tratamento de Erros
```python
def robust_processing(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Erro em {func.__name__}: {str(e)}")
        # Implementar estratégia de recuperação
        return handle_processing_error(e, func, args, kwargs)
```

### 🔄 Estratégias de Recovery
1. **Retry**: Tentar novamente com backoff exponencial
2. **Rollback**: Reverter para estado anterior válido
3. **Skip**: Pular registros problemáticos e continuar
4. **Alert**: Notificar administradores para intervenção manual

---

## 📈 Monitoramento e Observabilidade

### 📊 Métricas Essenciais
- **Qualidade**: % de registros válidos por tabela
- **Latência**: Tempo de processamento por camada
- **Volume**: Número de registros processados
- **Erro**: Taxa de falhas por pipeline

### 🔍 Logs Estruturados
```python
# Padrão de logging
logger.info(f"📊 {table_name} - Processamento: {input_count} → {output_count} ({quality_score:.2f}% qualidade)")
```

---

## 🎯 Checklist de Implementação

### ✅ Bronze Layer
- [ ] Metadados de auditoria completos
- [ ] Particionamento por data de processamento
- [ ] Validação de completude de arquivos
- [ ] Hash de registros para detecção de mudanças

### ✅ Silver Layer  
- [ ] SCD Tipo 2 implementado corretamente
- [ ] Validações de qualidade aplicadas
- [ ] Regras de negócio específicas do domínio
- [ ] Particionamento otimizado para consultas

### ✅ Gold Layer
- [ ] Chaves surrogate únicas e sequenciais
- [ ] Registros Unknown disponíveis
- [ ] Business Intelligence attributes calculados
- [ ] Z-ordering aplicado para performance

### ✅ Geral
- [ ] Convenções de nomenclatura seguidas
- [ ] Documentação atualizada
- [ ] Testes de validação implementados
- [ ] Monitoramento configurado

---

💡 **Próximo**: [Setup Guide](setup-guide.md) | [Troubleshooting](troubleshooting.md)