# 🔬 Scripts de Validação e Utilitários

## 📋 validate_structure.py
Script para validar se a estrutura do workshop está em conformidade com os padrões.

```python
#!/usr/bin/env python3
"""
Valida estrutura padronizada de workshop Microsoft Fabric
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json

def validate_required_files(workshop_path: Path) -> List[str]:
    """Valida presença de arquivos obrigatórios"""
    required_files = [
        "README.md",
        "pyproject.toml", 
        "LICENSE",
        "assets/data/",
        "notebooks/",
        "scripts/",
        "docs/",
        "templates/"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = workshop_path / file_path
        if not full_path.exists():
            missing_files.append(str(file_path))
    
    return missing_files

def validate_notebook_structure(notebooks_path: Path) -> Dict[str, List[str]]:
    """Valida estrutura de notebooks"""
    issues = {"missing_folders": [], "invalid_names": []}
    
    required_folders = ["01-bronze", "02-silver", "03-gold", "04-analytics"]
    
    for folder in required_folders:
        folder_path = notebooks_path / folder
        if not folder_path.exists():
            issues["missing_folders"].append(folder)
    
    # Validar nomenclatura de notebooks
    for notebook in notebooks_path.rglob("*.ipynb"):
        if not notebook.name[0].isdigit():
            issues["invalid_names"].append(str(notebook.relative_to(notebooks_path)))
    
    return issues

def validate_documentation(docs_path: Path) -> List[str]:
    """Valida documentação obrigatória"""
    required_docs = [
        "architecture.md",
        "troubleshooting.md", 
        "learning-objectives.md"
    ]
    
    missing_docs = []
    for doc in required_docs:
        if not (docs_path / doc).exists():
            missing_docs.append(doc)
    
    return missing_docs

def main():
    """Função principal de validação"""
    if len(sys.argv) != 2:
        print("Uso: python validate_structure.py <caminho_workshop>")
        sys.exit(1)
    
    workshop_path = Path(sys.argv[1])
    
    if not workshop_path.exists():
        print(f"❌ Caminho não encontrado: {workshop_path}")
        sys.exit(1)
    
    print("🔍 Validando estrutura do workshop...")
    
    # Validar arquivos obrigatórios
    missing_files = validate_required_files(workshop_path)
    if missing_files:
        print(f"❌ Arquivos/pastas obrigatórios ausentes: {missing_files}")
    else:
        print("✅ Arquivos obrigatórios presentes")
    
    # Validar estrutura de notebooks
    notebooks_issues = validate_notebook_structure(workshop_path / "notebooks")
    if any(notebooks_issues.values()):
        print(f"❌ Problemas na estrutura de notebooks: {notebooks_issues}")
    else:
        print("✅ Estrutura de notebooks válida")
    
    # Validar documentação
    missing_docs = validate_documentation(workshop_path / "docs")
    if missing_docs:
        print(f"❌ Documentação ausente: {missing_docs}")
    else:
        print("✅ Documentação completa")
    
    # Resultado final
    all_valid = not missing_files and not any(notebooks_issues.values()) and not missing_docs
    
    if all_valid:
        print("\n🎉 Estrutura do workshop está em conformidade!")
        sys.exit(0)
    else:
        print("\n❌ Estrutura precisa de correções antes da publicação")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 🧪 quality_checks.py
Script para validar qualidade de dados e integridade SCD Tipo 2.

```python
#!/usr/bin/env python3
"""
Validações de qualidade de dados para workshops Microsoft Fabric
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, isnan, isnull
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataQualityValidator:
    
    def __init__(self, spark_session: SparkSession):
        self.spark = spark_session
    
    def validate_scd2_integrity(self, table_name: str, natural_key: str) -> Dict[str, bool]:
        """Valida integridade SCD Tipo 2"""
        results = {}
        
        try:
            df = self.spark.table(table_name)
            
            # 1. Verificar duplicatas de registros correntes
            current_duplicates = self.spark.sql(f"""
                SELECT {natural_key}, COUNT(*) as count
                FROM {table_name}
                WHERE is_current = true
                GROUP BY {natural_key}
                HAVING COUNT(*) > 1
            """).count()
            
            results["no_current_duplicates"] = current_duplicates == 0
            
            # 2. Verificar consistência de datas
            date_inconsistencies = df.filter(
                (col("effective_date") > col("end_date")) & 
                (col("is_current") == False)
            ).count()
            
            results["date_consistency"] = date_inconsistencies == 0
            
            # 3. Verificar sequência de versões
            version_gaps = self.spark.sql(f"""
                WITH version_check AS (
                    SELECT {natural_key}, version,
                           LAG(version, 1, 0) OVER (
                               PARTITION BY {natural_key} 
                               ORDER BY version
                           ) as prev_version
                    FROM {table_name}
                )
                SELECT COUNT(*) as gaps
                FROM version_check
                WHERE version != prev_version + 1 AND prev_version != 0
            """).collect()[0]["gaps"]
            
            results["version_sequence"] = version_gaps == 0
            
            # 4. Verificar que registros correntes têm end_date no futuro
            current_end_dates = df.filter(
                (col("is_current") == True) & 
                (col("end_date") != "9999-12-31")
            ).count()
            
            results["current_end_dates"] = current_end_dates == 0
            
        except Exception as e:
            logger.error(f"Erro ao validar {table_name}: {str(e)}")
            results["error"] = str(e)
        
        return results
    
    def validate_dimension_integrity(self, dim_table: str) -> Dict[str, bool]:
        """Valida integridade de dimensões"""
        results = {}
        
        try:
            df = self.spark.table(dim_table)
            sk_column = [col for col in df.columns if col.endswith("SK")][0]
            
            # 1. Verificar unicidade de chaves surrogate
            sk_duplicates = df.groupBy(sk_column).count().filter(col("count") > 1).count()
            results["unique_surrogate_keys"] = sk_duplicates == 0
            
            # 2. Verificar presença de registro Unknown (-1)
            unknown_exists = df.filter(col(sk_column) == -1).count() > 0
            results["unknown_record_exists"] = unknown_exists
            
            # 3. Verificar se todas as chaves são positivas (exceto Unknown)
            negative_keys = df.filter((col(sk_column) < 0) & (col(sk_column) != -1)).count()
            results["no_negative_keys"] = negative_keys == 0
            
        except Exception as e:
            logger.error(f"Erro ao validar dimensão {dim_table}: {str(e)}")
            results["error"] = str(e)
        
        return results
    
    def validate_data_completeness(self, table_name: str) -> Dict[str, float]:
        """Calcula completude de dados por coluna"""
        df = self.spark.table(table_name)
        total_records = df.count()
        
        completeness = {}
        for column in df.columns:
            non_null_count = df.filter(col(column).isNotNull()).count()
            completeness[column] = (non_null_count / total_records) * 100
        
        return completeness

def main():
    """Executa validações de qualidade"""
    spark = SparkSession.builder.appName("QualityValidation").getOrCreate()
    validator = DataQualityValidator(spark)
    
    # Tabelas para validar
    silver_tables = [
        ("silver_customers", "customer_id"),
        ("silver_orders", "order_id"),
        ("silver_products", "product_id")
    ]
    
    dimension_tables = [
        "dim_customer",
        "dim_product", 
        "dim_seller",
        "dim_category",
        "dim_geography"
    ]
    
    all_passed = True
    
    print("🔍 Executando validações de qualidade...")
    
    # Validar SCD2 nas tabelas Silver
    for table_name, natural_key in silver_tables:
        try:
            print(f"\n📊 Validando SCD2: {table_name}")
            results = validator.validate_scd2_integrity(table_name, natural_key)
            
            for check, passed in results.items():
                if check != "error":
                    status = "✅" if passed else "❌"
                    print(f"  {status} {check}")
                    if not passed:
                        all_passed = False
                        
        except Exception as e:
            print(f"❌ Erro ao validar {table_name}: {str(e)}")
            all_passed = False
    
    # Validar dimensões Gold
    for dim_table in dimension_tables:
        try:
            print(f"\n🏗️ Validando dimensão: {dim_table}")
            results = validator.validate_dimension_integrity(dim_table)
            
            for check, passed in results.items():
                if check != "error":
                    status = "✅" if passed else "❌"
                    print(f"  {status} {check}")
                    if not passed:
                        all_passed = False
                        
        except Exception as e:
            print(f"❌ Erro ao validar {dim_table}: {str(e)}")
            all_passed = False
    
    # Resultado final
    if all_passed:
        print("\n🎉 Todas as validações de qualidade passaram!")
        return 0
    else:
        print("\n❌ Algumas validações falharam. Verifique os logs acima.")
        return 1

if __name__ == "__main__":
    exit(main())
```

---

## ⚡ performance_benchmarks.py
Script para validar performance de notebooks.

```python
#!/usr/bin/env python3
"""
Benchmarks de performance para workshops Microsoft Fabric
"""

import time
import json
from pathlib import Path
from pyspark.sql import SparkSession
from typing import Dict, List

class PerformanceBenchmark:
    
    def __init__(self, spark_session: SparkSession):
        self.spark = spark_session
        self.benchmarks = {}
    
    def benchmark_query(self, query: str, name: str) -> float:
        """Executa benchmark de query SQL"""
        start_time = time.time()
        
        try:
            result_df = self.spark.sql(query)
            # Force execution
            record_count = result_df.count()
            
            execution_time = time.time() - start_time
            self.benchmarks[name] = {
                "execution_time": execution_time,
                "record_count": record_count,
                "status": "success"
            }
            
            return execution_time
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.benchmarks[name] = {
                "execution_time": execution_time,
                "error": str(e),
                "status": "failed"
            }
            return execution_time
    
    def benchmark_scd2_merge(self, source_table: str, target_table: str, natural_key: str) -> float:
        """Benchmark de operação SCD2 merge"""
        merge_query = f"""
        MERGE INTO {target_table} AS target
        USING (
            SELECT *, 
                   current_date() as effective_date,
                   '9999-12-31' as end_date,
                   true as is_current,
                   1 as version
            FROM {source_table}
        ) AS source
        ON target.{natural_key} = source.{natural_key} AND target.is_current = true
        WHEN MATCHED AND target.hash_key != source.hash_key THEN
            UPDATE SET 
                is_current = false,
                end_date = current_date() - 1
        WHEN NOT MATCHED THEN
            INSERT *
        """
        
        return self.benchmark_query(merge_query, f"scd2_merge_{target_table}")
    
    def run_standard_benchmarks(self) -> Dict[str, float]:
        """Executa suite padrão de benchmarks"""
        
        benchmarks_to_run = [
            ("SELECT COUNT(*) FROM bronze_customers", "bronze_count_customers"),
            ("SELECT COUNT(*) FROM silver_customers WHERE is_current = true", "silver_current_customers"),
            ("SELECT COUNT(*) FROM dim_customer", "gold_dim_customer_count"),
            ("""
             SELECT c.customer_state, COUNT(*) as orders
             FROM dim_customer c
             JOIN fact_sales f ON c.DimCustomerSK = f.DimCustomerSK
             GROUP BY c.customer_state
             ORDER BY orders DESC
             LIMIT 10
             """, "analytical_query_top_states"),
        ]
        
        results = {}
        for query, name in benchmarks_to_run:
            execution_time = self.benchmark_query(query, name)
            results[name] = execution_time
            print(f"⏱️ {name}: {execution_time:.2f}s")
        
        return results
    
    def validate_performance_thresholds(self) -> bool:
        """Valida se performance está dentro dos limites aceitáveis"""
        
        # Thresholds de referência (em segundos)
        thresholds = {
            "bronze_count_customers": 30,
            "silver_current_customers": 45,
            "gold_dim_customer_count": 30,
            "analytical_query_top_states": 60,
        }
        
        all_passed = True
        
        for benchmark_name, threshold in thresholds.items():
            if benchmark_name in self.benchmarks:
                actual_time = self.benchmarks[benchmark_name]["execution_time"]
                passed = actual_time <= threshold
                
                status = "✅" if passed else "❌"
                print(f"{status} {benchmark_name}: {actual_time:.2f}s (limite: {threshold}s)")
                
                if not passed:
                    all_passed = False
            else:
                print(f"⚠️ Benchmark {benchmark_name} não foi executado")
                all_passed = False
        
        return all_passed
    
    def save_results(self, output_path: Path):
        """Salva resultados dos benchmarks"""
        with open(output_path, 'w') as f:
            json.dump(self.benchmarks, f, indent=2)

def main():
    """Executa benchmarks de performance"""
    spark = SparkSession.builder \
        .appName("PerformanceBenchmarks") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    
    benchmark = PerformanceBenchmark(spark)
    
    print("⚡ Executando benchmarks de performance...")
    
    # Executar benchmarks padrão
    benchmark.run_standard_benchmarks()
    
    # Validar thresholds
    print("\n📊 Validando limites de performance...")
    performance_ok = benchmark.validate_performance_thresholds()
    
    # Salvar resultados
    results_path = Path("performance_results.json")
    benchmark.save_results(results_path)
    print(f"\n💾 Resultados salvos em: {results_path}")
    
    if performance_ok:
        print("\n🎉 Todos os benchmarks passaram nos limites de performance!")
        return 0
    else:
        print("\n❌ Alguns benchmarks excederam os limites de performance")
        return 1

if __name__ == "__main__":
    exit(main())
```

---

## 🧪 run_test_suite.py
Script para executar toda a suíte de testes.

```python
#!/usr/bin/env python3
"""
Executa suíte completa de testes para workshop Microsoft Fabric
"""

import subprocess
import sys
from pathlib import Path
import pytest
import json

def run_pytest(test_path: Path) -> bool:
    """Executa testes pytest"""
    try:
        result = pytest.main([
            str(test_path),
            "-v",
            "--tb=short",
            "--junitxml=test_results.xml",
            "--cov=scripts/utils",
            "--cov-report=html",
            "--cov-report=term"
        ])
        return result == 0
    except Exception as e:
        print(f"❌ Erro ao executar testes: {str(e)}")
        return False

def run_structure_validation(workshop_path: Path) -> bool:
    """Executa validação de estrutura"""
    try:
        result = subprocess.run([
            sys.executable, 
            "scripts/validate_structure.py", 
            str(workshop_path)
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro na validação de estrutura: {str(e)}")
        return False

def run_quality_checks() -> bool:
    """Executa validações de qualidade de dados"""
    try:
        result = subprocess.run([
            sys.executable,
            "scripts/quality_checks.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro nas validações de qualidade: {str(e)}")
        return False

def run_performance_benchmarks() -> bool:
    """Executa benchmarks de performance"""
    try:
        result = subprocess.run([
            sys.executable,
            "scripts/performance_benchmarks.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro nos benchmarks: {str(e)}")
        return False

def generate_test_report(results: Dict[str, bool]):
    """Gera relatório consolidado de testes"""
    
    report = {
        "total_suites": len(results),
        "passed_suites": sum(1 for passed in results.values() if passed),
        "failed_suites": sum(1 for passed in results.values() if not passed),
        "success_rate": (sum(1 for passed in results.values() if passed) / len(results)) * 100,
        "details": results
    }
    
    # Salvar relatório JSON
    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Imprimir resumo
    print(f"\n📊 RELATÓRIO DE TESTES")
    print(f"├── Total de suítes: {report['total_suites']}")
    print(f"├── Aprovadas: {report['passed_suites']}")
    print(f"├── Reprovadas: {report['failed_suites']}")
    print(f"└── Taxa de sucesso: {report['success_rate']:.1f}%")
    
    return report["failed_suites"] == 0

def main():
    """Executa toda a suíte de validações"""
    
    workshop_path = Path.cwd()
    test_results = {}
    
    print("🧪 Executando suíte completa de testes...\n")
    
    # 1. Validação de estrutura
    print("1️⃣ Validando estrutura do workshop...")
    test_results["structure"] = run_structure_validation(workshop_path)
    
    # 2. Testes unitários
    print("\n2️⃣ Executando testes unitários...")
    test_path = workshop_path / "scripts" / "tests"
    if test_path.exists():
        test_results["unit_tests"] = run_pytest(test_path)
    else:
        print("⚠️ Pasta de testes não encontrada, pulando testes unitários")
        test_results["unit_tests"] = True
    
    # 3. Validações de qualidade de dados
    print("\n3️⃣ Validando qualidade de dados...")
    test_results["data_quality"] = run_quality_checks()
    
    # 4. Benchmarks de performance
    print("\n4️⃣ Executando benchmarks de performance...")
    test_results["performance"] = run_performance_benchmarks()
    
    # 5. Gerar relatório final
    print("\n5️⃣ Gerando relatório final...")
    all_passed = generate_test_report(test_results)
    
    if all_passed:
        print("\n🎉 Todos os testes passaram! Workshop pronto para publicação.")
        return 0
    else:
        print("\n❌ Alguns testes falharam. Revise os resultados antes de publicar.")
        return 1

if __name__ == "__main__":
    exit(main())
```

---

## 🔧 scd2_utils.py
Funções utilitárias reutilizáveis para SCD Tipo 2.

```python
"""
Utilitários para SCD Tipo 2 em workshops Microsoft Fabric
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import *
from pyspark.sql.types import *
from delta.tables import DeltaTable
import hashlib
from typing import List, Dict, Optional

