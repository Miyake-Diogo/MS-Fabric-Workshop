# 🏗️ Estrutura Padronizada de Workshop

## 📁 Hierarquia de Pastas

### 🏗️ Estrutura Obrigatória
```
📦 workshop-name/
├── 📄 README.md                          # Documentação principal
├── 📄 pyproject.toml                     # Configurações Python/UV
├── 📄 uv.lock                           # Lock file de dependências
├── 📄 LICENSE                           # Licença do projeto
├── 📁 assets/                           # Recursos do workshop
│   ├── 📁 data/                         # Datasets
│   │   ├── 📁 bronze/                   # Dados brutos
│   │   ├── 📁 silver/                   # Dados limpos (opcional)
│   │   └── 📁 gold/                     # Dados analíticos (opcional)
│   ├── 📁 images/                       # Imagens para documentação
│   ├── 📁 gifs/                         # GIFs demonstrativos
│   └── 📁 schemas/                      # Esquemas de dados
├── 📁 notebooks/                        # Notebooks Jupyter
│   ├── 📁 01-bronze/                    # Ingestão de dados
│   ├── 📁 02-silver/                    # Transformações limpeza
│   ├── 📁 03-gold/                      # Modelagem dimensional
│   └── 📁 04-analytics/                 # Análises e relatórios
├── 📁 scripts/                          # Scripts auxiliares
│   ├── 📁 setup/                        # Scripts de configuração
│   ├── 📁 utils/                        # Utilitários reutilizáveis
│   └── 📁 tests/                        # Testes automatizados
├── 📁 docs/                             # Documentação adicional
│   ├── 📄 architecture.md               # Arquitetura do workshop
│   ├── 📄 troubleshooting.md            # Guia de problemas
│   └── 📄 learning-objectives.md        # Objetivos de aprendizado
├── 📁 templates/                        # Templates reutilizáveis
└── 📁 infra/                           # Infraestrutura (opcional)
    ├── 📁 bicep/                        # Templates Bicep
    └── 📁 terraform/                    # Templates Terraform
```

---

## 📝 Convenções de Nomenclatura

### 📁 Pastas
- **snake_case**: para nomes de pastas
- **números com prefixo**: para ordenação lógica (01-, 02-, etc.)
- **inglês**: idioma padrão para estrutura técnica
- **descritivo**: nome deve indicar claramente o conteúdo

### 📄 Arquivos
- **kebab-case**: para arquivos de documentação (`learning-objectives.md`)
- **PascalCase**: para notebooks principais (`LoadDataToLakehouse.ipynb`)
- **snake_case**: para scripts Python (`data_validation.py`)
- **UPPERCASE**: para arquivos de configuração (`README.md`, `LICENSE`)

### 🏷️ Notebooks
```
[Número]-[Ação][Entidade][Destino].ipynb

Exemplos:
- 01-LoadOlistDataToLakehouse.ipynb
- 02-SilverTransformations.ipynb
- 03-GoldDimensionalModeling.ipynb
- 04-BusinessIntelligenceAnalytics.ipynb
```

### 🏷️ Tabelas Delta
```
[Camada][Entidade]

Exemplos:
- bronze_customers (Bronze)
- silver_customers (Silver com SCD2)
- dim_customer (Gold - Dimensão)
- fact_sales (Gold - Fato)
```

---

## 🎯 Padrões por Camada

### 🥉 Camada Bronze
**Objetivo**: Ingestão e armazenamento de dados brutos com auditoria

**Estrutura do Notebook**:
```python
# 1. CONFIGURAÇÃO E IMPORTS
import pyspark.sql.functions as F
from pyspark.sql.types import *
from delta.tables import DeltaTable
import logging

# 2. CONFIGURAÇÃO DE LOGGING
logger = logging.getLogger(__name__)

# 3. CONFIGURAÇÕES DO LAKEHOUSE
lakehouse_name = "WorkshopLakehouse"
source_data_path = "/path/to/source"

# 4. FUNÇÕES UTILITÁRIAS
def add_audit_columns(df):
    """Adiciona colunas de auditoria padrão"""
    return df.withColumn("ingestion_timestamp", F.current_timestamp()) \
             .withColumn("source_system", F.lit("source_name")) \
             .withColumn("batch_id", F.lit("batch_identifier"))

# 5. VALIDAÇÃO DE QUALIDADE
def validate_bronze_data(df, table_name):
    """Validações básicas para dados bronze"""
    record_count = df.count()
    null_columns = [col for col in df.columns if df.filter(F.col(col).isNull()).count() == record_count]
    
    logger.info(f"✅ {table_name}: {record_count:,} registros carregados")
    if null_columns:
        logger.warning(f"⚠️ Colunas completamente nulas: {null_columns}")

# 6. PROCESSAMENTO PRINCIPAL
def load_to_bronze(source_path, target_table, file_format="csv"):
    """Carrega dados para camada Bronze"""
    # Implementar lógica de ingestão
    pass

# 7. EXECUÇÃO
if __name__ == "__main__":
    # Executar pipeline bronze
    pass
```

