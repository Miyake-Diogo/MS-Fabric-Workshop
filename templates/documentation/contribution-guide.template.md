# 🤝 Guia de Contribuição - Microsoft Fabric Workshop

## 🎯 Bem-vindo ao Projeto!

Este guia define padrões e processos para contribuir com workshops Microsoft Fabric de alta qualidade, focados em **SCD Tipo 2** e **arquitetura medallão**.

---

## 📋 Processo de Contribuição

### 🔄 Workflow Padrão

1. **🍴 Fork & Clone**
   ```bash
   git clone https://github.com/seu-usuario/workshop-repo.git
   cd workshop-repo
   ```

2. **🌟 Criar Branch Feature**
   ```bash
   git checkout -b feature/nova-funcionalidade
   # ou
   git checkout -b fix/correcao-bug
   # ou  
   git checkout -b workshop/novo-workshop-nome
   ```

3. **💻 Desenvolvimento**
   - Seguir [Estrutura Padronizada](workshop-structure.template.md)
   - Implementar SCD Tipo 2 corretamente
   - Adicionar testes e validações
   - Documentar adequadamente

4. **🧪 Validação Local**
   ```bash
   # Executar testes
   uv run pytest scripts/tests/
   
   # Validar estrutura
   uv run scripts/validate_structure.py
   
   # Verificar qualidade de dados
   uv run scripts/quality_checks.py
   ```

5. **📤 Pull Request**
   - Criar PR descritivo
   - Aguardar review
   - Aplicar feedback
   - Merge após aprovação

---

## 🎯 Tipos de Contribuição

### 🆕 Novo Workshop
**Quando usar**: Criando workshop completo do zero

**Estrutura da Branch**: `workshop/nome-do-workshop`

**Checklist**:
- [ ] Seguir [estrutura padronizada](workshop-structure.template.md)
- [ ] Implementar SCD Tipo 2 em todas as camadas
- [ ] Incluir datasets de exemplo
- [ ] Documentação completa (README, troubleshooting, objectives)
- [ ] Testes unitários e de qualidade
- [ ] GIFs/screenshots demonstrativos

**Template de Commit**:
```
feat(workshop): add [nome-workshop] with SCD Type 2

- Implementa arquitetura medallão completa
- SCD Tipo 2 em camadas Silver e Gold  
- Inclui [X] notebooks com [Y] entidades
- Cobertura de testes: [Z]%
- Datasets: [lista dos datasets]

Closes #issue-number
```

---

### 🔧 Melhoria de Funcionalidade
**Quando usar**: Melhorando workshops existentes

**Estrutura da Branch**: `feature/descricao-melhoria`

**Tipos Comuns**:
- Otimizações de performance
- Novos tipos de validação SCD2
- Melhores práticas de Delta Lake
- Funções utilitárias reutilizáveis

**Checklist**:
- [ ] Manter compatibilidade com workshops existentes
- [ ] Atualizar testes relacionados
- [ ] Documentar mudanças
- [ ] Validar performance

**Template de Commit**:
```
feat(scd2): improve performance with adaptive partitioning

- Reduz tempo de processamento em 40%
- Implementa particionamento adaptativo
- Adiciona Z-ordering automático
- Mantém compatibilidade com SCD2 existente

Benchmarks:
- Antes: 15min para 1M registros
- Depois: 9min para 1M registros
```

---

### 🐛 Correção de Bug
**Quando usar**: Corrigindo problemas identificados

**Estrutura da Branch**: `fix/descricao-problema`

**Tipos Comuns**:
- Erros na lógica SCD Tipo 2
- Problemas de performance
- Bugs de validação de dados
- Erros de configuração

**Checklist**:
- [ ] Reproduzir o bug localmente
- [ ] Identificar causa raiz
- [ ] Implementar correção mínima
- [ ] Adicionar teste regressivo
- [ ] Validar correção

