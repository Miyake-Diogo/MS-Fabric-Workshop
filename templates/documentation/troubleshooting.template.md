# 🚨 Troubleshooting Guide: Microsoft Fabric Workshop

## 📋 Guia de Resolução de Problemas

Este documento contém soluções para problemas comuns encontrados durante a execução de workshops Microsoft Fabric com **SCD Tipo 2**.

---

## 🥉 Problemas da Camada Bronze

### ❌ Erro: "Schema Mismatch"
**Sintoma**: Erro ao carregar arquivos com schemas diferentes
```
AnalysisException: Cannot merge incompatible schemas
```

**✅ Solução**:
```python
# Habilitar merge de schema
df.write \
  .mode("append") \
  .option("mergeSchema", "true") \
  .format("delta") \
  .save(bronze_path)
```

**🔧 Prevenção**: 
- Use schema explícito quando possível
- Monitore evolução de schema nos sistemas fonte

---

### ❌ Erro: "File Not Found"
**Sintoma**: Arquivo de dados não encontrado
```
FileNotFoundException: Path does not exist
```

**✅ Solução**:
```python
# Verificar existência antes de processar
if os.path.exists(source_path):
    df = spark.read.csv(source_path)
else:
    logger.warning(f"Arquivo não encontrado: {source_path}")
    # Implementar estratégia alternativa
```

**🔧 Prevenção**:
- Validar paths antes do processamento
- Implementar retry com backoff
- Configurar alertas para falhas de arquivo

---

### ❌ Erro: "OutOfMemory" durante ingestão
**Sintoma**: Spark fica sem memória ao processar arquivos grandes
```
OutOfMemoryError: Java heap space
```

**✅ Solução**:
```python
# Processar em batches menores
def process_large_file_in_chunks(file_path, chunk_size=10000):
    for chunk_df in pd.read_csv(file_path, chunksize=chunk_size):
        spark_df = spark.createDataFrame(chunk_df)
        # Processar chunk individual
        process_chunk(spark_df)

# Ou aumentar configurações Spark
spark.conf.set("spark.driver.memory", "8g")
spark.conf.set("spark.executor.memory", "8g")
```

---

## 🥈 Problemas da Camada Silver

### ❌ Erro: SCD Tipo 2 - Registros Duplicados Correntes
**Sintoma**: Múltiplos registros `is_current = true` para mesma chave natural
```sql
SELECT customer_id, COUNT(*) 
FROM silver_customers 
WHERE is_current = true 
GROUP BY customer_id 
HAVING COUNT(*) > 1
```

**✅ Solução**:
```python
# Debug: Identificar problema na lógica SCD2
def fix_duplicate_current_records(table_name, natural_key):
    # 1. Identificar registros problemáticos
    duplicates = spark.sql(f"""
        SELECT {natural_key}, MAX(version) as max_version
        FROM {table_name}
        WHERE is_current = true
        GROUP BY {natural_key}
        HAVING COUNT(*) > 1
    """)
    
    # 2. Corrigir: manter apenas a versão mais recente
    for row in duplicates.collect():
        key = row[natural_key]
        max_ver = row.max_version
        
        spark.sql(f"""
            UPDATE {table_name}
            SET is_current = false, end_date = current_date() - 1
            WHERE {natural_key} = '{key}' 
            AND is_current = true 
            AND version < {max_ver}
        """)
```

**🔧 Prevenção**:
- Validar lógica de merge SCD2
- Implementar testes unitários para SCD2
- Monitorar métricas de qualidade

---

### ❌ Erro: "Dates Inconsistency" 
**Sintoma**: `effective_date > end_date` em registros SCD2
```sql
SELECT COUNT(*) FROM silver_customers 
WHERE effective_date > end_date
```

**✅ Solução**:
```python
# Corrigir datas inconsistentes
def fix_date_inconsistency(table_name):
    spark.sql(f"""
        UPDATE {table_name}
        SET end_date = CASE 
            WHEN effective_date > end_date AND is_current = false 
            THEN date_add(effective_date, 365)  -- Assumir 1 ano de validade
            WHEN is_current = true 
            THEN '9999-12-31'
            ELSE end_date
        END
        WHERE effective_date > end_date
    """)
```

