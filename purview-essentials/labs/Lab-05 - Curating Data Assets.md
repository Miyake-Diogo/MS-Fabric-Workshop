![Banner](../assets/purview-ref/banner.png)

# Lab 05: Curadoria de Data Assets

## Tarefa 1: Curadoria de Data Assets

> Microsoft Purview Solution: Unified Catalog

**⏰ Duração:** 20 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá curado uma amostra de data assets dos scans configurados no [Lab 3](./Lab-03%20-%20Managing%20Data%20Sources.md). Eles serão enriquecidos com descrições, tags, classificações, etc., trazendo mais contexto para os usuários.

### Introdução à Curadoria Federada

Curadoria de dados é o processo de organizar e gerenciar data assets para garantir qualidade, precisão e confiabilidade. Envolve enriquecer os dados com metadados (descrições, tags, classificações, lineage, etc.) para torná-los mais descobertos e úteis.

Como os dados são gerados por todas as áreas, é importante pensar no ciclo de curadoria antes de começar.

Tradicionalmente, a curadoria era feita por uma equipe central, partindo do modelo de dados corporativo, buscando representar toda a organização. Esse modelo era lento, caro e difícil de escalar. A orientação da Microsoft é adotar o [modelo federado](https://learn.microsoft.com/purview/what-is-data-catalog#:~:text=we%20believe%20in%20a%20federated%20governance%20approach%3A%20providing%20a%20centralized%20place%20to%20develop%20data%20safety%2C%20quality%2C%20and%20standards%2C%20but%20providing%20tools%20to%20create%20self%2Dservice%20access%20control%2C%20discoverability%2C%20and%20maintenance.), empoderando o negócio para assumir ownership dos dados.

O modelo federado distribui ownership, reduz gargalos e incentiva participação no ciclo de gestão, governança e uso dos dados. Engaja o negócio e empodera especialistas para cuidar dos dados que conhecem melhor.

#### Exemplo de Data Asset Não Curado

![Exemplo Asset - Not Curated](../assets/purview-ref/non-curated-data-asset.png)

No exemplo acima, um Power BI Report. Note como é difícil entender o propósito do asset sem descrição, tags ou classificação. É um problema comum e mostra a importância da curadoria.

Com curadoria básica, o asset pode ser transformado:

![Curated Data Asset](../assets/purview-ref/curated-data-asset.png)

### Exercício: Curadoria de Data Assets

**✍️ Faça no Purview:** [15 minutos] Navegue até um asset no catálogo (via busca/filtros) e expanda a página de overview. Familiarize-se e comece a editar (curar) o asset.

- O nome do asset é significativo para o negócio?
- A linguagem e [taxonomia](https://learn.microsoft.com/azure/well-architected/security/data-classification#:~:text=taxonomy%20to%20assets.-,Taxonomy,-A%20system%20to) estão corretas?
- Pode adicionar descrição rica para informar sobre o asset e seus usos?
- O asset deve ser certificado e considerado confiável?
- O schema está descrito?
- Experts e owners estão atribuídos?
- Precisa adicionar tags para facilitar descoberta?

**_NB_**: O recurso Asset Ratings & Comment está disponível para cada asset. Qualquer Data Map - Collection Data Reader pode contribuir. É ótimo para engajar o negócio e receber feedback. Não confunda com [data quality](https://learn.microsoft.com/purview/data-quality-overview), que será abordado em outro lab.

![Asset Rating Flyout](../assets/purview-ref/asset-rating-flyout.png)

**🫂 Atividade em Grupo:** [5 minutos] Discuta como posicionar o recurso de rating/comentário para os usuários. Que abordagem de change management usar para promover adoção e uso responsável?

**✨ Dica:** Showcases, roadshows, lunch-learns, etc. com boa comunicação são ótimos para engajar e criar entusiasmo pelo serviço.

Ao final da curadoria, acesse a aba History do asset e revise as mudanças feitas. É ótimo para rastrear alterações e saber quem fez.

**✨ Dica:** Use 'Show details' para comparar mudanças. Pode levar minutos para refletir na aba History.

![Asset History Overview](../assets/purview-ref/asset-history-overview.png)

## Tarefa 2: Navegar e Descobrir Data Assets

> Microsoft Purview Solution: Unified Catalog

**⏰ Duração:** 5 minutos

**🎯 Resultado:** Ao final desta tarefa, você terá entendido a experiência de busca de dados no Unified Catalog.

### Exercício: Navegando e Descobrindo Data Assets

Com vários assets curados, é hora de navegar e descobrir no Unified Catalog. Isso ajuda a entender como são organizados e apresentados aos usuários.

**✍️ Faça no Purview:** [5 minutos] Navegue até o Unified Catalog e explore os assets curados via **Data search**. Use a busca por nome, descrição ou tags. Use filtros para refinar por classificação, termos do glossário, etc.

**✨ Dica:** Você pode ver assets diferentes dos colegas, dependendo dos papéis e permissões atribuídos na Collection ou status do Governance Domain.

---

**⏸️ Reflexão:** Agora que aprendeu o básico de curadoria, quais desafios prevê para engajar áreas de negócio? Como superá-los?

👉 [Continue: Lab 6](./Lab-06%20-%20Data%20Products%20and%20Access.md)
