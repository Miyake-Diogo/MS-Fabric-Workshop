![Banner](../assets/purview-ref/banner.png)

# Lab 03: Gerenciando Data Sources

## Tarefa 1: Registrando Data Sources

> Microsoft Purview Solution: Data Map

**⏰ Duração:** 30 minutos

**🎯 Resultado:** Ao final desta tarefa você terá registrado uma série de data sources no Data Map. Eles poderão ser escaneados, trazendo metadados técnicos que ficarão disponíveis para usuários via Unified Catalog.

### Por que registrar Data Sources?

> Fonte: [Managing Data Sources](https://learn.microsoft.com/en-us/purview/manage-data-sources)

O Purview Data Governance permite registrar, gerenciar e mover data sources no Data Map da organização. Isso facilita a categorização e o controle de acesso aos dados.

[Registrar](https://learn.microsoft.com/purview/how-to-create-and-manage-collections#register-source-to-a-collection) é obrigatório para que o Purview escaneie o source e leia metadados técnicos e lineage (dependendo do [connector](https://learn.microsoft.com/purview/microsoft-purview-connector-overview#microsoft-purview-data-map-available-data-sources)).

Para registrar um data source, é necessário ser [Data Source Admin](https://learn.microsoft.com/purview/governance-roles-permissions#domain-and-collection-permissions:~:text=and%20glossary%20terms.-,Data%20source%20administrator,-%2D%20a%20role%20that) e ter acesso individual ao source. O processo envolve selecionar 'Data sources' no Data Map, escolher o tipo e preencher o formulário de registro.

**_NB_** - A maioria dos data sources tem requisitos específicos para registro e escaneamento, como configurações de rede (private endpoints/firewall), habilitar identidade do Purview para acesso 'read', etc. Estes tópicos estão fora do escopo deste masterclass.

Normalmente, data sources são registrados uma vez por equipe de TI central ou via IaC (Terraform/ARM), com privilégios elevados. Isso garante consistência e que pré-requisitos sejam atendidos.

### Exercício: Adicionando Data Sources

**🫂 Atividade em Grupo:** [15 minutos] Revise os [supported data sources](https://learn.microsoft.com/purview/microsoft-purview-connector-overview) e discuta quais serão onboarded primeiro. Comece por algo simples (ex: Azure SQL Database ou Azure Data Lake Storage).

- Quais são os data sources comuns na organização?
- Onde estão esses data sources? Azure, outro cloud, on-premises?
- Quais ativos devem ser priorizados para maior benefício ao negócio?
- Tem data sources fora da lista suportada? </br>
  **_NB_** - Evite integrações customizadas, pois geram responsabilidades de Product Manager durante todo o ciclo de vida.

**✨ Dica:** O Purview atualiza seu [roadmap](https://learn.microsoft.com/purview/whats-new#whats-planned-for-microsoft-purview) com novos connectors planejados.

**✍️ Faça no Purview:** [15 minutos] Usando o Data Map, registre um data source pelo wizard. Selecione o domain e collection onde será registrado. Tenha certeza da hierarquia antes de continuar.

![Botão Register data source](../assets/purview-ref/register-datasource-button.png)

Após registro, o Data Map precisa ser populado via escaneamento. Próximo passo:

- Navegue até o overview do data source e observe data de registro, collection path, hierarquia.
- O data source deve ser habilitado para enforcement de políticas de acesso automatizadas? (configurado em tarefas futuras)

**✨ Dica:** Como um data source só pode ser registrado uma vez, se for compartilhado entre Unified Catalog - [Governance domains](https://learn.microsoft.com/purview/what-is-data-catalog#governance-domains), pode ser melhor registrar em uma parent collection compartilhada.

- Veja mais [best practices](https://learn.microsoft.com/purview/concept-best-practices-domains-and-gov-domains) na documentação.

Após registrar, é possível mover o source para outra collection no mesmo domain, se tiver acesso. Ao mover, os scans vão junto, mas os assets **não aparecem** na nova collection até o próximo scan.

---

## Tarefa 2: Configurar Scans de Data Source

> Microsoft Purview Solution: Data Map

**⏰ Duração:** 20 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá escaneado os data sources registrados para popular o Data Map com 'Data Assets'.

### Exercício: Escaneando um Data Source

**🫂 Atividade em Grupo:** [10 minutos] O Purview escaneia metadados técnicos com amostra de linhas. Discuta a frequência ideal de escaneamento para cada data source.

Desde janeiro de 2025, não há custo de compute para escanear data sources no Purview. Pode escanear com a frequência desejada sem custo adicional, mas consome recursos de rede fora do Purview.

Boas práticas de escaneamento continuam importantes. Perguntas para considerar:

- Com que frequência o schema evolui?
- Quais camadas do data lake devem ser escaneadas?
- Faz sentido escanear diariamente ou semanalmente/mensalmente?
- Precisa escanear em runtime específico? Azure auto-resolved ou self-hosted?
- Qual credencial usar? Recomenda-se a Purview system-assigned managed identity ([SAMI](https://learn.microsoft.com/purview/register-scan-azure-sql-managed-instance#:~:text=The%20Microsoft%20Purview%20system%2Dassigned%20managed%20identity%20is%20created%20automatically%20when%20the%20account%20is%20created%20and%20has%20the%20same%20name%20as%20your%20Microsoft%20Purview%20account.))
- Qual nível de scan é apropriado?
- Em qual collection os assets devem ser escaneados?
- Scans completos ou incrementais?

**✨ Dica:** Não escaneie pastas onde dados são criados mais rápido que o scan executa (ex: arquivos em raw zone criados a cada segundo). Pode gerar ciclo infinito e latência.

**✍️ Faça no Purview:** [10 minutos] Configure um scan para um data source selecionado.

1. Selecione o data source e clique em 'New Scan'.
   ![Configurar novo Data Source Scan](../assets/purview-ref/data-map-configure-scan-button.png)

2. Configure nome, credencial e nível de scan. Defina em qual collection os assets serão escritos. Dê acesso à SAMI. Teste a conexão e prossiga.
   ![Configurar Scan Details](../assets/purview-ref/configure-scan-details.png)

3. Os próximos passos dependem do tipo de data source, mas normalmente envolvem selecionar escopo, tipos de arquivos, scan rule set e frequência.

Selecione 'Run Once', salve e execute o scan. Após configurar, abra o Data Source e veja os scans recentes, cada um com opções de trigger, editar ou deletar.

![Data Source Overview](../assets/purview-ref/data-source-overview.png)

**⏸️ Aguarde:** O scan precisa terminar antes de avançar. Use a aba 'Monitoring' ou Scan Details para acompanhar o status.

## Tarefa 3: Definindo Scan Rule Sets

> Microsoft Purview Solution: Data Map

**⏰ Duração:** 20 minutos

**🎯 Resultado:** Ao final desta tarefa, você entenderá scan rule sets, como implementar e quando usar para otimizar escaneamento.

### Entendendo Scan Rule Sets

> Fonte: [Creating Scan Rule Sets](https://learn.microsoft.com/en-us/purview/create-a-scan-rule-set)

O Purview tem scan rule set padrão para cada tipo de data source. Eles escaneiam os tipos de arquivo e metadados mais comuns. Cada scan ingere metadados e aplica classificações. Existem mais de 200+ classificações, de IDs governamentais, financeiros, pessoais, segurança... até classificações customizadas.

![Scan Rule Set](../assets/purview-ref/scan-rule-set-overview.png)

O rule set padrão é um bom começo, mas pode criar sets customizados conforme aprende sobre seus dados. Por exemplo, pode excluir tipos de arquivo ou aplicar classificações específicas.

Como scans consomem recursos, otimize rule sets para escanear só o necessário e aplicar classificações esperadas. Isso melhora performance. Não faz sentido analisar para `Argentina National Identity (DNI) Number` se sabe que não existe esse dado.

**✨ Dica:** Só pode usar o scan rule set no domain onde foi criado.

### Exercício: Criando Scan Rule Set

**🫂 Atividade em Grupo:** [10 minutos] Discuta a necessidade de scan rule sets customizados. Considere:

- Existem tipos de arquivo que devem ser excluídos?
- Existem classificações que devem ser aplicadas a tipos específicos?
- Existem classificações que devem ser excluídas?

**✍️ Faça no Purview:** [10 minutos] Crie um scan rule set customizado para um data source já escaneado. Selecione a aba 'Scan rule sets' e clique em 'New'.

## Tarefa 4: Classificações

> Microsoft Purview Solution: Data Map

**⏰ Duração:** 10 minutos

**🎯 Resultado:** Ao final desta tarefa, você entenderá classificações system e custom no Purview, incluindo como configurar.

### Entendendo Classificações

> Fonte: [Classifications](https://learn.microsoft.com/en-us/purview/concept-classification)

Classificações são aplicadas no escaneamento e servem para categorizar e rotular data assets. O Purview tem várias classificações internacionais padrão, mas pode criar customizadas para detectar e marcar dados específicos.

**Exemplo:** Como classificações aparecem em uma Azure SQL Table:
![Asset-level Classifications](../assets/purview-ref/asset-level-classifications.png)

**Exemplo:** Como classificações de schema aparecem:
![Schema-level Classifications](../assets/purview-ref/schema-level-classifications.png)

#### Classificações Customizadas

Se não existe uma classificação pronta, pode criar uma customizada (regex ou dictionary lookup). Define a porcentagem de linhas amostradas que devem bater para aplicar a classificação. Quanto menor, maior risco de falso positivo.

Exemplo: ID de Invoice formatado (ex: INV-123-XYZ) ou handle do X (ex: @username).

### Exercício: Criando Classificação Customizada

**✍️ Faça no Purview:** [10 minutos] Crie a classificação customizada conforme atividade anterior.

1. No Data Map, vá em 'Annotation Management' > 'Classifications'. Clique '+ New' e preencha nome e descrição.
   ![New Classification](../assets/purview-ref/new-classification.png)

2. Associe uma regra de classificação. Clique '+ New' em 'Classification Rules'.
   - Preencha nome e descrição.
   - Associe à classificação criada.
   - Deixe 'Enabled'.
   - Selecione o tipo (ex: Regular Expression).
   ![Create Classification Rule](../assets/purview-ref/new-classification-rule.png)

   Clique 'Continue'.

3. Configure a regex. Pode subir sample data ou informar o padrão.
   - Especifique o Data Pattern.
   - Defina o Minimum Match Threshold (percentual mínimo para aplicar classificação).
     **✨ Dica:** Valor sugerido é 60%. Se usar múltiplos padrões, fica fixo em 60%.
   - Pode definir padrão para nome de coluna também.
   ![Test Classification Rule](../assets/purview-ref/test-classification-rule.png)

   Clique 'Create' para confirmar.

Pode revisar Scan Rule Sets para incluir a nova classificação.

**✨ Dica:** Se deletar uma regra, pode definir o que acontece onde ela está aplicada.

![Delete Classification Rule](../assets/purview-ref/delete-classification-rule.png)

## Tarefa 5: Entendendo Integration Runtimes

> Microsoft Purview Solution: Data Map

**⏰ Duração:** 10 minutos

**🎯 Resultado:** Ao final desta tarefa, você entenderá os tipos de integration runtimes disponíveis no Purview.

### Entendendo Integration Runtimes

> Fonte: [Choose the right integration runtime](https://learn.microsoft.com/en-us/purview/choose-the-right-integration-runtime-configuration)

O Purview usa integration runtimes (IR) para conectar data sources e prover compute para scans. Nem todo data source suporta todos os tipos de IR.

Podem ser auto-resolved pelo Azure ou self-hosted pela organização. A escolha depende do data source e da configuração de rede.

Tipos:
- **Azure Integration Runtime:** Gerenciado pelo Azure, conecta data sources Azure. Auto-resolved, sem configuração extra.
- **Managed Virtual Network (VNet) Integration Runtime:** Conecta data sources em VNet. Auto-resolved, sem configuração extra.
- **Self-hosted Integration Runtime:** Hospedado na rede da organização, conecta data sources on-premises. Requer configuração extra.
- **Kubernetes supported Self-Hosted Integration Runtime (Preview):** Conecta data sources on-premises. Requer configuração extra.
- **AWS Integration Runtime:** Conecta data sources AWS.

**✨ Dica:** Considere a configuração de rede e o data source ao escolher IR. Para on-premises, use self-hosted.

**🫂 Atividade em Grupo:** [10 minutos] Revise os IR disponíveis e discuta quais são mais adequados para a organização.

## Tarefa 6: Monitoramento

> Microsoft Purview Solution: Data Map

Cada scan tem um Run ID único. Veja o status geral na aba Monitoring do Data Map e aprofunde em cada categoria.

![Data Map Monitoring](../assets/purview-ref/data-map-monitoring.png)

Mais detalhes:

![Scan Status](../assets/purview-ref/data-map-scan-status.png)

Informações adicionais (incluindo logs) disponíveis.

### Exercício: Monitore seus scans

**✍️ Faça no Purview:** [5 minutos] Familiarize-se com os tipos de status e logs disponíveis na aba Monitoring.

- O scan do Task 2 foi concluído? Se não, consegue descobrir o motivo?

---

**⏸️ Reflexão:** Agora você registrou data sources, configurou scans e definiu scan rule sets no Purview. Aprendeu sobre classificações e como criar customizadas. Também entendeu integration runtimes e como conectar data sources.

O que isso significa? Agora está pronto para mapear dados em governance domains.

Cada vez que um data source é onboarded, siga estes passos:

![Data Source Onboarding Process](../assets/purview-ref/data-source-onboarding-process.png)

Antes de sair, revise esta seção para entender o que é necessário ao conectar novos data sources ou escalar o Purview.

👉 [Continue: Lab 4](./Lab-04%20-%20Governance%20Domains%20and%20Terms.md)