**Template de Commit**:
```
fix(scd2): resolve duplicate current records issue

- Corrige lógica de merge SCD2 que permitia duplicatas
- Adiciona validação de integridade pós-merge
- Inclui teste regressivo para cenário específico

Problema: registros com is_current=true duplicados
Causa: condição de merge incompleta
Solução: validar versão máxima antes de marcar current

Fixes #issue-number
```

---

### 📚 Melhoria de Documentação
**Quando usar**: Atualizando ou melhorando documentação

**Estrutura da Branch**: `docs/descricao-melhoria`

**Tipos Comuns**:
- Atualizar troubleshooting guide
- Melhorar README de workshops
- Documentar novas funcionalidades
- Adicionar exemplos de uso

**Checklist**:
- [ ] Linguagem clara e objetiva
- [ ] Exemplos práticos
- [ ] Screenshots/GIFs quando relevante
- [ ] Links funcionais
- [ ] Formatação Markdown correta

---

## 🏗️ Padrões de Código

### 🐍 Python/PySpark

```python
# ✅ BOM: Função bem documentada com SCD2
def perform_scd2_merge(source_df, target_table, natural_keys, effective_date_col="effective_date"):
    """
    Executa merge SCD Tipo 2 entre source e target.
    
    Args:
        source_df (DataFrame): Dados de origem
        target_table (str): Nome da tabela de destino  
        natural_keys (list): Chaves naturais para join
        effective_date_col (str): Coluna de data efetiva
        
    Returns:
        dict: Estatísticas do merge (inserted, updated, unchanged)
        
    Example:
        >>> stats = perform_scd2_merge(df, "silver_customers", ["customer_id"])
        >>> print(f"Inseridos: {stats['inserted']}")
    """
    # Implementação aqui...
    pass

# ❌ RUIM: Função sem documentação e parâmetros hardcoded
def merge_data(df, table):
    # Faz merge dos dados
    pass
```

### 📊 Nomenclatura de Tabelas

```python
# ✅ BOM: Nomenclatura consistente
bronze_customers = "bronze_customers"
silver_customers = "silver_customers"  
dim_customer = "dim_customer"
fact_sales = "fact_sales"

# ❌ RUIM: Nomenclatura inconsistente
raw_customer_data = "customers_raw"
cleaned_customers = "CustomersCleaned"
customer_dimension = "DimCust"
```

### 🔧 Configurações

```python
# ✅ BOM: Configurações externalizadas
CONFIG = {
    "lakehouse_name": "WorkshopLakehouse",
    "bronze_schema": "bronze",
    "silver_schema": "silver", 
    "gold_schema": "gold",
    "scd2_columns": ["effective_date", "end_date", "is_current", "version"],
    "optimization": {
        "auto_compact": True,
        "z_order_enabled": True,
        "vacuum_retention_hours": 168
    }
}

# ❌ RUIM: Valores hardcoded
spark.sql("CREATE TABLE bronze.customers ...")
```

### 🧪 Testes

```python
# ✅ BOM: Teste específico e claro
def test_scd2_no_duplicate_current_records():
    """Testa que não há registros correntes duplicados após merge SCD2"""
    # Arrange
    source_data = create_test_customer_changes()
    
    # Act
    perform_scd2_merge(source_data, "test_customers", ["customer_id"])
    
    # Assert
    duplicates = spark.sql("""
        SELECT customer_id, COUNT(*) as count
        FROM test_customers 
        WHERE is_current = true
        GROUP BY customer_id
        HAVING COUNT(*) > 1
    """).count()
    
    assert duplicates == 0, "Encontrados registros correntes duplicados"

# ❌ RUIM: Teste genérico sem validação específica
def test_merge():
    # Testa se merge funciona
    assert True
```

---

## 📋 Code Review Guidelines

### 🔍 O que Revisar

**Arquitetura SCD Tipo 2**:
- [ ] Implementação correta de effective_date, end_date, is_current, version
- [ ] Lógica de merge preserva histórico
- [ ] Chaves surrogate únicas nas dimensões
- [ ] Unknown records (-1) implementados