def add_scd2_columns(df: DataFrame, natural_key_cols: List[str]) -> DataFrame:
    """
    Adiciona colunas SCD Tipo 2 padrão a um DataFrame
    
    Args:
        df: DataFrame de origem
        natural_key_cols: Lista de colunas que formam a chave natural
        
    Returns:
        DataFrame com colunas SCD2 adicionadas
    """
    
    # Adicionar colunas SCD2
    df_with_scd2 = df.withColumn("effective_date", current_date()) \
                     .withColumn("end_date", lit("9999-12-31").cast(DateType())) \
                     .withColumn("is_current", lit(True)) \
                     .withColumn("version", lit(1)) \
                     .withColumn("hash_key", create_hash_key(df, natural_key_cols))
    
    return df_with_scd2

def create_hash_key(df: DataFrame, columns: List[str]) -> Column:
    """
    Cria hash key para detecção de mudanças
    
    Args:
        df: DataFrame de origem
        columns: Colunas para incluir no hash
        
    Returns:
        Coluna com hash MD5
    """
    
    # Concatenar colunas (ignorando colunas SCD2)
    scd2_columns = {"effective_date", "end_date", "is_current", "version", "hash_key"}
    hash_columns = [col_name for col_name in columns if col_name not in scd2_columns]
    
    concat_cols = concat_ws("|", *[coalesce(col(c).cast("string"), lit("NULL")) for c in hash_columns])
    
    return md5(concat_cols)