**🔧 Prevenção**:
- Validar datas durante transformação SCD2
- Implementar constraints de integridade
- Adicionar testes de qualidade específicos

---

### ❌ Erro: Performance Lenta em Transformações
**Sintoma**: Notebooks Silver demoram muito para executar

**✅ Solução**:
```python
# Otimizações de performance
# 1. Habilitar Adaptive Query Execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# 2. Otimizar joins
# Usar broadcast para tabelas pequenas (<200MB)
df_result = large_df.join(broadcast(small_df), "key")

# 3. Particionar adequadamente
df.write.partitionBy("effective_year", "is_current")

# 4. Usar cache para DataFrames reutilizados
df_cached = df.cache()
```

**🔧 Prevenção**:
- Monitorar tamanho das partições
- Implementar Z-ordering
- Revisar lógica de joins

---

## 🥇 Problemas da Camada Gold

### ❌ Erro: Chaves Surrogate Duplicadas
**Sintoma**: Chaves surrogate não são únicas
```sql
SELECT DimCustomerSK, COUNT(*) 
FROM DimCustomer 
GROUP BY DimCustomerSK 
HAVING COUNT(*) > 1
```

**✅ Solução**:
```python
# Regenerar chaves surrogate únicas
def fix_duplicate_surrogate_keys(dimension_name):
    table_name = f"Dim{dimension_name}"
    sk_column = f"Dim{dimension_name}SK"
    
    # Criar nova sequência única
    window_spec = Window.orderBy("natural_key", "effective_date", "version")
    
    df_fixed = spark.table(table_name).withColumn(
        f"{sk_column}_new",
        row_number().over(window_spec)
    ).drop(sk_column).withColumnRenamed(f"{sk_column}_new", sk_column)
    
    # Salvar corrigido
    df_fixed.write.mode("overwrite").saveAsTable(table_name)
```

**🔧 Prevenção**:
- Usar `row_number()` em vez de hash para chaves surrogate
- Implementar validação de unicidade
- Testes automatizados para integridade

---

### ❌ Erro: Missing Unknown Records
**Sintoma**: Fatos referenciando chaves que não existem nas dimensões
```sql
SELECT f.DimCustomerSK 
FROM FactSales f 
LEFT JOIN DimCustomer d ON f.DimCustomerSK = d.DimCustomerSK 
WHERE d.DimCustomerSK IS NULL
```

**✅ Solução**:
```python
# Adicionar registros Unknown faltantes
def create_missing_unknown_records():
    unknown_records = [
        {"DimCustomerSK": -1, "customer_id": "UNKNOWN", "customer_name": "Unknown"},
        {"DimProductSK": -1, "product_id": "UNKNOWN", "product_name": "Unknown"},
        # ... outras dimensões
    ]
    
    for record in unknown_records:
        dimension_name = [k for k in record.keys() if k.endswith("SK")][0].replace("SK", "")
        
        # Inserir se não existir
        spark.sql(f"""
            INSERT INTO {dimension_name}
            SELECT * FROM VALUES {tuple(record.values())}
            WHERE NOT EXISTS (
                SELECT 1 FROM {dimension_name} WHERE {dimension_name}SK = -1
            )
        """)
```

**🔧 Prevenção**:
- Sempre criar Unknown records primeiro
- Validar integridade referencial regularmente
- Implementar foreign key checks

---

### ❌ Erro: Z-Ordering Falha
**Sintoma**: Comando OPTIMIZE ZORDER falha
```
AnalysisException: Z-Ordering column not found
```