**Características Obrigatórias**:
- ✅ Colunas de auditoria (`ingestion_timestamp`, `source_system`, `batch_id`)
- ✅ Validação básica de qualidade
- ✅ Logging estruturado
- ✅ Tratamento de exceções
- ✅ Documentação inline

---

### 🥈 Camada Silver
**Objetivo**: Limpeza, padronização e implementação de SCD Tipo 2

**Estrutura do Notebook**:
```python
# 1. CONFIGURAÇÃO E IMPORTS
import pyspark.sql.functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window
from delta.tables import DeltaTable
import logging

# 2. CONFIGURAÇÕES SCD TIPO 2
scd2_columns = ["effective_date", "end_date", "is_current", "version", "hash_key"]

# 3. FUNÇÕES SCD TIPO 2
def add_scd2_columns(df, natural_key_cols):
    """Adiciona colunas SCD Tipo 2 padrão"""
    # Implementar lógica SCD2
    pass

def apply_business_rules(df, entity_name):
    """Aplica regras de negócio específicas"""
    # Implementar regras por entidade
    pass

def perform_scd2_merge(source_df, target_table, natural_keys):
    """Executa merge com lógica SCD Tipo 2"""
    # Implementar merge SCD2
    pass

# 4. VALIDAÇÕES DE QUALIDADE
def validate_scd2_integrity(table_name, natural_key):
    """Valida integridade SCD Tipo 2"""
    # Verificar duplicatas de registros correntes
    # Verificar consistência de datas
    # Verificar sequência de versões
    pass

# 5. OTIMIZAÇÕES
def optimize_silver_table(table_name, zorder_columns):
    """Aplica otimizações Delta Lake"""
    spark.sql(f"OPTIMIZE {table_name} ZORDER BY ({', '.join(zorder_columns)})")
    spark.sql(f"VACUUM {table_name} RETAIN 168 HOURS")  # 7 dias

# 6. PROCESSAMENTO PRINCIPAL
def process_entity_to_silver(entity_name, natural_keys, business_rules_func):
    """Processa entidade para Silver com SCD2"""
    # Implementar pipeline completo
    pass

# 7. EXECUÇÃO
if __name__ == "__main__":
    # Processar todas as entidades
    pass
```

**Características Obrigatórias**:
- ✅ SCD Tipo 2 completo (effective_date, end_date, is_current, version)
- ✅ Regras de negócio específicas por entidade
- ✅ Validações de integridade de dados
- ✅ Hash keys para detecção de mudanças
- ✅ Otimizações de performance (particionamento, Z-ordering)

---

### 🥇 Camada Gold
**Objetivo**: Modelagem dimensional para analytics com SCD Tipo 2

**Estrutura do Notebook**:
```python
# 1. CONFIGURAÇÃO E IMPORTS
import pyspark.sql.functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window
from delta.tables import DeltaTable
import logging

# 2. FUNÇÕES DE MODELAGEM DIMENSIONAL
def create_dimension_scd2(source_table, dimension_name, natural_key, attributes):
    """Cria dimensão com SCD Tipo 2"""
    # Implementar criação de dimensão
    pass

def generate_surrogate_key(df, dimension_name):
    """Gera chaves surrogate únicas"""
    # Implementar geração de SK
    pass

def create_unknown_record(dimension_name, schema):
    """Cria registro Unknown padrão"""
    # Implementar registro Unknown
    pass

def add_business_intelligence_attributes(df, dimension_type):
    """Adiciona atributos de BI específicos"""
    # Implementar atributos de BI
    pass

# 3. DIMENSÕES TEMPORAIS
def create_dim_date(start_date="2020-01-01", end_date="2030-12-31"):
    """Cria dimensão temporal completa"""
    # Implementar dimensão de data
    pass

# 4. VALIDAÇÕES DE INTEGRIDADE
def validate_dimension_integrity(dimension_name):
    """Valida integridade dimensional"""
    # Verificar unicidade de chaves surrogate
    # Verificar Unknown records
    # Verificar SCD2 consistency
    pass

# 5. MÉTRICAS DE QUALIDADE
def generate_dimension_metrics(dimension_name):
    """Gera métricas de qualidade dimensional"""
    # Contar registros por status (current/historical)
    # Calcular distribuição de versões
    # Identificar dimensões com muitas mudanças
    pass

# 6. PROCESSAMENTO PRINCIPAL
def create_all_dimensions():
    """Cria todas as dimensões do modelo"""
    # Implementar criação sequencial
    pass

# 7. EXECUÇÃO
if __name__ == "__main__":
    # Executar modelagem dimensional
    pass
```

**Características Obrigatórias**:
- ✅ Chaves surrogate únicas
- ✅ Registros Unknown (-1)
- ✅ SCD Tipo 2 preservado das camadas inferiores
- ✅ Atributos de business intelligence
- ✅ Dimensão temporal completa
- ✅ Validações de integridade referencial

