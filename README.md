# Case Técnico Dadosfera — Julio Baltazar

## O problema do cliente

Meu cliente fictício é uma grande empresa de e-commerce especializada em produtos de hardware e eletrônicos (notebooks, componentes de PC, periféricos, wearables). Hoje, os dados desse catálogo — mais de 118 mil produtos — estão numa planilha bruta, sem organização, sem checagem de qualidade e sem nenhuma camada de análise em cima. Isso significa decisões mais lentas e mais caras: ninguém consegue responder rápido "quais categorias vendem mais", "onde estão os problemas de dado" ou "quais produtos merecem destaque", sem antes gastar tempo limpando e cruzando planilhas manualmente.

## A solução construída

Usando a Plataforma Dadosfera, percorri o ciclo de vida completo do dado — de bruto a pronto para decisão — resolvendo uma dor específica do cliente em cada etapa:

| Dor do cliente | Etapa do case | O que foi construído |
|---|---|---|
| "Meus dados de produto estão espalhados e brutos" | [Item 1](item1/item1_base_dados.md) + [Item 2](item2/item2_integracao.md) | Base de 118.338 produtos de hardware/eletrônicos centralizada e carregada na plataforma |
| "Não sei documentar nem organizar o que eu tenho" | [Item 3](item3/item3_catalogacao.md) | Catálogo documentado com dicionário de dados e zona (Raw) do Data Lake |
| "Não confio nos meus dados" | [Item 4](item4/item4_relatorio_qualidade_dados.md) | Relatório de qualidade com great-expectations, identificando 3,7% de produtos sem preço e 14% sem avaliação, com plano de tratamento |
| "Tenho dado de texto bagunçado (título de produto) que eu não aproveito" | [Item 5](item5/item5_llm_features.md) | Extração automática de features estruturadas (marca, conectividade, público-alvo) via LLM |
| "Preciso de resposta rápida pra decisão, não de planilha crua" | [Item 6](item6/item6_modelagem_dados.md) + [Item 7](item7/item7_dashboard.md) | Modelagem dimensional (Kimball) + dashboard com 5 visualizações, incluindo análise de categoria e série temporal |
| "Preciso automatizar o processamento, não repetir tudo manualmente" | [Item 8](item8/item8_pipeline.md) | Pipeline de 4 etapas (Extração → Qualidade → Modelagem → Carga), replicando o conceito de Steps da Dadosfera |
| "Quero conseguir usar isso no dia a dia sem depender de um analista" | [Item 9](item9/item9_data_app.md) | Data App em Streamlit para exploração self-service dos dados, publicado no Streamlit Community Cloud |

## Planejamento do projeto

O planejamento e acompanhamento de todas as etapas foi feito via Kanban board — ver [Item 0](item0/item0_planejamento.md).

## Estrutura do repositório

```
├── README.md                  → este arquivo (narrativa geral do case)
├── app.py                     → código do Data App (Streamlit) — fica na raiz por exigência do deploy
├── requirements.txt           → dependências do Data App
├── produtos_hardware_eletronicos_app.csv → base usada pelo Data App
├── item0/  → Planejamento (Kanban board)
├── item1/  → Base de dados
├── item2/  → Integração (upload na Dadosfera)
├── item3/  → Catalogação (Data Lake)
├── item4/  → Qualidade de dados
├── item5/  → Extração de features via LLM
├── item6/  → Modelagem de dados (Kimball)
├── item7/  → Dashboard e visualizações
├── item8/  → Pipeline de dados
├── item9/  → Data App
└── item10/ → Apresentação final (vídeo)
```

## Conclusão (prova de conceito)

Ao final deste case, uma base de 118 mil produtos brutos foi transformada em uma plataforma de dados funcional: catalogada, com qualidade auditada, enriquecida via IA, modelada dimensionalmente e pronta para consumo analítico via dashboard e Data App — tudo dentro da Dadosfera (ou abstraído para ambientes equivalentes, quando módulos específicos não estavam disponíveis no ambiente de treinamento). Isso demonstra, na prática, o argumento central da Dadosfera: ela é o caminho mais rápido entre dados brutos e valor de negócio.

Mais detalhes sobre viabilidade e próximos passos estão na apresentação em vídeo — ver [Item 10](item10/item10_apresentacao.md).
