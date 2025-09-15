# Introdução ao Fabric Lakehouse

## Preparando o Ambiente

### Pré-requisitos
- Acesso ao Microsoft Fabric
- Notebooks do projeto
- Dataset Olist

### Etapas do Tutorial

1. Upload dos Notebooks
Faça o upload de todos os notebooks necessários para o projeto no Microsoft Fabric.

2. Criação do Lakehouse
Após o upload dos notebooks, crie um novo Lakehouse no Microsoft Fabric.

3. Upload do Dataset
Faça o upload dos arquivos do dataset Hollist para o Lakehouse criado.

4. Execução dos Notebooks
Execute os notebooks na seguinte ordem:
1. **Bronze** - Processamento inicial dos dados
2. **Silver** - Transformações intermediárias
3. **Dimensão Gold** - Criação das tabelas dimensão
4. **Fato Gold** - Criação das tabelas fato

5. Acesso aos Dados
Após executar todos os notebooks, você terá acesso completo aos dados estruturados no Lakehouse.

 6. Geração de Relatórios
Com os dados disponíveis, você poderá criar os relatórios necessários para análise.

### Observações Importantes

- **Sobre os Scripts**: Não se preocupe com a complexidade do código. Os notebooks contêm comentários explicativos sobre cada etapa do processo.

- **Estrutura Simplificada**: As criações de tabelas, fatos e dimensões são intencionalmente simples para demonstrar as capacidades do Microsoft Fabric.

- **Flexibilidade**: Este tutorial apresenta uma abordagem básica. Você pode adaptar as estruturas e modelagens de acordo com suas necessidades específicas.


## Referencias
- [Lakehouse Tutorial](https://learn.microsoft.com/pt-br/fabric/data-engineering/tutorial-lakehouse-introduction)
- [Fabric End-to-End Tutorials](https://learn.microsoft.com/pt-br/fabric/fundamentals/end-to-end-tutorials)

