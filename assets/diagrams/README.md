# 📊 Diagramas de Arquitetura - Microsoft Fabric Workshop

## 🎯 Visão Geral

Esta pasta contém diagramas de arquitetura da solução workshop em diferentes formatos para facilitar o entendimento técnico.

## 📁 Conteúdo

### Diagramas Principais

| Arquivo | Descrição | Formato |
|---------|-----------|---------|
| [overall-architecture.md](#overall-architecture) | Arquitetura geral da solução | Mermaid |
| [data-flow.md](#data-flow) | Fluxo de dados ETL/ELT | Mermaid |
| [conversational-flow.md](#conversational-flow) | Fluxo conversacional | Mermaid |
| [security-model.md](#security-model) | Modelo de segurança | Mermaid |

---

## Overall Architecture

```mermaid
graph TB
    subgraph "🎨 Frontend Layer"
        WebUI[🌐 Web Interface<br/>React + TypeScript]
        Mobile[📱 Mobile App<br/>PWA]
        PowerBI[📊 Power BI<br/>Embedded Reports]
        Teams[💬 Teams Bot<br/>Integration]
    end
    
    subgraph "🚀 Application Layer"
        API[🔌 REST API<br/>FastAPI]
        WebSocket[⚡ WebSocket<br/>Real-time Chat]
        Auth[🔐 Authentication<br/>Azure AD]
        Cache[💾 Redis Cache<br/>Session Management]
    end
    
    subgraph "🧠 AI Layer"
        Foundry[🤖 AI Foundry<br/>Agent Orchestration]
        OpenAI[🤖 Azure OpenAI<br/>GPT-4o-mini]
        Agents[🤖 Data Agents<br/>NL to SQL]
        Embedding[📝 Text Embeddings<br/>Vector Search]
    end
    
    subgraph "📊 Data Layer"
        Fabric[🏢 Microsoft Fabric<br/>Unified Platform]
        Lakehouse[🏗️ Lakehouse<br/>Delta Lake]
        Warehouse[🏪 Data Warehouse<br/>SQL Analytics]
        KQL[⚡ KQL Database<br/>Real-time Analytics]
    end
    
    subgraph "☁️ Infrastructure"
        ContainerApps[📦 Azure Container Apps<br/>Serverless Containers]
        KeyVault[🔐 Key Vault<br/>Secrets Management]
        Storage[💾 Blob Storage<br/>File Storage]
        Monitor[📈 Application Insights<br/>Monitoring]
    end
    
    subgraph "🔒 Security"
        AAD[🔐 Azure AD<br/>Identity Provider]
        RBAC[👥 RBAC<br/>Role Management]
        Network[🌐 Virtual Network<br/>Network Security]
        Firewall[🔥 WAF<br/>Application Security]
    end
    
    %% Connections
    WebUI --> API
    Mobile --> API
    PowerBI --> Lakehouse
    Teams --> Foundry
    
    API --> Auth
    API --> Cache
    WebSocket --> Foundry
    
    Foundry --> OpenAI
    Foundry --> Agents
    Foundry --> Embedding
    
    Agents --> Lakehouse
    Lakehouse --> Fabric
    Warehouse --> Fabric
    KQL --> Fabric
    
    API --> ContainerApps
    ContainerApps --> KeyVault
    ContainerApps --> Storage
    ContainerApps --> Monitor
    
    Auth --> AAD
    AAD --> RBAC
    ContainerApps --> Network
    API --> Firewall
    
    %% Styling
    classDef frontend fill:#e1f5fe
    classDef application fill:#f3e5f5  
    classDef ai fill:#e8f5e8
    classDef data fill:#fff3e0
    classDef infrastructure fill:#fce4ec
    classDef security fill:#ffebee
    
    class WebUI,Mobile,PowerBI,Teams frontend
    class API,WebSocket,Auth,Cache application
    class Foundry,OpenAI,Agents,Embedding ai
    class Fabric,Lakehouse,Warehouse,KQL data
    class ContainerApps,KeyVault,Storage,Monitor infrastructure
    class AAD,RBAC,Network,Firewall security
```

---

## Data Flow

```mermaid
graph TD
    subgraph "🔄 Ingestion Layer"
        Files[📄 Raw Files<br/>CSV, Parquet, JSON]
        Streaming[🌊 Streaming Data<br/>Event Hubs, IoT]
        APIs[🔌 External APIs<br/>REST, GraphQL]
    end
    
    subgraph "🥉 Bronze Layer (Raw)"
        BronzeData[📦 Bronze Tables<br/>- Exact copy of source<br/>- All historical data<br/>- Minimal validation]
        BronzeFiles[📁 Bronze Files<br/>- Original format<br/>- Partitioned by date<br/>- Audit trail]
    end
    
    subgraph "🥈 Silver Layer (Cleansed)"
        SilverData[🧹 Silver Tables<br/>- Data quality rules<br/>- Standardized formats<br/>- Deduplicated]
        DataQuality[✅ Quality Checks<br/>- Null validation<br/>- Format validation<br/>- Business rules]
    end
    
    subgraph "🥇 Gold Layer (Curated)"
        Dimensions[📐 Dimension Tables<br/>- Customer<br/>- Product<br/>- Geography<br/>- Date]
        Facts[📊 Fact Tables<br/>- Sales<br/>- Orders<br/>- Inventory<br/>- Events]
        Aggregates[📈 Aggregate Tables<br/>- Daily summaries<br/>- Monthly totals<br/>- KPI calculations]
    end
    
    subgraph "📊 Consumption Layer"
        PowerBI[📊 Power BI<br/>DirectQuery/Import]
        DataAgent[🤖 Data Agents<br/>NL Queries]
        API[🔌 REST APIs<br/>Application Integration]
        Notebooks[📓 Notebooks<br/>Data Science]
    end
    
    %% Flow connections
    Files --> BronzeData
    Streaming --> BronzeData
    APIs --> BronzeData
    Files --> BronzeFiles
    
    BronzeData --> SilverData
    BronzeFiles --> SilverData
    SilverData --> DataQuality
    
    DataQuality --> Dimensions
    DataQuality --> Facts
    Facts --> Aggregates
    Dimensions --> Facts
    
    Dimensions --> PowerBI
    Facts --> PowerBI
    Aggregates --> PowerBI
    
    Dimensions --> DataAgent
    Facts --> DataAgent
    
    Facts --> API
    Aggregates --> API
    
    SilverData --> Notebooks
    Facts --> Notebooks
    
    %% Transformations
    subgraph "🔧 Transformation Logic"
        ETL[⚙️ ETL Notebooks<br/>- Python/PySpark<br/>- SQL Transformations<br/>- Data Pipelines]
        Schedule[⏰ Scheduling<br/>- Hourly refresh<br/>- Daily batch<br/>- Real-time streaming]
    end
    
    ETL -.-> SilverData
    ETL -.-> Facts
    ETL -.-> Dimensions
    Schedule -.-> ETL
    
    %% Styling
    classDef ingestion fill:#e3f2fd
    classDef bronze fill:#8d6e63,color:#fff
    classDef silver fill:#90a4ae,color:#fff  
    classDef gold fill:#ffb300,color:#fff
    classDef consumption fill:#4caf50,color:#fff
    classDef transformation fill:#9c27b0,color:#fff
    
    class Files,Streaming,APIs ingestion
    class BronzeData,BronzeFiles bronze
    class SilverData,DataQuality silver
    class Dimensions,Facts,Aggregates gold
    class PowerBI,DataAgent,API,Notebooks consumption
    class ETL,Schedule transformation
```

---

## Conversational Flow

```mermaid
sequenceDiagram
    participant User as 👤 Usuário
    participant UI as 🌐 Interface Web
    participant API as 🔌 FastAPI Backend
    participant Foundry as 🧠 AI Foundry
    participant Agent as 🤖 Data Agent
    participant Lakehouse as 🏗️ Lakehouse
    participant OpenAI as 🤖 Azure OpenAI
    
    Note over User,OpenAI: Fluxo de Consulta Conversacional
    
    User->>UI: "Qual foi o total de vendas em 2023?"
    UI->>API: POST /chat/message
    
    Note over API: Validação e autenticação
    API->>Foundry: Enviar mensagem via SDK
    
    Note over Foundry: Processamento da intenção
    Foundry->>OpenAI: Analisar linguagem natural
    OpenAI-->>Foundry: Contexto e intenção
    
    Note over Foundry: Decisão de usar ferramenta
    Foundry->>Agent: Converter para SQL
    
    Note over Agent: Geração de query
    Agent->>Agent: NL to SQL conversion
    Agent->>Lakehouse: Executar query SQL
    
    Note over Lakehouse: Processamento de dados
    Lakehouse-->>Agent: Resultados da query
    
    Note over Agent: Formatação dos dados
    Agent-->>Foundry: Dados estruturados
    
    Note over Foundry: Geração de resposta
    Foundry->>OpenAI: Formatar resposta amigável
    OpenAI-->>Foundry: Texto formatado
    
    Note over Foundry: Resposta final
    Foundry-->>API: Resposta completa
    
    Note over API: Processamento final
    API-->>UI: JSON response
    
    Note over UI: Renderização
    UI-->>User: "Total de vendas em 2023: R$ 2.4M"
    
    %% Error handling
    rect rgb(255, 230, 230)
        Note over Agent,Lakehouse: Tratamento de Erros
        Agent->>Lakehouse: Query inválida
        Lakehouse-->>Agent: Erro SQL
        Agent-->>Foundry: Erro + sugestão
        Foundry-->>User: "Não encontrei dados para 2023..."
    end
    
    %% Performance optimization
    rect rgb(230, 255, 230)
        Note over API,Agent: Otimizações
        API->>API: Cache de respostas
        Agent->>Agent: Cache de queries
        Foundry->>Foundry: Context management
    end
```

---

## Security Model

```mermaid
graph TB
    subgraph "🔐 Identity Layer"
        AAD[🔐 Azure Active Directory<br/>- User authentication<br/>- Service principals<br/>- Conditional access]
        MFA[📱 Multi-Factor Auth<br/>- SMS/App verification<br/>- Hardware tokens<br/>- Biometric]
        PIM[👑 Privileged Identity<br/>- Just-in-time access<br/>- Approval workflows<br/>- Time-bound roles]
    end
    
    subgraph "🛡️ Authorization Layer"
        RBAC[👥 Role-Based Access<br/>- Admin<br/>- Contributor<br/>- Viewer<br/>- Custom roles]
        ABAC[🏷️ Attribute-Based<br/>- Department<br/>- Location<br/>- Clearance level<br/>- Time-based]
        RLS[🔒 Row-Level Security<br/>- Customer data isolation<br/>- Regional restrictions<br/>- Hierarchical access]
    end
    
    subgraph "🔒 Data Protection"
        Encryption[🔐 Encryption<br/>- At rest (AES-256)<br/>- In transit (TLS 1.3)<br/>- Customer-managed keys]
        DLP[🛡️ Data Loss Prevention<br/>- Sensitive data detection<br/>- Policy enforcement<br/>- Incident response]
        Masking[🎭 Data Masking<br/>- Dynamic masking<br/>- Static masking<br/>- Tokenization]
    end
    
    subgraph "🌐 Network Security"
        VNet[🌐 Virtual Network<br/>- Network isolation<br/>- Subnet segmentation<br/>- NSG rules]
        Firewall[🔥 Web App Firewall<br/>- OWASP protection<br/>- Rate limiting<br/>- Bot protection]
        PrivateLink[🔗 Private Endpoints<br/>- No public internet<br/>- DNS integration<br/>- Traffic isolation]
    end
    
    subgraph "📊 Monitoring & Compliance"
        Audit[📋 Audit Logging<br/>- All data access<br/>- Administrative actions<br/>- Query execution<br/>- Failed attempts]
        SIEM[🚨 Security Information<br/>- Real-time monitoring<br/>- Threat detection<br/>- Incident response]
        Compliance[✅ Compliance<br/>- GDPR compliance<br/>- SOC 2 certification<br/>- Industry standards]
    end
    
    subgraph "🔑 Secrets Management"
        KeyVault[🔐 Azure Key Vault<br/>- API keys<br/>- Connection strings<br/>- Certificates<br/>- Encryption keys]
        MSI[🎭 Managed Identity<br/>- No stored credentials<br/>- Automatic rotation<br/>- Azure AD integration]
        Rotation[🔄 Key Rotation<br/>- Automated rotation<br/>- Version management<br/>- Zero-downtime updates]
    end
    
    %% Connections showing security flow
    AAD --> RBAC
    AAD --> MFA
    AAD --> PIM
    
    RBAC --> RLS
    ABAC --> RLS
    PIM --> RBAC
    
    Encryption --> DLP
    DLP --> Masking
    
    VNet --> PrivateLink
    Firewall --> VNet
    
    Audit --> SIEM
    SIEM --> Compliance
    
    KeyVault --> MSI
    MSI --> Rotation
    
    %% Data flow security
    RLS -.-> Audit
    Masking -.-> Audit
    PrivateLink -.-> Audit
    
    %% Styling
    classDef identity fill:#e8eaf6
    classDef authorization fill:#f3e5f5
    classDef protection fill:#e0f2f1
    classDef network fill:#fff3e0
    classDef monitoring fill:#fce4ec
    classDef secrets fill:#f1f8e9
    
    class AAD,MFA,PIM identity
    class RBAC,ABAC,RLS authorization
    class Encryption,DLP,Masking protection
    class VNet,Firewall,PrivateLink network
    class Audit,SIEM,Compliance monitoring
    class KeyVault,MSI,Rotation secrets
```

---

## 📝 Como Usar os Diagramas

### No GitHub
Os diagramas Mermaid são renderizados automaticamente no GitHub quando visualizados em arquivos `.md`.

### Localmente
1. **VS Code:** Use a extensão "Mermaid Preview"
2. **Browser:** Use o [Mermaid Live Editor](https://mermaid.live/)
3. **Exportar:** Converta para PNG/SVG usando ferramentas online

### Em Documentação
```markdown
<!-- Incluir diagrama -->
![Architecture Diagram](./diagrams/overall-architecture.md#overall-architecture)
```

### Personalização
Os diagramas podem ser editados para refletir:
- Configurações específicas do ambiente
- Componentes adicionais implementados
- Fluxos customizados por organização

---

**💡 Dica:** Mantenha os diagramas atualizados conforme a arquitetura evolui!