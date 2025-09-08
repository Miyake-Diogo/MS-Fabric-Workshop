![Banner](../assets/purview-ref/banner.png)

# Lab 01: Introdução & Visão Executiva

## Tarefa 1: Boas-vindas e Apresentações

**⏰ Duração:** 30 minutos

**🎯 Resultado:** Como passaremos 8 horas ou mais juntos, vamos nos conhecer e entender seu envolvimento no programa de governança de dados.

**🫂 Atividade em Grupo:**
1. Apresente-se: Nome, cargo na organização, definição pessoal de Data Governance.
2. Facilitador apresenta o tema e agenda do treinamento.
3. "Como chegamos até aqui?" - Compartilhe o estado atual da governança de dados na sua organização e desafios de maturidade/técnicos.

O facilitador conduz uma conversa em grupo com os seguintes prompts:

**Maturidade em Governança de Dados**
- Você tem um [Data Steward](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/organize-roles-responsibilities#:~:text=Platform%20group%2C%20governance-,Data%20Steward,-Data%20Trustee) na organização? Quem é?
- Já possui um [data catalog](https://learn.microsoft.com/purview/what-is-data-catalog#:~:text=Data%20Catalog%20experience%20allows%20you%20to%20explore%20and%20understand%20your%20data)? Como funciona? É efetivo?

**Requisitos**
- Sua organização está sujeita a [compliance](https://learn.microsoft.com/azure/compliance/) que exige metadados em região específica? Onde está o data catalog hoje?
- Já possui políticas de [Data Security](https://learn.microsoft.com/purview/purview?view=o365-worldwide#data-security) M365 - Enterprise (Information Protection / Sensitivity Labels, Insider Risk Management, Information Barriers etc)?
- Tem política de [AI / Generative AI](https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/responsible-ai#the-responsible-ai-principles)? Como gerencia riscos de exposição de dados?
- Existem sistemas on-premises que devem ser catalogados?
- Consome fontes de dados externas/APIs críticas?

**Implementação**
- Quais métricas de sucesso importam para os stakeholders?
- Considerando que governança de dados é interdisciplinar, já identificou casos de uso e stakeholders?
- Já definiu como os custos de governança serão distribuídos?
- Planejou o caminho para produção? Tem datas para go-live do data catalog?

## Tarefa 2: Visão Executiva

**⏰ Duração:** 75 minutos

**🎯 Resultado:** O facilitador apresenta uma visão executiva sobre governança de dados, tendências do setor e o aplicativo Purview Data Governance.

Apresenta o [Cloud Adoption Framework](https://learn.microsoft.com/azure/cloud-adoption-framework/) para Governança de Dados.

![Overview](../assets/purview-ref/data_gov_overview.png)

- Define [Data Governance](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/overview-cloud-scale-analytics#govern-your-analytics-estate) e seu valor.
- Discute o [modelo de maturidade](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/govern#data-governance-maturity-model) e convida o grupo a avaliar sua organização.
- Discute requisitos típicos de [governança de dados](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/govern-requirements).
- Discute [processos de governança](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/govern-components).
- Apresenta o [modelo de referência para planejamento](https://learn.microsoft.com/purview/data-catalog-get-started?view=o365-worldwide#reference-model-for-planning).

Discute as [recomendações de classificação de dados](https://learn.microsoft.com/azure/well-architected/security/data-classification) do [Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/), destacando que muitas organizações já têm políticas de classificação, mas ainda estão evoluindo a taxonomia.

Apresenta os desafios do setor e introduz o Microsoft Purview.

Resumo: Purview Data Governance contém dois componentes principais:
