# 🔧 Guia de Troubleshooting - Microsoft Fabric Workshop

## 📋 Índice

- [Problemas Comuns](#problemas-comuns)
- [Microsoft Fabric Issues](#microsoft-fabric-issues)
- [Data Agents Problems](#data-agents-problems)
- [AI Foundry Integration](#ai-foundry-integration)
- [DataBot Application](#databot-application)
- [Performance Issues](#performance-issues)
- [Deployment Problems](#deployment-problems)
- [Logs e Diagnósticos](#logs-e-diagnósticos)

## 🚨 Problemas Comuns

### 1. "Não consigo acessar o Microsoft Fabric"

#### Sintomas:
- Página não carrega
- Erro de autenticação
- Workspace não aparece

#### Possíveis Causas:
- ❌ Trial expirado
- ❌ Permissões insuficientes
- ❌ Problemas de rede
- ❌ Cache do browser

#### Soluções:

**Verificar Status do Trial:**
```
1. Acesse fabric.microsoft.com
2. Vá em Settings > Trial Status
3. Verificar dias restantes
4. Renovar se necessário
```

**Limpar Cache do Browser:**
```javascript
// Chrome DevTools Console
localStorage.clear();
sessionStorage.clear();
location.reload();
```

**Testar Conectividade:**
```powershell
# Testar conectividade
Test-NetConnection fabric.microsoft.com -Port 443
nslookup fabric.microsoft.com
```

### 2. "Workspace não encontrado ou sem permissões"

#### Sintomas:
- Workspace não listado
- Erro 403 Forbidden
- Não consegue criar itens

#### Soluções:

**Verificar Permissões:**
```
1. No Fabric Portal:
   - Workspace Settings > Users
   - Verificar role (Admin/Member/Contributor)
   
2. Solicitar acesso ao administrador se necessário
```

**Verificar Capacidade:**
```
1. Workspace Settings > Capacity
2. Verificar se capacity está ativa
3. Verificar consumption units disponíveis
```

### 3. "Erro ao carregar dados no Lakehouse"

#### Sintomas:
- Upload falha
- Arquivo não aparece
- Erro de tamanho

#### Soluções:

**Verificar Limites:**
```
Limites do Fabric:
- Arquivo individual: 200MB
- Total workspace: Depende da capacity
- Formatos suportados: CSV, Parquet, JSON, Excel
```

**Upload Alternativo:**
```python
# Via notebook
import pandas as pd

# Ler arquivo local
df = pd.read_csv("/local/path/file.csv")

# Salvar no Lakehouse
df.to_parquet("/lakehouse/default/Files/data/file.parquet")
```

## 🏢 Microsoft Fabric Issues

### Lakehouse Problems

#### Problema: "Tabela não encontrada"
```sql
-- Erro comum
SELECT * FROM dimcustomer;
-- Error: Table 'dimcustomer' doesn't exist

-- Solução: Verificar nome exato
SHOW TABLES;
-- ou
SELECT * FROM information_schema.tables;
```

#### Problema: "Schema conflicts"
```python
# Erro ao escrever dados
df.write.saveAsTable("table_name")
# Error: Schema mismatch

# Solução: Forçar overwrite
df.write.mode("overwrite").saveAsTable("table_name")

# Ou ajustar schema
df_cleaned = df.select("col1", "col2", "col3")
df_cleaned.write.saveAsTable("table_name")
```

#### Problema: "Performance lenta"
```sql
-- Otimização de tabelas
OPTIMIZE table_name;

-- Z-ordering para queries frequentes
OPTIMIZE table_name ZORDER BY (date_column, key_column);

-- Vacuum para limpeza
VACUUM table_name RETAIN 168 HOURS;
```

### Notebook Issues

#### Problema: "Kernel não inicia"
```python
# Verificar versão do Spark
spark.version

# Reiniciar kernel via UI
# Notebook menu: Kernel > Restart Kernel

# Verificar capacity consumption
# Portal: Monitoring > Capacity Metrics
```

#### Problema: "Import errors"
```python
# Instalar packages no notebook
%pip install package_name

# Para instalar permanentemente
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "package_name"])
```

## 🤖 Data Agents Problems

### Agent Creation Issues

#### Problema: "Não consegue criar Data Agent"
**Verificações:**
```
1. Capacidade suficiente no workspace
2. Lakehouse com dados carregados
3. Permissões adequadas
4. Feature preview habilitada
```

**Solução:**
```
1. Workspace Settings > Preview Features
2. Habilitar "Data Agents (Preview)"
3. Aguardar 15-30 minutos para ativação
4. Tentar criar agent novamente
```

#### Problema: "Agent não encontra tabelas"
```
Verificações:
✓ Lakehouse conectado ao workspace
✓ Tabelas visíveis no SQL Analytics Endpoint
✓ Dados carregados (não apenas arquivos)

Solução:
1. No Lakehouse, converter Files para Tables
2. Verificar via SQL Analytics Endpoint
3. Aguardar indexação (5-10 minutos)
```

### Query Generation Issues

#### Problema: "SQL gerado está incorreto"
**Exemplo de problema:**
```sql
-- Agent gera:
SELECT * FROM customer WHERE name = "João"

-- Erro: Syntax incorrect

-- Correção: Treinar com exemplos
-- Adicionar query example:
SELECT * FROM dimcustomer WHERE FirstName = 'João'
```

**Melhorar training:**
```
1. Adicionar 5-10 query examples
2. Cobrir diferentes padrões:
   - Joins
   - Aggregations  
   - Date filters
   - String matching
3. Usar nomes de colunas exatos
```

#### Problema: "Agent não entende contexto"
**Instruções melhores:**
```
❌ Ruim:
"Use os dados para consultas"

✅ Bom:
"Esta fonte contém dados de vendas de bicicletas:
- dimcustomer: dados de clientes (18K registros)
- factinternetsales: vendas online (60K transações)
- dimproduct: catálogo de produtos (606 itens)

Para análises de vendas, use factinternetsales com joins para dimensões.
Para análises de clientes, use dimcustomer com dimgeography."
```

## 🧠 AI Foundry Integration

### Connection Issues

#### Problema: "Erro de autenticação com AI Foundry"
```bash
# Verificar service principal
az ad sp show --id <service-principal-id>

# Verificar permissões
az role assignment list --assignee <service-principal-id>

# Testar token
curl -X POST "https://login.microsoftonline.com/<tenant>/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=<client-id>&client_secret=<secret>&scope=https://management.azure.com/.default&grant_type=client_credentials"
```

#### Problema: "Endpoint não responde"
```python
# Testar endpoint
import requests

response = requests.get(
    "https://api.fabric.microsoft.com/v1/workspaces/<workspace-id>/aiskills/<agent-id>/aiassistant/openai",
    headers={"Authorization": "Bearer <token>"}
)
print(response.status_code, response.text)
```

### Model Issues

#### Problema: "Quota exceeded no OpenAI"
```bash
# Verificar uso atual
az cognitiveservices account list-usage \
  --name <openai-resource> \
  --resource-group <rg>

# Verificar limites
az cognitiveservices account list-skus \
  --name <openai-resource> \
  --resource-group <rg>
```

**Soluções:**
- Aguardar reset da quota (mensal)
- Aumentar tier do OpenAI
- Implementar rate limiting
- Usar multiple deployments

## 💬 DataBot Application

### Development Issues

#### Problema: "Dependências não instalam"
```bash
# Verificar versão Python
python --version  # Deve ser 3.11+

# Limpar cache pip
pip cache purge

# Usar uv para instalação mais rápida
pip install uv
uv pip install -r requirements.txt

# Virtual environment
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

#### Problema: "Frontend não inicia"
```bash
# Verificar Node.js
node --version  # Deve ser 18+

# Limpar cache npm
npm cache clean --force

# Reinstalar dependências
rm -rf node_modules package-lock.json
npm install

# Iniciar com debug
npm start --verbose
```

### Runtime Issues

#### Problema: "Erro de CORS"
```python
# Backend: adicionar CORS headers
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Problema: "WebSocket connection fails"
```python
# Verificar configuração WebSocket
import websockets

async def test_connection():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("test")
        response = await websocket.recv()
        print(response)
```

## ⚡ Performance Issues

### Slow Query Performance

#### Diagnóstico:
```sql
-- Verificar estatísticas da tabela
DESCRIBE EXTENDED table_name;

-- Verificar plano de execução
EXPLAIN SELECT * FROM table_name WHERE condition;

-- Verificar particionamento
SHOW PARTITIONS table_name;
```

#### Otimizações:
```sql
-- Criar índices (se suportado)
CREATE INDEX idx_customer_date ON factinternetsales (CustomerKey, OrderDateKey);

-- Otimizar layout
OPTIMIZE factinternetsales;

-- Z-order por colunas frequentes
OPTIMIZE factinternetsales ZORDER BY (CustomerKey, ProductKey);
```

### Memory Issues

#### Problema: "Out of memory errors"
```python
# Processamento em lotes
batch_size = 10000
for i in range(0, df.count(), batch_size):
    batch = df.limit(batch_size).offset(i)
    batch.write.mode("append").saveAsTable("target_table")

# Usar particionamento
df.repartition(10).write.saveAsTable("table_name")

# Cache estratégico
df.cache()  # Apenas para DataFrames reutilizados
```

## 🚀 Deployment Problems

### Infrastructure Issues

#### Problema: "Bicep deployment fails"
```bash
# Verificar deployment
az deployment group show --name <deployment-name> --resource-group <rg>

# Ver logs de erro
az deployment operation group list --name <deployment-name> --resource-group <rg>

# Validar template
az deployment group validate --template-file main.bicep --parameters main.parameters.json --resource-group <rg>
```

#### Problema: "Container App não inicia"
```bash
# Verificar logs
az containerapp logs show --name <app-name> --resource-group <rg>

# Verificar configuração
az containerapp show --name <app-name> --resource-group <rg>

# Testar localmente com Docker
docker build -t databot .
docker run -p 8000:8000 databot
```

## 📊 Logs e Diagnósticos

### Fabric Monitoring

#### Acessar Logs:
```
1. Fabric Portal > Monitoring
2. Activity Log para workspace
3. Query History para Lakehouse
4. Agent Usage para Data Agents
```

#### KQL Queries úteis:
```kql
// Errors nos últimos 7 dias
WorkspaceActivity
| where TimeGenerated > ago(7d)
| where ResultType != "Success"
| summarize count() by ResultType, bin(TimeGenerated, 1h)
| render timechart

// Performance de queries
QueryHistory  
| where TimeGenerated > ago(1d)
| summarize avg(DurationMs) by bin(TimeGenerated, 1h)
| render timechart
```

### Application Insights

#### Query para Erros:
```kql
// Erros da aplicação
exceptions
| where timestamp > ago(1d)
| summarize count() by type, bin(timestamp, 1h)
| render timechart

// Performance requests
requests
| where timestamp > ago(1d)
| summarize avg(duration) by name, bin(timestamp, 5m)
| render timechart
```

### Debug Local

#### Verificar Conectividade:
```python
# Testar conexão Fabric
import requests

def test_fabric_connection():
    try:
        response = requests.get("https://api.fabric.microsoft.com/v1/workspaces")
        print(f"Status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False

# Testar AI Foundry
def test_ai_foundry():
    # Implementar teste específico
    pass
```

## 📞 Obtendo Ajuda

### Escalação de Problemas

**Nível 1 - Self-Service:**
- Consultar esta documentação
- Verificar logs da aplicação
- Testar soluções conhecidas

**Nível 2 - Comunidade:**
- [GitHub Issues](https://github.com/Miyake-Diogo/MS-Fabric-Workshop/issues)
- [GitHub Discussions](https://github.com/Miyake-Diogo/MS-Fabric-Workshop/discussions)
- [Fabric Community](https://community.fabric.microsoft.com/)

**Nível 3 - Suporte Microsoft:**
- Azure Support Ticket
- Microsoft Learn Q&A
- Tech Community Forums

### Informações para Suporte

Sempre incluir:
```
1. ⏰ Timestamp do problema
2. 🔍 Mensagem de erro exata
3. 🔧 Componente afetado (Fabric/Agent/App)
4. 📊 Dados de contexto (workspace ID, etc.)
5. 🔄 Passos para reproduzir
6. 🌐 Ambiente (dev/test/prod)
```

---

**🔧 Problema não listado?** Abra um issue no GitHub com detalhes completos e logs relevantes!