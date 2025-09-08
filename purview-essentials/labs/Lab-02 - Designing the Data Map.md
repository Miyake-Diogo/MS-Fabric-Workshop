![Banner](../assets/purview-ref/banner.png)

# Lab 02: Design do Data Map

## Tarefa 1: Considere o Design

> Microsoft Purview Solution: Data Map

**⏰ Duração:** 30 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá respondido perguntas importantes que ajudarão a estruturar o workshop e focar a sessão.

**🫂 Atividade em Grupo:** [30 minutos] Juntos, revisite as perguntas do início do Lab 1, adicionando detalhes para guiar os próximos exercícios.

- Você está interessado nas capacidades de Security, Privacy e Compliance do Purview, ou apenas em Data Governance sobre dados estruturados?
- Você possui a licença Microsoft 365 Enterprise para testar os recursos de Security/Privacy/Compliance?
- Já existem políticas de Data Security M365 - E3/E5 (Information Protection, Insider Risk Management, Information Barriers etc)?
- Existem serviços on-premises que precisam ser considerados/avaliados como parte da iniciativa de Data Governance / catalogação do Purview?
- Considerando que governança de dados é interdisciplinar, você identificou casos de uso e stakeholders em toda a empresa?
- Você já definiu como os custos de governança de dados serão distribuídos?
- Você planejou o caminho para produção?

Se não conseguiu responder muitas dessas perguntas, busque clareza ao final da sessão/workshop, quando as capacidades ficarem mais claras.

## Tarefa 2: Crie seus Platform Domains

> Microsoft Purview Solution: Data Map

**⏰ Duração:** 10 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá implementado um platform domain e poderá dividir seu Purview Data Map conforme ambiente, isolamento e requisitos de segurança.

### Entendendo Platform Domains