**✅ Solução**:
```python
# Verificar colunas antes de Z-ordering
def safe_zorder(table_name, columns):
    # Verificar se colunas existem
    table_columns = [col.name for col in spark.table(table_name).schema]
    valid_columns = [col for col in columns if col in table_columns]
    
    if valid_columns:
        spark.sql(f"OPTIMIZE {table_name} ZORDER BY ({', '.join(valid_columns)})")
        logger.info(f"✅ Z-ordering aplicado em {table_name}: {valid_columns}")
    else:
        logger.warning(f"⚠️ Nenhuma coluna válida para Z-ordering em {table_name}")
```

**🔧 Prevenção**:
- Validar schema antes de otimização
- Documentar colunas de Z-ordering por tabela
- Implementar retry em otimizações

---

## 🔧 Problemas de Configuração

### ❌ Erro: Lakehouse Connection Failed
**Sintoma**: Não consegue conectar ao Lakehouse
```
ConnectionException: Failed to connect to lakehouse
```

**✅ Solução**:
```python
# Verificar configurações do Lakehouse
def verify_lakehouse_connection():
    try:
        # Testar acesso
        spark.sql("SHOW DATABASES").show()
        print("✅ Conexão com Lakehouse OK")
    except Exception as e:
        print(f"❌ Erro de conexão: {str(e)}")
        
        # Verificações diagnósticas
        print("🔍 Verificando configurações...")
        print(f"Workspace: {spark.conf.get('spark.workspace.name', 'não configurado')}")
        print(f"Lakehouse: {spark.conf.get('spark.lakehouse.name', 'não configurado')}")
```

**🔧 Prevenção**:
- Documentar configurações necessárias
- Implementar health checks
- Validar permissões de acesso

---

### ❌ Erro: Insufficient Compute Resources  
**Sintoma**: Spark jobs falham por falta de recursos
```
ResourceException: Insufficient resources to run job
```

**✅ Solução**:
```python
# Otimizar configurações de recursos
def optimize_spark_config():
    # Para datasets pequenos/médios
    spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB")
    spark.conf.set("spark.sql.adaptive.coalescePartitions.minPartitionSize", "64MB")
    
    # Para datasets grandes
    spark.conf.set("spark.executor.memory", "8g")
    spark.conf.set("spark.executor.cores", "4")
    spark.conf.set("spark.driver.memory", "4g")
    
    # Otimizações gerais
    spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

**🔧 Prevenção**:
- Dimensionar recursos adequadamente
- Monitorar uso de recursos
- Implementar processamento adaptativo

---

## 📊 Problemas de Qualidade de Dados

### ❌ Erro: High Data Rejection Rate
**Sintoma**: Muitos registros rejeitados nas validações de qualidade

**✅ Solução**:
```python
# Análise detalhada de rejeições
def analyze_data_quality_issues(table_name):
    df = spark.table(table_name)
    
    print("📊 Análise de Qualidade de Dados:")
    print(f"Total de registros: {df.count():,}")
    
    # Verificar valores nulos por coluna
    for col_name in df.columns:
        null_count = df.filter(col(col_name).isNull()).count()
        null_pct = (null_count / df.count()) * 100
        if null_pct > 5:  # Mais de 5% nulos
            print(f"⚠️ {col_name}: {null_pct:.1f}% valores nulos")
    
    # Verificar duplicatas
    duplicates = df.count() - df.dropDuplicates().count()
    if duplicates > 0:
        print(f"⚠️ {duplicates:,} registros duplicados")
    
    # Verificar outliers em colunas numéricas
    numeric_columns = [col_name for col_name, data_type in df.dtypes 
                      if data_type in ['int', 'double', 'float', 'decimal']]
    
    for col_name in numeric_columns:
        stats = df.select(col_name).describe().collect()
        # Implementar lógica de detecção de outliers
```

**🔧 Prevenção**:
- Implementar validações incrementais
- Documentar regras de qualidade
- Monitorar tendências de qualidade

---

## 🚨 Problemas de Pipeline

### ❌ Erro: Pipeline Timeout
**Sintoma**: Pipeline para de responder ou excede tempo limite

**✅ Solução**:
```python
# Implementar processamento resiliente
def resilient_pipeline_execution(steps):
    for step_name, step_func in steps.items():
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f"🔄 Executando {step_name} (tentativa {retry_count + 1})")
                step_func()
                logger.info(f"✅ {step_name} concluído")
                break
                
            except Exception as e:
                retry_count += 1
                wait_time = 2 ** retry_count  # Backoff exponencial
                
                if retry_count < max_retries:
                    logger.warning(f"⚠️ {step_name} falhou, tentando novamente em {wait_time}s")
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ {step_name} falhou após {max_retries} tentativas: {str(e)}")
                    raise
