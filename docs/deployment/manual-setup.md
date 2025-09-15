# 🔧 Setup Manual - Microsoft Fabric Workshop

## 📋 Visão Geral

Este guia fornece instruções passo-a-passo para configurar manualmente todo o ambiente necessário para os workshops do Microsoft Fabric.

## ⏱️ Tempo Estimado
- **Configuração básica:** 45-60 minutos
- **Setup completo:** 90-120 minutos
- **Verificação e testes:** 30 minutos

## 🚀 Passo 1: Configuração do Microsoft Fabric

### 1.1 Criação do Workspace

1. **Acesse o Portal do Fabric:**
   ```
   URL: https://app.fabric.microsoft.com
   ```

2. **Crie um Novo Workspace:**
   - Clique em "Workspaces" no menu lateral
   - Selecione "New workspace"
   - Nome: `FabricWorkshop`
   - Descrição: `Workspace para workshops do Microsoft Fabric`

3. **Configure a Capacidade:**
   - Se usando trial: automático
   - Se usando licença: selecione capacidade F2+

### 1.2 Verificação de Permissões

```powershell
# Verificar se workspace foi criado
# (Através do portal Fabric)
```

## 🏗️ Passo 2: Criação do Lakehouse

### 2.1 Criar Lakehouse Principal

1. **No Portal Fabric:**
   - Vá para "Data Engineering" experience
   - Clique em "New" → "Lakehouse"
   - Nome: `AdventureWorksLH`

2. **Verificar Estrutura:**
   ```
   AdventureWorksLH/
   ├── Files/     # Para arquivos não estruturados
   ├── Tables/    # Para tabelas gerenciadas  
   └── Schemas/   # Para esquemas customizados
   ```

### 2.2 Upload dos Datasets

1. **Preparar Dados Localmente:**
   ```bash
   git clone https://github.com/Miyake-Diogo/MS-Fabric-Workshop.git
   cd MS-Fabric-Workshop/workshops/lakehouse/data
   ```

2. **Upload via Portal:**
   - Navegue para "Files" no Lakehouse
   - Crie pasta `bronze/`
   - Upload todos os arquivos .parquet e .csv

3. **Estrutura Final:**
   ```
   Files/bronze/
   ├── AdvWorksDatasets/
   │   ├── DimCustomer.parquet
   │   ├── DimProduct.parquet
   │   ├── FactInternetSales.parquet
   │   └── ...
   └── OlistDatasets/
       ├── olist_customers_dataset.csv
       ├── olist_orders_dataset.csv
       └── ...
   ```

## 📓 Passo 3: Configuração dos Notebooks

### 3.1 Upload dos Notebooks

1. **No Portal Fabric:**
   - Vá para "Data Engineering"
   - Clique em "New" → "Notebook"
   - Upload arquivo `.ipynb`

2. **Notebooks para Upload (em ordem):**
   ```
   01-LoadADVWorksDataToLH.ipynb
   01-LoadOlistDataToLH.ipynb  
   02-SilverTransformations.ipynb
   03-GoldTransformationsDim.ipynb
   04-GoldTransformationsFact.ipynb
   05-GoldOptimizations.ipynb
   ```

### 3.2 Conectar Notebooks ao Lakehouse

Para cada notebook:
1. Clique em "Add Lakehouse"
2. Selecione "Existing Lakehouse"  
3. Escolha `AdventureWorksLH`
4. Confirme conexão

### 3.3 Executar Notebooks Sequencialmente

```python
# Execute na ordem:
# 1. LoadADVWorksDataToLH (15 min)
# 2. LoadOlistDataToLH (15 min)  
# 3. SilverTransformations (30 min)
# 4. GoldTransformationsDim (45 min)
# 5. GoldTransformationsFact (45 min)  
# 6. GoldOptimizations (30 min)
```

## 🤖 Passo 4: Configuração do Data Agent

### 4.1 Criar Data Agent

1. **No Portal Fabric:**
   - Vá para "Data Science" experience
   - Clique em "New" → "Data Agent"
   - Nome: `AdventureWorksAgent`