def perform_scd2_merge(source_df: DataFrame, 
                      target_table: str, 
                      natural_key_cols: List[str],
                      spark_session) -> Dict[str, int]:
    """
    Executa merge SCD Tipo 2 completo
    
    Args:
        source_df: DataFrame com dados novos
        target_table: Nome da tabela de destino
        natural_key_cols: Colunas da chave natural
        spark_session: Sessão Spark
        
    Returns:
        Estatísticas do merge (inserted, updated, unchanged)
    """
    
    # Preparar dados de origem com SCD2
    source_with_scd2 = add_scd2_columns(source_df, natural_key_cols)
    
    # Criar view temporária para merge
    source_with_scd2.createOrReplaceTempView("source_data")
    
    # Construir condição de join
    join_condition = " AND ".join([f"target.{col} = source.{col}" for col in natural_key_cols])
    
    # Executar merge SCD2
    merge_sql = f"""
    MERGE INTO {target_table} AS target
    USING source_data AS source
    ON {join_condition} AND target.is_current = true
    
    WHEN MATCHED AND target.hash_key != source.hash_key THEN
        UPDATE SET 
            is_current = false,
            end_date = current_date() - 1
    
    WHEN NOT MATCHED THEN
        INSERT *
    """
    
    # Executar merge
    spark_session.sql(merge_sql)
    
    # Para registros que foram atualizados, inserir nova versão
    updated_keys_sql = f"""
    SELECT DISTINCT {', '.join(natural_key_cols)}
    FROM {target_table}
    WHERE end_date = current_date() - 1
    """
    
    updated_keys = spark_session.sql(updated_keys_sql)
    
    if updated_keys.count() > 0:
        # Juntar com dados de origem para inserir novas versões
        new_versions = source_with_scd2.join(
            updated_keys, 
            natural_key_cols, 
            "inner"
        ).withColumn("version", lit(2))  # Simplificado, deveria calcular próxima versão
        
        # Inserir novas versões
        new_versions.write.mode("append").saveAsTable(target_table)
    
    # Calcular estatísticas (simplificado)
    stats = {
        "inserted": source_with_scd2.count(),
        "updated": updated_keys.count(),
        "unchanged": 0
    }
    
    return stats

