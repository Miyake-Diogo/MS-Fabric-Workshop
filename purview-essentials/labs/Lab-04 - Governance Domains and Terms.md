![Banner](../assets/purview-ref/banner.png)

# Lab 04: Domínios de Governança e Termos

## Tarefa 1: Criando Governance Domains

> Microsoft Purview Solution: Unified Catalog

**⏰ Duração:** 20 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá criado governance domains no Purview.

### Entendendo Governance Domains

No Purview, um 'governance domain' é um conceito abstrato que traz contexto de negócio aos dados técnicos e permite escalar práticas de governança.

Focado em melhorar gestão de ownership, um [governance domain](https://learn.microsoft.com/purview/what-is-data-catalog#governance-domains) é um limite lógico para governança, ownership e descoberta de data products e assets.

![Exemplo de Governance Domains](../assets/purview-ref/governance-domain-overview.png)

**Fatos Importantes**
- Pode representar unidades de negócio, linhas de negócio, domínios de dados, regulatórios ou projetos.
  - Veja [Best Practices](https://learn.microsoft.com/purview/data-catalog-best-practices#create-governance-domains) para decidir abordagem.
- Podem ser hierárquicos, até cinco níveis de profundidade.
  - Exemplo: domínio `Customer` pode conter `Customer Delivery` e `Customer Experience`.
- Tem nome, descrição, owner(s), [data products](https://learn.microsoft.com/purview/what-is-data-catalog#data-products), [glossary terms](https://learn.microsoft.com/purview/what-is-data-catalog#glossary-terms), OKRs e [critical data elements](https://learn.microsoft.com/en-us/purview/what-is-data-catalog#critical-data-elements).
- Definindo categorias, permite busca mais eficiente e alinhamento da governança ao negócio.
- Ajuda a gerenciar catálogo crescente, garantindo governança efetiva. Glossary terms definidos podem ser aplicados a qualquer data product do domínio.

Governance domains usam contexto de negócio para garantir dados mais descobertos e bem governados.

### Exercício: Criando Governance Domains

**🫂 Atividade em Grupo:** [20 minutos] Organize times e discuta os 'domains' da organização. Podem ser departamentos, unidades, etc.

Use whiteboard ou papel para desenhar e documentar.
- Nome do domain.
- Descrição e responsabilidades.
- Owner(s).
- **Opcional:** Discuta [key roles](https://learn.microsoft.com/purview/governance-roles-permissions#governance-domain-level-permission) de stewards, product owners, quality stewards.

Ao final, apresente o design ao grupo. Consolidar tudo em um master diagram para usar nos exercícios seguintes.

**✍️ Faça no Purview:** [10 minutos] Transfira os domains para o Unified Catalog. Marque como '[draft](https://learn.microsoft.com/purview/how-to-create-manage-governance-domains#:~:text=governance%20domain%20until%20its%20status%20is%20set%20to%20Published)' para não aparecer aos usuários até publicar.

![Create Governance Domain](../assets/purview-ref/create-governance-domain.png)

## Tarefa 2: Mapear Governance Domains para Data Map Collections

> Microsoft Purview Solution: Unified Catalog

**🎯 Resultado:** Ao final desta tarefa, você terá mapeado seus governance domains para collections do Data Map.

### Entendendo a relação entre Governance Domains e Data Map Collections

Domains mudam conforme a organização evolui, e responsabilidades também. Ao mapear domains para [Collections](https://learn.microsoft.com/purview/how-to-create-and-manage-collections), cria-se o link entre contexto de negócio e dados técnicos.

Esse link é crucial para garantir governança efetiva. Assim, as pessoas certas ficam responsáveis e políticas corretas são aplicadas aos dados.

**🫂 Atividade em Grupo:** [5 minutos] Discuta a relação entre Collections do Data Map e Governance Domains do Unified Catalog.
- Para um domain, quais hierarquias de Collection devem ser ligadas?
- Quais assets devem ser incluídos?

**✍️ Faça no Purview:** [5 minutos] Faça o mapeamento necessário para escopar os assets relevantes para cada domain.

## Tarefa 3: Criar Glossary Terms

> Microsoft Purview Solution: Unified Catalog

**⏰ Duração:** 10 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá definido um ou mais [terms](https://learn.microsoft.com/purview/how-to-create-manage-glossary-term#create-a-term) para os domains criados.

### Entendendo Glossary Terms

Glossary terms são essenciais para governança, gestão e descoberta de dados. São mais que vocabulário: estão ligados a assets, categorizados e trazem contexto. Termos consistentes simplificam o jargão técnico e melhoram entendimento de negócio.

Termos ajudam stewards a aplicar políticas e escalar governança conforme o estate cresce.

Escalabilidade é alcançada ao transformar termos estáticos em termos ativos com políticas. Assim, políticas são aplicadas automaticamente sempre que o termo é usado em um data product, garantindo segurança e discoverability.

**Fatos Importantes**
- **Terms** são agrupados por domain para dar contexto.
- **Policies** nos termos trazem controles de saúde, requisitos de governança e termos de uso.
- **Custom Attributes (preview)** podem ser adicionados para mais contexto.
- **Publishing** torna o termo visível a todos. [Workflow](https://learn.microsoft.com/purview/how-to-create-manage-glossary-terms#publish) executado após validação.
- **[Linking](https://learn.microsoft.com/purview/how-to-create-manage-glossary-terms#manage-data-product-links) Data Products** permite termos mais contextuais.
- **Related Terms** trazem contexto de negócio e podem ser gerenciados na página do termo.

### Exercício: Criando Glossary Terms

**🫂 Atividade em Grupo:** [5 minutos] Discuta como a organização lida com acrônimos e dicionários de dados.
- Onde novos colaboradores buscam o glossário?
- Tem planilhas grandes de termos?
- Usa SharePoint para termos?
- Seria útil co-locar o glossário com a ferramenta de governança?

**✍️ Faça no Purview:** [5 minutos] Crie novos termos para domains e preencha os campos 'steward' e 'expert'.

**✨ Dica:** Teste o Copilot ([licença dependente](https://learn.microsoft.com/purview/copilot-in-purview-overview)) para gerar termos relevantes. Teste Term Policies. Pode usar [Macula Purview Automate](https://www.maculasys.com/microsoft-purview) para importar planilhas de termos em lote.

## Tarefa 4: Navegar pelo Enterprise Glossary

> Microsoft Purview Solution: Unified Catalog

**⏰ Duração:** 5 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá verificado a experiência de descoberta de termos no Enterprise Glossary.

### Exercício: Navegando pelo Enterprise Glossary

Agora que criou domains e termos, explore o [Enterprise Glossary](https://learn.microsoft.com/purview/enterprise-glossary). É a experiência para usuários finais descobrirem e entenderem os termos.

Para o termo aparecer, ele e o domain devem estar publicados.

**👉 Faça no Purview:** [5 minutos] Navegue até o Enterprise Glossary e explore os termos criados.
- Veja a hierarquia apresentada, informações e status de publicação.
- Se mover para draft, o glossário reflete.
- Se o domain for draft, todos os termos somem do glossário.

---

**⏸️ Reflexão:** Agora você implementou domains e articulou o valor de conceitos de negócio sobre os dados físicos para ajudar na governança. Também criou termos para dar contexto aos assets. Pronto para avançar?

👉 [Continue: Lab 5](./Lab-05%20-%20Curating%20Data%20Assets.md)