2. **Selecionar Dados:**
   Escolha as tabelas:
   ```
   ✅ dimcustomer
   ✅ dimdate
   ✅ dimgeography  
   ✅ dimproduct
   ✅ dimproductcategory
   ✅ dimpromotion
   ✅ dimreseller
   ✅ dimsalesterritory
   ✅ factinternetsales
   ✅ factresellersales
   ```

### 4.2 Configurar Instruções do Agent

```
A fonte de dados AdventureWorksLH contém informações sobre vendas de bicicletas:

CUSTOMERS: 
- dimcustomer: dados demográficos de clientes
- dimgeography: informações geográficas  

PRODUCTS:
- dimproduct: catálogo de produtos
- dimproductcategory: categorias de produtos
- dimpromotion: promoções ativas

SALES:
- factinternetsales: vendas online
- factresellersales: vendas de revendedores
- dimdate: dimensão temporal

Use para análises de vendas, comportamento de clientes e performance de produtos.
```

### 4.3 Adicionar Queries de Exemplo

#### Exemplo 1:
```sql
-- Questão: Qual foi o total de vendas por categoria em 2013?
SELECT 
    pc.EnglishProductCategoryName,
    SUM(fis.SalesAmount) as TotalSales
FROM factinternetsales fis
JOIN dimproduct p ON fis.ProductKey = p.ProductKey  
JOIN dimproductcategory pc ON p.ProductCategoryKey = pc.ProductCategoryKey
JOIN dimdate d ON fis.OrderDateKey = d.DateKey
WHERE d.CalendarYear = 2013
GROUP BY pc.EnglishProductCategoryName
ORDER BY TotalSales DESC;
```

#### Exemplo 2:
```sql
-- Questão: Top 10 clientes por valor total de compras
SELECT TOP 10
    c.FirstName + ' ' + c.LastName as CustomerName,
    SUM(fis.SalesAmount) as TotalPurchases
FROM factinternetsales fis
JOIN dimcustomer c ON fis.CustomerKey = c.CustomerKey
GROUP BY c.CustomerKey, c.FirstName, c.LastName  
ORDER BY TotalPurchases DESC;
```

## ☁️ Passo 5: Configuração Azure AI Foundry

### 5.1 Criar AI Foundry Project

1. **Via Portal Azure:**
   ```
   URL: https://portal.azure.com
   ```

2. **Criar Resource Group:**
   ```bash
   az group create --name fabric-workshop-rg --location eastus
   ```

3. **Criar AI Foundry Hub:**
   - Ir para "AI + Machine Learning"
   - Criar "Azure AI Foundry"
   - Nome: `fabric-ai-foundry`
   - Resource Group: `fabric-workshop-rg`

### 5.2 Configurar Azure OpenAI

1. **Criar Azure OpenAI Service:**
   ```bash
   az cognitiveservices account create \
     --name fabric-openai \
     --resource-group fabric-workshop-rg \
     --kind OpenAI \
     --sku S0 \
     --location eastus
   ```

2. **Deploy do Modelo:**
   - No Azure OpenAI Studio
   - Deploy model: `gpt-4o-mini`
   - Deployment name: `gpt-4o-mini`

### 5.3 Conectar Data Agent ao AI Foundry

1. **Obter Endpoint do Data Agent:**
   ```
   Exemplo:
   https://api.fabric.microsoft.com/v1/workspaces/{workspace-id}/aiskills/{artifact-id}/aiassistant/openai
   ```

2. **Configurar no AI Foundry:**
   - Criar novo "Agent"
   - Adicionar "Custom Tool"
   - Configurar endpoint do Fabric

3. **Instruções do Sistema:**
   ```
   Você é um assistente especializado em dados que SEMPRE usa a ferramenta MyAgent Knowledge para consultar informações do dataset AdventureWorks.
   
   Para qualquer pergunta sobre dados:
   1. Use a ferramenta MyAgent Knowledge
   2. Formate a resposta de forma clara
   3. Sugira análises adicionais quando apropriado
   ```