**Performance**:
- [ ] Particionamento adequado (por effective_date geralmente)
- [ ] Z-ordering em colunas de consulta frequente
- [ ] Uso de broadcast joins quando apropriado
- [ ] Cache para DataFrames reutilizados

**Qualidade de Dados**:
- [ ] Validações de integridade SCD2
- [ ] Detecção de duplicatas de registros correntes
- [ ] Consistência de datas (effective_date <= end_date)
- [ ] Validação de chaves estrangeiras

**Testes**:
- [ ] Cobertura adequada (mínimo 80%)
- [ ] Testes de regressão para bugs conhecidos
- [ ] Validação de dados de entrada e saída
- [ ] Testes de performance básicos

**Documentação**:
- [ ] README atualizado
- [ ] Docstrings em funções públicas
- [ ] Comentários em lógica complexa
- [ ] Exemplos de uso

### 💬 Feedback Construtivo

**✅ BOM**:
```
A lógica SCD2 está correta, mas sugiro extrair a validação 
de integridade para uma função separada para reutilização:

```python
def validate_scd2_integrity(table_name, natural_key):
    # validação aqui
```

Isso facilitaria testes e manutenção.
```

**❌ RUIM**:
```
Código está ruim, refaça.
```

---

## 🚀 Performance Guidelines

### ⚡ Otimizações Obrigatórias

```python
# 1. Particionamento por data efetiva
df.write \
  .partitionBy("effective_year") \
  .format("delta") \
  .mode("overwrite") \
  .saveAsTable("silver_customers")

# 2. Z-ordering em colunas de consulta
spark.sql("OPTIMIZE silver_customers ZORDER BY (customer_id, is_current)")

# 3. Vacuum periódico (7 dias retenção)
spark.sql("VACUUM silver_customers RETAIN 168 HOURS")

# 4. Adaptive Query Execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

### 📊 Benchmarks de Referência

| Operação | Dataset | Tempo Esperado | Configuração |
|----------|---------|----------------|--------------|
| Bronze Ingestion | 1M registros | < 2min | Standard compute |
| Silver SCD2 | 1M registros | < 5min | Standard compute |
| Gold Dimensions | 5 dimensões | < 3min | Standard compute |
| Full Pipeline | Olist completo | < 15min | Standard compute |

---

## 🔒 Segurança e Compliance

### 🛡️ Dados Sensíveis

```python
# ✅ BOM: Mascarar dados sensíveis
def mask_sensitive_data(df):
    """Mascara campos sensíveis para ambientes de desenvolvimento"""
    return df.withColumn(
        "email", 
        F.regexp_replace(F.col("email"), r"(.{2}).*(@.*)", r"$1****$2")
    ).withColumn(
        "phone",
        F.regexp_replace(F.col("phone"), r"(\d{2})\d{6}(\d{2})", r"$1******$2")
    )

# ❌ RUIM: Expor dados reais
df.show(100, truncate=False)  # Pode mostrar emails reais
```

### 📝 Auditoria

```python
# ✅ BOM: Logging de auditoria
def audit_scd2_merge(table_name, stats):
    """Registra auditoria de operação SCD2"""
    audit_record = {
        "timestamp": datetime.now(),
        "operation": "scd2_merge",
        "table": table_name,
        "records_inserted": stats["inserted"],
        "records_updated": stats["updated"],
        "user": spark.sql("SELECT current_user()").collect()[0][0]
    }
    
    # Salvar em tabela de auditoria
    audit_df = spark.createDataFrame([audit_record])
    audit_df.write.mode("append").saveAsTable("audit.operations")