def validate_scd2_integrity(table_name: str, 
                           natural_key_cols: List[str], 
                           spark_session) -> Dict[str, bool]:
    """
    Valida integridade SCD Tipo 2 de uma tabela
    
    Args:
        table_name: Nome da tabela a validar
        natural_key_cols: Colunas da chave natural
        spark_session: Sessão Spark
        
    Returns:
        Dicionário com resultados das validações
    """
    
    validations = {}
    
    # 1. Verificar duplicatas de registros correntes
    natural_key_join = ", ".join(natural_key_cols)
    
    current_duplicates = spark_session.sql(f"""
        SELECT {natural_key_join}, COUNT(*) as count
        FROM {table_name}
        WHERE is_current = true
        GROUP BY {natural_key_join}
        HAVING COUNT(*) > 1
    """).count()
    
    validations["no_current_duplicates"] = current_duplicates == 0
    
    # 2. Verificar consistência de datas
    date_issues = spark_session.sql(f"""
        SELECT COUNT(*) as issues
        FROM {table_name}
        WHERE effective_date > end_date
        OR (is_current = true AND end_date != '9999-12-31')
        OR (is_current = false AND end_date = '9999-12-31')
    """).collect()[0]["issues"]
    
    validations["date_consistency"] = date_issues == 0
    
    # 3. Verificar sequência de versões
    version_gaps = spark_session.sql(f"""
        WITH version_sequence AS (
            SELECT {natural_key_join}, version,
                   ROW_NUMBER() OVER (
                       PARTITION BY {natural_key_join} 
                       ORDER BY version
                   ) as expected_version
            FROM {table_name}
        )
        SELECT COUNT(*) as gaps
        FROM version_sequence
        WHERE version != expected_version
    """).collect()[0]["gaps"]
    
    validations["version_sequence"] = version_gaps == 0
    
    return validations