## 🛠️ Passo 6: Configuração da Aplicação DataBot (Opcional)

### 6.1 Preparar Ambiente Local

1. **Clonar e Navegar:**
   ```bash
   cd MS-Fabric-Workshop/applications/databot
   ```

2. **Criar Ambiente Virtual:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Instalar Dependências:**
   ```bash
   pip install -e .
   ```

### 6.2 Configurar Variáveis de Ambiente

1. **Copiar Template:**
   ```bash
   copy .env.example .env
   ```

2. **Editar .env:**
   ```env
   # Azure Configuration
   AZURE_CLIENT_ID=your_client_id
   AZURE_CLIENT_SECRET=your_client_secret  
   AZURE_TENANT_ID=your_tenant_id
   
   # AI Foundry Configuration
   AI_FOUNDRY_ENDPOINT=https://your-foundry.ai.azure.com
   AI_FOUNDRY_API_KEY=your_api_key
   
   # Fabric Agent Configuration
   FABRIC_AGENT_ENDPOINT=https://api.fabric.microsoft.com/v1/workspaces/.../aiassistant/openai
   ```

### 6.3 Testar Aplicação Localmente

```bash
# Backend
cd src/backend
python main.py

# Frontend (em outro terminal)
cd src/frontend  
npm install
npm start
```

## ✅ Passo 7: Verificação e Testes

### 7.1 Verificar Lakehouse

```sql
-- No SQL Analytics endpoint do Lakehouse
SELECT 
    table_name,
    COUNT(*) as record_count
FROM (
    SELECT 'dimcustomer' as table_name, COUNT(*) as count FROM dimcustomer
    UNION ALL
    SELECT 'factinternetsales', COUNT(*) FROM factinternetsales
) t
```

### 7.2 Testar Data Agent

**Perguntas para testar:**
```
"Qual foi o total de vendas em 2013?"
"Quais são os 5 produtos mais vendidos?"  
"Mostrar vendas por país"
"Qual cliente teve maior valor de compras?"
```

### 7.3 Verificar AI Foundry Integration

```python
# Teste via Python
import requests

response = requests.post(
    "https://your-foundry-endpoint/chat",
    headers={"Authorization": "Bearer <token>"},
    json={"message": "Mostre um resumo das vendas"}
)
print(response.json())
```

## 🔧 Troubleshooting

### Problemas Comuns

#### Lakehouse não aparece para seleção
**Solução:**
1. Verificar permissões no workspace
2. Atualizar página do browser
3. Tentar novamente após alguns minutos

#### Notebooks não executam
**Solução:**
1. Verificar conexão com Lakehouse
2. Confirmar que dados foram uploadados
3. Executar células uma por vez

#### Data Agent não funciona
**Solução:**
1. Verificar se tabelas estão disponíveis
2. Revisar instruções do agent
3. Adicionar mais exemplos de queries

#### Erro de autenticação no AI Foundry
**Solução:**
1. Verificar service principal
2. Confirmar permissões adequadas
3. Testar endpoint manualmente

## 📚 Próximos Passos

Após o setup manual estar completo:

1. **Execute Workshop Lakehouse:** [Guia detalhado](../workshops/fabric-lakehouse.md)
2. **Execute Workshop Data Agents:** [Guia detalhado](../workshops/fabric-data-agents.md)  
3. **Explore Aplicação DataBot:** [Documentação](../../applications/databot/README.md)
4. **Configure Deploy Automatizado:** [Setup com IaC](automated-deployment.md)

## 📞 Suporte

- **Issues:** [GitHub Issues](https://github.com/Miyake-Diogo/MS-Fabric-Workshop/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Miyake-Diogo/MS-Fabric-Workshop/discussions)
- **Docs Oficiais:** [Microsoft Learn](https://learn.microsoft.com/fabric/)

---

**🎉 Parabéns!** Seu ambiente está configurado e pronto para os workshops. Comece com o [Workshop Lakehouse](../workshops/fabric-lakehouse.md)!