```

---

## 📊 Métricas de Qualidade

### 📈 KPIs de Workshop

- **Completude**: % notebooks executados com sucesso
- **Performance**: Tempo total < benchmark definido
- **Qualidade**: 0 violações de integridade SCD2
- **Cobertura**: > 80% cobertura de testes
- **Documentação**: README score > 90%

### 🔍 Validações Automáticas

```python
# CI/CD Pipeline validations
def validate_workshop_quality():
    """Valida qualidade geral do workshop"""
    checks = {
        "structure": validate_folder_structure(),
        "scd2_integrity": validate_all_scd2_tables(),
        "performance": run_performance_benchmarks(),
        "tests": run_test_suite(),
        "documentation": validate_documentation()
    }
    
    failed_checks = [k for k, v in checks.items() if not v]
    
    if failed_checks:
        raise ValueError(f"Falha nas validações: {failed_checks}")
    
    return True
```

---

## 🚀 Deploy e Release

### 📦 Processo de Release

1. **🏷️ Versionamento Semântico**
   - `MAJOR.MINOR.PATCH` (ex: 2.1.3)
   - MAJOR: mudanças incompatíveis
   - MINOR: novas funcionalidades compatíveis  
   - PATCH: correções de bugs

2. **📋 Release Checklist**
   ```bash
   # 1. Atualizar versão
   echo "version = '2.1.0'" > version.py
   
   # 2. Executar validações completas
   uv run scripts/validate_all.py
   
   # 3. Gerar CHANGELOG
   uv run scripts/generate_changelog.py
   
   # 4. Criar tag e release
   git tag -a v2.1.0 -m "Release 2.1.0: SCD2 performance improvements"
   git push origin v2.1.0
   
   # 5. Publicar assets
   gh release create v2.1.0 --title "v2.1.0" --notes-file CHANGELOG.md
   ```

3. **📢 Comunicação**
   - Atualizar documentação principal
   - Notificar stakeholders sobre mudanças
   - Publicar no canal de comunicação da equipe

---

## 🆘 Suporte e Comunidade

### 💬 Canais de Comunicação

- **🐛 Issues**: Para bugs e solicitações de funcionalidades
- **💭 Discussions**: Para dúvidas e ideias gerais
- **📧 Email**: Para questões sensíveis ou privadas
- **💬 Teams**: Para comunicação rápida da equipe

### 🏷️ Labels Padrão

| Label | Uso | Prioridade |
|-------|-----|------------|
| `bug` | Problemas funcionais | Alta |
| `enhancement` | Melhorias | Média |
| `documentation` | Docs | Baixa |
| `scd2` | Relacionado a SCD Tipo 2 | Alta |
| `performance` | Otimizações | Média |
| `good-first-issue` | Para novos contribuidores | Baixa |

### 🎯 Mentoria

**Para Novos Contribuidores**:
- Comece com issues marcadas como `good-first-issue`
- Leia este guia completamente
- Execute workshops existentes primeiro
- Peça ajuda quando necessário

**Para Mentores**:
- Seja paciente e construtivo
- Foque no aprendizado, não apenas no resultado
- Compartilhe contexto e reasoning
- Celebre contribuições, mesmo pequenas

---

## 🙏 Reconhecimento

### 🏆 Tipos de Contribuição Valorizadas

- **🏗️ Arquitetural**: Melhorias significativas na arquitetura
- **⚡ Performance**: Otimizações mensuráveis  
- **🧪 Qualidade**: Melhoria na cobertura de testes
- **📚 Educacional**: Documentação e exemplos claros
- **🐛 Manutenção**: Correções de bugs importantes
- **🆕 Inovação**: Novas funcionalidades relevantes

### 📜 Hall of Fame

Contributors que fizeram impacto significativo serão reconhecidos no README principal com:
- Nome/avatar
- Tipo de contribuição principal
- Link para contribuições relevantes

---

## 📞 Contato

Para dúvidas sobre este guia:
- Abra uma Discussion no repositório
- Entre em contato com a equipe de maintainers
- Consulte a documentação adicional em `/docs/`

---

🎉 **Obrigado por contribuir para melhorar a qualidade dos workshops Microsoft Fabric!**

*Juntos construímos soluções de dados mais robustas e educativas.* 🚀