> Fonte: [Domains](https://learn.microsoft.com/purview/concept-domains)

O Microsoft Purview introduziu ['domains'](https://learn.microsoft.com/purview/concept-domains) (não confundir com [Governance Domains](https://learn.microsoft.com/purview/what-is-data-catalog#governance-domains)) como estrutura dentro do Data Map. Domains distribuem responsabilidade organizacional, criam separação lógica e garantem gestão consistente entre assets e glossários.

Uma das maiores mudanças na nova experiência é a substituição de múltiplas contas de governança de dados (classic Azure Purview) por múltiplos domains sob uma conta Purview padrão para o tenant.

**Fatos Importantes:**

- Todo Data Map começa com um [default domain](https://learn.microsoft.com/purview/concept-domains#default-domain), que é a root collection da conta principal após o upgrade para a nova experiência.
  - Até 4 domains customizados podem ser criados para melhor organização e governança.
- Um novo papel, [Domain Admin](https://learn.microsoft.com/purview/governance-roles-permissions#domain-and-collection-permissions:~:text=roles%20are%20currently%3A-,Domain%20admin,-(domain%20level)), pode ser atribuído. Ele pode gerenciar permissões e recursos do domain.
- É possível [merge](https://learn.microsoft.com/purview/merge-domain?source=docs) contas Azure Purview clássicas do tenant na nova experiência usando domains.

![Um tenant contém múltiplos domains, cada um com collections e glossários](../assets/purview-ref/tenant-with-domains.png)

- Cada Data Map tem 1-5 Domains. Cada Domain pode ter até [256 collections](https://learn.microsoft.com/purview/concept-best-practices-collections#:~:text=A%20collections%20hierarchy%20in%20a%20Microsoft%20Purview%20can%20support%20as%20many%20as%20256%20collections%2C%20with%20a%20maximum%20of%20eight%20levels%20of%20depth.), com até oito níveis de profundidade.

### Entendendo Collections dentro dos Domains

> Fonte: [Manage Domains and Collections](https://learn.microsoft.com/en-us/purview/how-to-create-and-manage-domains-collections)

No contexto do Purview, collections organizam recursos como data sources, scans e assets dentro de um domain. Cada domain começa com uma root collection e pode conter várias sub collections.

![Criando uma nova Collection](../assets/purview-ref/creating-new-collection.png)

**Características:**

- Estrutura Hierárquica: Collections formam uma árvore, permitindo organizar recursos em hierarquia com [limites de controle de acesso](https://learn.microsoft.com/purview/how-to-create-and-manage-collections#add-roles-and-restrict-access-through-collections).
- Atribuição de Papéis: Collections suportam atribuição de papéis, permitindo gerenciar acesso e permissões de forma granular (Domain admins, Collection admins, Data curators, etc).
- Gestão de Recursos: Recursos associados à collection são incluídos automaticamente. Dependendo das permissões, podem ser visualizados, editados ou excluídos.
- Movimentação de Recursos: Collections permitem mover [registered sources](https://learn.microsoft.com/purview/how-to-create-and-manage-collections#register-source-to-a-collection) entre collections e adicionar assets.
- Herança: Permissões são herdadas automaticamente da collection pai para as sub collections. Pode ser [restrita/desabilitada](https://learn.microsoft.com/purview/how-to-create-and-manage-domains-collections#restrict-inheritance) conforme necessário.

Para gerenciar collections, é preciso ser Domain Admin ou Collection Admin no [portal de governança do Purview](https://learn.microsoft.com/purview/governance-roles-permissions#domain-and-collection-permissions).

### Exercício: Criar Domains e Collections

**🫂 Atividade em Grupo:** [5 minutos] Identifique se há necessidade de criar múltiplos platform domains no Purview (limite de 4). Eles permitem separar data sources em domains isolados ou unir contas Azure Purview clássicas.

- É necessário criar um setup dev/prod (lembrando que um data source só pode ser registrado em um lugar)?
- É possível usar um único domain (prod) e mudar o status de assets não curados ao invés de usar múltiplos domains?
- Sua organização tem estrutura de empresa mãe/filha e precisa representar isso no Data Map?

> **Seu tenant se enquadra em algum desses casos?** Governo, Saúde, Educação? Se sim, consulte seu contato Microsoft para o melhor setup, pois só é possível criar 4 domains customizados.

**✍️ Faça no Purview:** [5 minutos] Navegue até o Data Map e crie um novo platform/technical domain se necessário. Caso não seja necessário, continue no default domain.

- [Atribua](https://learn.microsoft.com/purview/governance-roles-permissions#add-role-assignments) o(s) admin(s) do domain.

## Tarefa 3: Criar e Estender Sensitivity Labels

> Microsoft Purview Solution: Information Protection

**⏰ Duração:** 30 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá criado sensitivity labels para o tenant na solução Compliance. Elas podem ser adicionadas manualmente (ou automaticamente se houver licença E5 Risk & Compliance) aos data assets na criação ou posteriormente. Você também aprenderá a expandir esses labels para o Data Map para rotular dados estruturados.

### Entendendo Sensitivity Labels

Sensitivity Labels ajudam a classificar e proteger dados organizacionais (geralmente na criação, mas podem ser aplicados/modificados a qualquer momento). Garantem produtividade e colaboração ao 'carimbar' o dado (arquivo, pasta etc) com texto e propriedades de proteção que acompanham o dado onde estiver.

![Sensitivity Label Recommendation](../assets/purview-ref/sensitivity-label-recommendation.png)

Podem ser usadas para controlar acesso via criptografia, adicionar marca d'água e aplicar políticas automaticamente. Isso garante proteção consistente em Teams, SharePoint, chats e reuniões.

Labels são criadas e mantidas em Purview - Information Protection e se estendem ao Power BI, Data Map e até integrações com terceiros. [Supported data sources](https://learn.microsoft.com/en-us/purview/microsoft-purview-connector-overview) (ver coluna 'labeling').

O escopo do label determina suas configurações e disponibilidade em apps e serviços. A ordem na lista define prioridade (labels mais abaixo têm maior prioridade).

![Applying Sensitivity Labels](../assets/purview-ref/applying-sensitivity-labels.png)

Sub labels, ou 'child' labels, agrupam logicamente os labels. Não herdam configurações de proteção do parent, mas herdam cor.

Labels também são reconhecidos por serviços Microsoft como Copilot for Microsoft 365 e Azure Information Protection, que checam direitos de uso do usuário em tempo real, adicionando proteção extra.

### Exercício: Implementar Sensitivity Labels

**🫂 Atividade em Grupo:** [5 minutos] Discuta se sua organização possui licença E3/E5 e se os sensitivity labels já estão configurados.

- Você já usa sensitivity labels e eles são aplicados automaticamente ou manualmente em dados não estruturados (Microsoft 365 apps)?
- Labels são aplicados para todos os usuários (recomendado) ou seletivamente?

**✍️ Faça no Purview:** [5 minutos] Abra a solução Information Protection:

- Crie, revise e publique sensitivity labels organizacionais conforme necessário.
  ![Sensitivity Labels Overview in Microsoft Purview](../assets/purview-ref/sensitivity-labels-overview.png)
- Defina políticas de Auto-labeling conforme necessidade.
- Defina Trainable Classifiers e Sensitive Information Types conforme aplicável.
- Habilite a opção 'Extend Sensitivity Labels to the Purview Data Map'.
  - Novos scans e data sources suportados podem ser rotulados automaticamente.

## Tarefa 4: Adicionando Lineage Connections

> Microsoft Purview Solution: Data Map

**⏰ Duração:** 10 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá conectado uma instância Azure Data Factory e uma conta Azure Data Share ao Data Map. Isso garante que processos ETL (ex: nível de coluna) sejam capturados como lineage após registrar e escanear os data sources conectados.

### Entendendo Data Lineage

Data Lineage representa o ciclo de vida dos dados, rastreando origem e movimentação. Inclui dados brutos, transformados e utilizados por plataformas de visualização.

Compreender lineage é importante para troubleshooting de pipelines, análise de qualidade, compliance e impacto. Mostra como os dados se movem, incluindo transformações e regras de negócio.

![Asset Lineage](../assets/purview-ref/asset-lineage.png)

**Tipos de Lineage:**

- **Entity (ou asset) Lineage:** Lineage em nível de entidade/objeto. Representado como grafo ligando entidades de origem e destino por processos computacionais, tornando o lineage legível.
- **Column-level (ou attribute) lineage:** Lineage em nível de coluna. Identifica colunas de origem usadas para criar/derivar colunas no destino, rastreando mudanças coluna a coluna.

### Exercício: Adicionar Lineage Connections (opcional)

**✍️ Faça no Purview:** [5 minutos] Navegue até 'Source Management' no Data Map, aba 'Lineage connections'. Adicione recursos Azure Data Factory.

![Adding Data Factory Lineage Connections](../assets/purview-ref/data-factory-lineage-connection.png)

Após registro, o Status deve aparecer como: `Connected`

![Data Factory Lineage Overview](../assets/purview-ref/data-factory-lineage-overview.png)

**✍️ Faça no Purview:** [5 minutos] Navegue até 'Source Management', aba 'Lineage connections'. Adicione recursos Azure Data Share.

**✨ Dica:** Cada instância Data Factory ou Azure Data Share só pode ser conectada a uma conta Purview. Não é possível compartilhar uma instância entre contas.

---

**⏸️ Reflexão:** Agora você entendeu a necessidade de múltiplos platform domains e a hierarquia de collections. Aprendeu sobre os papéis que o administrador pode atribuir nos níveis mais altos do Data Map. Experimentou Sensitivity Labels e os estendeu ao Data Map para rotulagem automática.

Por fim, aprendeu sobre os benefícios do lineage, como ferramentas ETL (Azure Data Factory) e serviços de compartilhamento (Azure Data Share) podem ser conectados ao Purview para fornecer informações de lineage.

👉 [Continue: Lab 3](./Lab-03%20-%20Managing%20Data%20Sources.md)
