# Microsoft Fabric Workshops

Esta seção contém todos os workshops práticos para aprender Microsoft Fabric.

## 📚 Workshops Disponíveis

### 1. Lakehouse
**Localização:** `lakehouse/`
**Descrição:** Workshop completo sobre Fabric Lakehouse incluindo transformações Bronze, Silver e Gold.

**Notebooks:**
- `01-LoadADVWorksDataToLH.ipynb` - Carregamento de dados AdventureWorks
- `01-LoadOlistDataToLH.ipynb` - Carregamento de dados Olist  
- `02-SilverTransformations.ipynb` - Transformações camada Silver
- `03-GoldTransformationsDim.ipynb` - Criação de tabelas dimensão
- `04-GoldTransformationsFact.ipynb` - Criação de tabelas fato
- `05-GoldOptimizations.ipynb` - Otimizações da camada Gold

### 2. Data Agents
**Localização:** `data-agents/`
**Descrição:** Workshop sobre criação e uso de Data Agents no Fabric.

**Componentes:**
- Notebooks de exemplo
- Queries de demonstração
- Integração com AI Foundry

### 3. Recursos Compartilhados
**Localização:** `shared/`
**Descrição:** Recursos utilizados por múltiplos workshops.

## 🚀 Como Começar

1. **Pré-requisitos:**
   - Acesso ao Microsoft Fabric
   - Python 3.11+
   - Jupyter Notebook ou VS Code

2. **Instalação das dependências:**
   ```bash
   cd workshops/
   pip install -e .
   ```

3. **Executar os workshops:**
   - Navegue para o workshop desejado
   - Siga a documentação específica em cada pasta
   - Execute os notebooks na ordem indicada

## 📖 Documentação

Cada workshop possui sua própria documentação detalhada na pasta `docs/` correspondente.

## 🤝 Contribuição

Para adicionar novos workshops ou melhorar os existentes, siga a estrutura padrão:
```
workshop-name/
├── README.md
├── docs/
├── notebooks/
├── data/ (se necessário)
└── examples/
```