---

## 📚 Documentação Obrigatória

### 📄 README.md
```markdown
# 📊 Workshop: [Nome do Workshop]

## 🎯 Objetivos de Aprendizado
- [ ] Objetivo 1
- [ ] Objetivo 2
- [ ] Objetivo 3

## 🏗️ Arquitetura
- Camada Bronze: [Descrição]
- Camada Silver: [Descrição] 
- Camada Gold: [Descrição]

## 🚀 Setup Rápido
1. Passo 1
2. Passo 2
3. Passo 3

## 📊 Datasets
| Dataset | Tamanho | Descrição |
|---------|---------|-----------|
| Dataset 1 | XXX MB | Descrição |

## 📝 Notebooks
1. **01-Bronze**: Ingestão de dados
2. **02-Silver**: Transformações com SCD2
3. **03-Gold**: Modelagem dimensional
4. **04-Analytics**: Análises de negócio

## 🔧 Troubleshooting
Ver [troubleshooting.md](docs/troubleshooting.md)
```

### 📄 pyproject.toml
```toml
[project]
name = "workshop-name"
version = "1.0.0"
description = "Microsoft Fabric Workshop"
requires-python = ">=3.8"

dependencies = [
    "pyspark>=3.4.0",
    "delta-spark>=2.4.0",
    "pandas>=1.5.0",
    "jupyter>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "flake8>=5.0.0",
]

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py38']

[tool.pytest.ini_options]
testpaths = ["scripts/tests"]
python_files = ["test_*.py"]
```

---

## 🧪 Testes Obrigatórios

### 🔬 Testes Unitários
```python
# scripts/tests/test_scd2_functions.py
import pytest
from pyspark.sql import SparkSession
from scripts.utils.scd2_utils import add_scd2_columns, perform_scd2_merge

class TestSCD2Functions:
    @pytest.fixture
    def spark(self):
        return SparkSession.builder.appName("test").getOrCreate()
    
    def test_add_scd2_columns(self, spark):
        """Testa adição de colunas SCD2"""
        # Implementar teste
        pass
    
    def test_scd2_merge_logic(self, spark):
        """Testa lógica de merge SCD2"""
        # Implementar teste
        pass
    
    def test_business_rules_validation(self, spark):
        """Testa validação de regras de negócio"""
        # Implementar teste
        pass
```

### 🔍 Testes de Qualidade
```python
# scripts/tests/test_data_quality.py
import pytest
from scripts.utils.quality_checks import validate_scd2_integrity

class TestDataQuality:
    def test_no_duplicate_current_records(self):
        """Testa ausência de registros correntes duplicados"""
        # Implementar teste
        pass
    
    def test_date_consistency(self):
        """Testa consistência de datas SCD2"""
        # Implementar teste
        pass
    
    def test_surrogate_key_uniqueness(self):
        """Testa unicidade de chaves surrogate"""
        # Implementar teste
        pass
```

---

## 📋 Checklist de Qualidade

### ✅ Antes de Publicar Workshop

**Estrutura**:
- [ ] Hierarquia de pastas seguindo padrão
- [ ] Nomenclatura consistente
- [ ] Documentação completa (README, troubleshooting, architecture)
- [ ] Licença incluída

**Notebooks**:
- [ ] SCD Tipo 2 implementado corretamente
- [ ] Regras de negócio documentadas
- [ ] Validações de qualidade incluídas
- [ ] Logging estruturado
- [ ] Otimizações de performance aplicadas

**Qualidade**:
- [ ] Testes unitários passando
- [ ] Testes de qualidade de dados passando
- [ ] Validação com datasets de teste
- [ ] Performance adequada (< 10min por notebook)

**Documentação**:
- [ ] Objetivos de aprendizado claros
- [ ] Setup instructions testadas
- [ ] Troubleshooting guide atualizado
- [ ] Screenshots/GIFs demonstrativos

**Reutilização**:
- [ ] Templates extraídos e generalizados
- [ ] Códigos parametrizados
- [ ] Funções utilitárias documentadas
- [ ] Configurações externalizadas

---

## 🚀 Deploy e Distribuição

### 📦 Empacotamento
```bash
# Validar estrutura
uv run scripts/validate_structure.py

# Executar testes
uv run pytest scripts/tests/

# Criar package
uv build

# Publicar no repositório interno
git tag v1.0.0
git push origin v1.0.0
```

### 📋 Release Checklist
- [ ] Versão atualizada em pyproject.toml
- [ ] CHANGELOG.md atualizado
- [ ] Testes passando
- [ ] Documentação revisada
- [ ] Tag de release criada
- [ ] Assets empacotados

---

💡 **Lembre-se**: Esta estrutura padronizada garante qualidade, reutilização e facilita a manutenção de todos os workshops Microsoft Fabric!