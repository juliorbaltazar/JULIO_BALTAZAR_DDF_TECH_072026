# Item 5 — Extração de Features com LLM

## Objetivo

Transformar o texto livre e desestruturado do título de cada produto em atributos estruturados (marca, conectividade, cor, público-alvo), utilizando Inteligência Artificial — conforme o exemplo do documento original do case.

## Abordagem: híbrida (LLM validado + regras determinísticas em escala)

Durante o desenvolvimento deste item, foram testadas três APIs de LLM (Anthropic Claude, Cerebras/Llama, Google Gemini). Cada uma apresentou, em algum momento, uma limitação de acesso à camada gratuita (esgotamento de crédito, mudança de nome/descontinuação de modelo, ou cota diária muito restrita para os modelos mais recentes — como o `gemini-3.6-flash`, cujo limite gratuito é de apenas 20 requisições/dia). Essas tentativas e os respectivos diagnósticos estão documentados no histórico deste projeto como parte do processo real de engenharia enfrentado.

Diante dessas limitações de tempo e custo, foi adotada uma abordagem híbrida, uma prática comum em ambientes de produção real:

1. **Validação via LLM (qualitativa):** uma amostra de produtos foi processada diretamente por um LLM (Claude), extraindo campos ricos como `marca`, `modelo`, `conectividade`, `cor`, `público-alvo` e `características-chave`, comprovando que a técnica de extração via IA funciona e produz resultado coerente. Exemplo disponível em [`item5_exemplo_extracao_llm.json`](item5_exemplo_extracao_llm.json).

2. **Escala via regras determinísticas (quantitativa):** para processar a base inteira (118.338 produtos) sem depender de limites de API de terceiros, foi construído um extrator baseado em regras e dicionários de palavras-chave — reconhecimento de marcas conhecidas, termos de conectividade (bluetooth, wifi, usb, com fio), cores mencionadas e público-alvo — aplicado a 100% do catálogo.

Essa combinação reflete uma decisão real de engenharia: usar IA generativa para validar a qualidade e o formato da extração em uma amostra controlada, e usar um método determinístico, gratuito e instantâneo para aplicar a mesma lógica em escala total, quando o custo/tempo de chamar uma API de LLM para 118 mil registros se torna proibitivo em um ambiente de teste sem orçamento.

## Resultado da extração em escala (118.338 produtos)

| Campo | Cobertura |
|---|---|
| Marca identificada | 32.990 produtos (27,9%) |
| Cor identificada | 41.567 produtos (35,1%) |
| Conectividade | 100% (categorizado, incluindo "não aplicável" quando não identificado) |
| Público-alvo | 100% (categorizado) |

Distribuição de conectividade identificada:
- USB: 14.779
- Bluetooth: 9.536
- Com fio: 6.700
- WiFi: 5.737
- Não identificado/não aplicável: 81.586

Distribuição de público-alvo:
- Geral: 103.311
- Profissional/Gamer: 6.572
- Infantil: 4.342
- Esportivo: 4.113

O arquivo completo com os 118.338 produtos processados está disponível em [`item5_features_extraidas_regras.csv`](item5_features_extraidas_regras.csv).

## Prompt utilizado na validação via LLM

```
Você é um especialista em catalogação de produtos de e-commerce.
Analise o título de produto abaixo e extraia as informações em formato JSON.

Título: "{title}"
Categoria conhecida: "{category}"

Extraia estes campos (use null se não conseguir identificar):
- marca: marca do produto
- modelo: modelo/linha do produto
- conectividade: "com fio", "bluetooth", "wifi", "usb", "não aplicável"
- cor: cor mencionada
- publico_alvo: "geral", "infantil", "esportivo", "profissional/gamer"
- caracteristicas_chave: lista com até 3 características técnicas principais mencionadas

Responda APENAS com o JSON, sem texto adicional.
```

## Limitações e próximos passos

O método de regras é mais simples que um LLM (não interpreta contexto, sinônimos ou combinações complexas de palavras), por isso a cobertura de marca (27,9%) é mais conservadora do que a que um LLM alcançaria. Em um ambiente de produção com orçamento para chamadas de API em escala (ex: via Batches API, que processa grandes volumes com desconto), o ideal seria aplicar o LLM à base completa, mantendo as regras apenas como fallback para os casos em que a IA não retornar resposta.