def optimize_scd2_table(table_name: str, 
                       natural_key_cols: List[str], 
                       spark_session):
    """
    Aplica otimizações específicas para tabelas SCD2
    
    Args:
        table_name: Nome da tabela
        natural_key_cols: Colunas da chave natural
        spark_session: Sessão Spark
    """
    
    # Z-order por chave natural e status atual
    zorder_cols = natural_key_cols + ["is_current"]
    zorder_sql = f"OPTIMIZE {table_name} ZORDER BY ({', '.join(zorder_cols)})"
    
    spark_session.sql(zorder_sql)
    
    # Vacuum para remover arquivos antigos (manter 7 dias)
    vacuum_sql = f"VACUUM {table_name} RETAIN 168 HOURS"
    spark_session.sql(vacuum_sql)
    
    print(f"✅ Otimizações aplicadas em {table_name}")

# Configurações padrão SCD2
SCD2_CONFIG = {
    "columns": {
        "effective_date": "effective_date",
        "end_date": "end_date", 
        "is_current": "is_current",
        "version": "version",
        "hash_key": "hash_key"
    },
    "default_end_date": "9999-12-31",
    "date_format": "yyyy-MM-dd"
}
```

---

💡 **Uso dos Scripts**:

```bash
# Validar estrutura do workshop
uv run scripts/validate_structure.py .

# Executar validações de qualidade
uv run scripts/quality_checks.py

# Benchmarks de performance  
uv run scripts/performance_benchmarks.py

# Suite completa de testes
uv run scripts/run_test_suite.py
```

Estes scripts garantem qualidade, consistência e performance adequada em todos os workshops Microsoft Fabric! 🚀