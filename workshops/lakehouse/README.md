# 🏗️ Workshop: Fabric Lakehouse

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Arquitetura Medallion](#arquitetura-medallion)
- [Passo-a-Passo](#passo-a-passo)
- [Notebooks e Execução](#notebooks-e-execução)
- [Datasets Utilizados](#datasets-utilizados)
- [Troubleshooting](#troubleshooting)
- [Próximos Passos](#próximos-passos)

## 🎯 Visão Geral

Este workshop ensina como implementar uma arquitetura **Medallion** (Bronze, Silver, Gold) usando o **Microsoft Fabric Lakehouse**. Você aprenderá a:

- ✅ Carregar dados brutos (Bronze)
- ✅ Aplicar transformações e limpeza (Silver)  
- ✅ Criar tabelas dimensionais e fatos (Gold)
- ✅ Otimizar performance e armazenamento
- ✅ Consultar dados com SQL Analytics

### 🏆 Resultados Esperados
Ao final do workshop, você terá:
- Um Lakehouse funcional com arquitetura medallion
- Dados organizados e consultáveis
- Conhecimento prático de ETL no Fabric
- Base para análises avançadas e relatórios

## 🔧 Pré-requisitos

### Acesso e Permissões
- ✅ **Microsoft Fabric** (trial ou licença completa)
- ✅ **Workspace** com capacidade suficiente
- ✅ Permissões de **Contributor** ou **Admin** no workspace

### Conhecimentos Técnicos
- 🟢 **Básico:** SQL e conceitos de data warehousing
- 🟡 **Intermediário:** Python/PySpark (para customizações)
- 🔵 **Diferencial:** Experiência com Azure Data Factory

### Ferramentas Locais
- 📱 **Navegador moderno** (Chrome, Edge, Firefox)
- 💻 **VS Code** (opcional, para desenvolvimento local)
- 🐍 **Python 3.11+** (opcional, para testes locais)

## 🏗️ Arquitetura Medallion

### Conceito
A arquitetura Medallion organiza dados em camadas progressivamente refinadas:

```
📁 Bronze (Raw Data)
    ├── Dados brutos, sem transformação
    ├── Formato original (CSV, JSON, Parquet)
    └── Histórico completo preservado

📁 Silver (Cleaned Data)  
    ├── Dados limpos e padronizados
    ├── Duplicatas removidas
    ├── Tipos de dados corrigidos
    └── Validações aplicadas

📁 Gold (Business Data)
    ├── Tabelas dimensionais (Dims)
    ├── Tabelas fatos (Facts)
    ├── Agregações pré-calculadas
    └── Pronto para análise/BI
```

### Benefícios
- 🔄 **Reprocessamento** fácil a partir de qualquer camada
- 🎯 **Qualidade** progressiva dos dados
- ⚡ **Performance** otimizada para consumo
- 🛡️ **Governança** e auditoria simplificadas

## 🚀 Passo-a-Passo

### Etapa 1: Preparação do Ambiente

1. **Acesse o Microsoft Fabric**
   ```
   Portal: https://app.fabric.microsoft.com
   ```

2. **Crie ou Acesse seu Workspace**
   - Clique em "Workspaces" no menu lateral
   - Selecione workspace existente ou crie novo
   - Verifique se tem capacidade disponível

3. **Clone este Repositório**
   ```bash
   git clone https://github.com/Miyake-Diogo/MS-Fabric-Workshop.git
   cd MS-Fabric-Workshop/workshops/lakehouse
   ```

### Etapa 2: Criação do Lakehouse

1. **No Fabric Portal:**
   - Vá para "Data Engineering" experience
   - Clique em "New" → "Lakehouse"
   - Nome: `LakehouseWorkshop`

2. **Verifique a Estrutura:**
   ```
   LakehouseWorkshop/
   ├── Files/           # Arquivos não estruturados
   ├── Tables/          # Tabelas gerenciadas
   └── Schemas/         # Esquemas customizados
   ```

### Etapa 3: Upload dos Datasets

1. **Upload Manual via Portal:**
   - Navegue para "Files" no Lakehouse
   - Crie pasta `bronze/`
   - Upload dos datasets em `workshops/lakehouse/data/`

2. **Estrutura Recomendada:**
   ```
   Files/
   └── bronze/
       ├── advworks/
       │   ├── DimCustomer.parquet
       │   ├── DimProduct.parquet
       │   └── FactInternetSales.parquet
       └── olist/
           ├── olist_customers_dataset.csv
           ├── olist_orders_dataset.csv
           └── olist_products_dataset.csv
   ```

### Etapa 4: Upload e Configuração dos Notebooks

1. **No Fabric Portal:**
   - Vá para "Data Engineering"
   - Clique em "New" → "Notebook"
   - Upload do arquivo `.ipynb`

2. **Ordem de Upload:**
   ```
   01-LoadADVWorksDataToLH.ipynb    # Primeiro
   01-LoadOlistDataToLH.ipynb       # Paralelo ao anterior
   02-SilverTransformations.ipynb   # Segundo
   03-GoldTransformationsDim.ipynb  # Terceiro  
   04-GoldTransformationsFact.ipynb # Quarto
   05-GoldOptimizations.ipynb       # Quinto
   ```

3. **Conectar Notebooks ao Lakehouse:**
   - Em cada notebook: "Add Lakehouse"
   - Selecione "Existing Lakehouse"
   - Escolha `LakehouseWorkshop`

## 📓 Notebooks e Execução

### 01-LoadADVWorksDataToLH.ipynb
**Objetivo:** Carregar dados AdventureWorks na camada Bronze

**O que faz:**
```python
# Leitura de arquivos Parquet
df_customers = spark.read.parquet("/Files/bronze/advworks/DimCustomer.parquet")

# Salvamento como tabela Bronze
df_customers.write.mode("overwrite").saveAsTable("bronze_dim_customer")
```

**Tempo estimado:** 15 minutos

### 01-LoadOlistDataToLH.ipynb  
**Objetivo:** Carregar dados Olist na camada Bronze

**O que faz:**
```python
# Leitura de arquivos CSV
df_orders = spark.read.csv("/Files/bronze/olist/olist_orders_dataset.csv", header=True)

# Inferência de schema e limpeza básica
df_orders = df_orders.dropDuplicates()

# Salvamento como tabela Bronze
df_orders.write.mode("overwrite").saveAsTable("bronze_orders")
```

**Tempo estimado:** 15 minutos

### 02-SilverTransformations.ipynb
**Objetivo:** Transformar dados Bronze em Silver

**Principais transformações:**
- 🧹 Limpeza de dados nulos e inválidos
- 📊 Padronização de tipos de dados
- 🔄 Remoção de duplicatas
- ✅ Validações de qualidade

**Exemplo:**
```python
# Limpeza e padronização
df_silver = (df_bronze
    .filter(col("order_status").isNotNull())
    .withColumn("order_purchase_timestamp", 
                to_timestamp("order_purchase_timestamp"))
    .withColumn("customer_unique_id", 
                upper(trim("customer_unique_id")))
)

df_silver.write.mode("overwrite").saveAsTable("silver_orders")
```

**Tempo estimado:** 30 minutos

### 03-GoldTransformationsDim.ipynb
**Objetivo:** Criar tabelas dimensionais

**Dimensões criadas:**
- `dim_customer` - Dados de clientes
- `dim_product` - Catálogo de produtos  
- `dim_date` - Calendário temporal
- `dim_geography` - Informações geográficas

**Exemplo:**
```python
# Criação da dimensão Customer
dim_customer = (df_silver_customers
    .select(
        "customer_id",
        "customer_unique_id", 
        "customer_city",
        "customer_state"
    )
    .distinct()
    .withColumn("customer_key", monotonically_increasing_id())
)

dim_customer.write.mode("overwrite").saveAsTable("gold_dim_customer")
```

**Tempo estimado:** 45 minutos

### 04-GoldTransformationsFact.ipynb
**Objetivo:** Criar tabelas fatos

**Fatos criados:**
- `fact_sales` - Transações de vendas
- `fact_orders` - Pedidos detalhados

**Exemplo:**
```python
# Junção com dimensões para criar fact table
fact_sales = (df_silver_sales
    .join(dim_customer, "customer_id")
    .join(dim_product, "product_id")  
    .join(dim_date, "order_date")
    .select(
        "customer_key",
        "product_key", 
        "date_key",
        "sales_amount",
        "quantity"
    )
)

fact_sales.write.mode("overwrite").saveAsTable("gold_fact_sales")
```

**Tempo estimado:** 45 minutos

### 05-GoldOptimizations.ipynb
**Objetivo:** Otimizar performance e armazenamento

**Otimizações aplicadas:**
- 🗂️ **Particionamento** por data
- 📊 **Z-Ordering** em colunas frequentes
- 🗃️ **Delta table** optimizations
- 📈 **Estatísticas** atualizadas

**Exemplo:**
```python
# Otimização com Z-Order
spark.sql("""
    OPTIMIZE gold_fact_sales 
    ZORDER BY (date_key, customer_key)
""")

# Vacuum para remover arquivos antigos
spark.sql("VACUUM gold_fact_sales RETAIN 168 HOURS")
```

**Tempo estimado:** 30 minutos

## 📊 Datasets Utilizados

### AdventureWorks
**Origem:** Microsoft sample database
**Domínio:** Vendas de bicicletas
**Tamanho:** ~50MB

**Principais tabelas:**
- `DimCustomer` - 18,484 clientes
- `DimProduct` - 606 produtos
- `FactInternetSales` - 60,398 vendas

### Olist
**Origem:** Dataset público brasileiro
**Domínio:** E-commerce
**Tamanho:** ~150MB

**Principais tabelas:**
- `olist_customers_dataset` - 99,441 clientes
- `olist_orders_dataset` - 99,441 pedidos
- `olist_products_dataset` - 32,951 produtos

## 🔧 Troubleshooting

### Problemas Comuns

#### Erro: "Table already exists"
**Solução:**
```python
# Use mode overwrite
df.write.mode("overwrite").saveAsTable("table_name")
```

#### Erro: "Lakehouse not found"
**Solução:**
1. Verifique se o notebook está conectado ao Lakehouse
2. Use "Add Lakehouse" → "Existing Lakehouse"

#### Performance lenta
**Solução:**
```python
# Otimize as tabelas
spark.sql("OPTIMIZE table_name")

# Use cache para DataFrames reutilizados
df.cache()
```

#### Erro de memória
**Solução:**
```python
# Processe em lotes menores
df.repartition(10).write.saveAsTable("table_name")

# Use lazy evaluation
df.write.option("maxRecordsPerFile", 100000)
```

### Verificação de Qualidade

#### Validar carregamento
```sql
-- Verificar contagem de registros
SELECT COUNT(*) FROM bronze_dim_customer;

-- Verificar dados nulos
SELECT 
    COUNT(*) as total,
    COUNT(customer_id) as non_null_customers
FROM bronze_dim_customer;
```

#### Validar transformações
```sql
-- Comparar Bronze vs Silver
SELECT 
    'Bronze' as layer, COUNT(*) as record_count 
FROM bronze_orders
UNION ALL
SELECT 
    'Silver' as layer, COUNT(*) as record_count 
FROM silver_orders;
```

## 🎯 Próximos Passos

### Exploração Avançada
1. **Power BI Integration**
   - Conecte diretamente às tabelas Gold
   - Crie dashboards e relatórios

2. **Real-time Analytics**
   - Configure streaming de dados
   - Implemente KQL queries

3. **Machine Learning**
   - Use dados Gold para treinar modelos
   - Implemente MLOps pipelines

### Otimizações Adicionais
- Configure **Data Pipelines** para automação
- Implemente **Data Quality** monitoring
- Adicione **Data Lineage** tracking

### Recursos Relacionados
- [Workshop Data Agents](fabric-data-agents.md)
- [Deployment Guide](../deployment/manual-setup.md)
- [Architecture Overview](../architecture/overview.md)

---

**🎉 Parabéns!** Você completou o workshop Lakehouse e agora tem uma base sólida para análises avançadas com Microsoft Fabric.