```

**🔧 Prevenção**:
- Implementar checkpoints em pipelines longos
- Configurar timeouts apropriados
- Monitorar performance de steps

---

## 🔍 Debug e Diagnóstico

### 🔧 Ferramentas de Debug

```python
# 1. Debug de Schema
def debug_schema_differences(df1, df2, name1="df1", name2="df2"):
    schema1 = set([(f.name, f.dataType) for f in df1.schema])
    schema2 = set([(f.name, f.dataType) for f in df2.schema])
    
    only_in_1 = schema1 - schema2
    only_in_2 = schema2 - schema1
    
    if only_in_1:
        print(f"🔍 Colunas apenas em {name1}: {only_in_1}")
    if only_in_2:
        print(f"🔍 Colunas apenas em {name2}: {only_in_2}")

# 2. Debug de Performance
def debug_query_performance(query):
    # Habilitar métricas detalhadas
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.logLevel", "INFO")
    
    # Executar com explain
    df = spark.sql(query)
    df.explain(mode="extended")
    
    return df

# 3. Debug de Dados
def debug_data_issues(df, sample_size=1000):
    print(f"📊 Análise de amostra ({sample_size} registros):")
    
    # Schema
    print("\n🏗️ Schema:")
    df.printSchema()
    
    # Estatísticas básicas
    print("\n📈 Estatísticas:")
    df.describe().show()
    
    # Amostra de dados
    print("\n📋 Amostra:")
    df.limit(sample_size).show(20, truncate=False)
    
    # Valores únicos em colunas categóricas
    categorical_cols = [col_name for col_name, data_type in df.dtypes 
                       if data_type == 'string']
    
    for col_name in categorical_cols[:5]:  # Primeiras 5 colunas
        unique_count = df.select(col_name).distinct().count()
        print(f"🔍 {col_name}: {unique_count} valores únicos")
```

---

## 📞 Quando Buscar Ajuda

### 🆘 Escalonamento de Problemas

1. **Nível 1 - Auto-resolução**:
   - Consultar este guia de troubleshooting
   - Verificar logs do Spark
   - Executar scripts de diagnóstico

2. **Nível 2 - Documentação**:
   - [Architecture Guide](architecture-guide.md)
   - [Microsoft Fabric Documentation](https://docs.microsoft.com/fabric)
   - [Delta Lake Documentation](https://delta.io/docs)

3. **Nível 3 - Comunidade**:
   - Stack Overflow com tags `microsoft-fabric`, `pyspark`, `delta-lake`
   - GitHub Issues do projeto
   - Microsoft Tech Community

4. **Nível 4 - Suporte**:
   - Microsoft Support (para problemas de plataforma)
   - Equipe de desenvolvimento do workshop

---

## 📝 Checklist de Troubleshooting

### ✅ Antes de Reportar Problemas

- [ ] Verificar logs completos do Spark
- [ ] Executar scripts de diagnóstico
- [ ] Testar com dataset menor
- [ ] Verificar configurações do ambiente
- [ ] Documentar passos para reproduzir
- [ ] Coletar informações do ambiente (versões, configurações)
- [ ] Tentar soluções deste guia

### ✅ Informações para Incluir no Report

- [ ] Mensagem de erro completa
- [ ] Logs relevantes do Spark
- [ ] Configurações do ambiente
- [ ] Tamanho e características do dataset
- [ ] Passos para reproduzir o problema
- [ ] Tentativas de solução já realizadas

---

💡 **Dica**: Mantenha este guia atualizado com novos problemas e soluções encontrados durante os workshops!