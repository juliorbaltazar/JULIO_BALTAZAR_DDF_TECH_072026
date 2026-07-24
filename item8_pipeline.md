# Item 8 — Pipeline de Dados

## Nota sobre limitação de ambiente

O ambiente de treinamento disponibilizado para este case não possui acesso liberado ao Módulo de Inteligência da Dadosfera (aparece bloqueado 🔒 no menu lateral, junto com outros módulos premium como Transformação, Linhagem e Incorporar Ativos). Isso impossibilitou a construção do pipeline diretamente na interface visual da plataforma.

Como alternativa, o pipeline foi construído em Python, replicando fielmente o conceito de **Steps conectados** utilizado pelo Módulo de Inteligência da Dadosfera: cada etapa é uma função isolada, que recebe o resultado da etapa anterior e passa adiante o seu próprio resultado, formando uma cadeia de processamento — exatamente o modelo descrito na documentação oficial (*"um Pipeline pode ser construído conectando múltiplos passos, que determina a ordem de execução e estão conectados de forma a continuar trabalhando em dados resultantes"*).

## Desenho do pipeline

```
[Step 1: Extração]  →  [Step 2: Qualidade]  →  [Step 3: Modelagem]  →  [Step 4: Carga]
   (dados brutos)        (aplica regras           (gera fato +           (salva CSVs
                          do Item 4)                dimensões,             finais prontos
                                                     Item 6)                para consumo)
```

Cada Step corresponde a um item já desenvolvido anteriormente no case, agora encadeado e automatizado.

## Código (Google Colab)

```python
import pandas as pd
import numpy as np

# ==========================================================
# STEP 1: Extração — carrega os dados brutos
# ==========================================================
def step1_extracao(caminho_csv):
    print("[Step 1] Extraindo dados brutos...")
    df = pd.read_csv(caminho_csv)
    print(f"[Step 1] {len(df)} registros carregados.")
    return df


# ==========================================================
# STEP 2: Qualidade — aplica as regras definidas no Item 4
# ==========================================================
def step2_qualidade(df):
    print("[Step 2] Aplicando regras de qualidade...")
    df = df.copy()

    # Regra 1: flag de preço indisponível
    df['preco_indisponivel'] = df['price'] == 0

    # Regra 2: avaliação zero vira nulo (não é uma nota real)
    df['avaliacao_tratada'] = df['stars'].replace(0, np.nan)

    # Regra 3: remove os poucos títulos anormalmente curtos
    antes = len(df)
    df = df[df['title'].str.len() >= 5]
    removidos = antes - len(df)

    print(f"[Step 2] {df['preco_indisponivel'].sum()} produtos marcados sem preço.")
    print(f"[Step 2] {df['avaliacao_tratada'].isna().sum()} produtos sem avaliação (tratados como nulo).")
    print(f"[Step 2] {removidos} registros com título inválido removidos.")
    return df


# ==========================================================
# STEP 3: Modelagem — gera fato e dimensões (Item 6)
# ==========================================================
def step3_modelagem(df):
    print("[Step 3] Gerando modelo dimensional...")

    dim_categoria = df[['category_id', 'category_name']].drop_duplicates().reset_index(drop=True)
    dim_categoria.columns = ['id_categoria', 'nome_categoria']

    dim_produto = df[['asin', 'title', 'imgUrl', 'productURL']].drop_duplicates().reset_index(drop=True)
    dim_produto.columns = ['asin', 'titulo', 'link_imagem', 'link_produto']

    fato_produtos = df[['asin', 'category_id', 'price', 'listPrice',
                         'avaliacao_tratada', 'reviews', 'boughtInLastMonth',
                         'isBestSeller', 'preco_indisponivel']].copy()
    fato_produtos.columns = ['asin', 'id_categoria', 'preco', 'preco_tabela',
                              'avaliacao_media', 'numero_avaliacoes', 'comprado_ultimo_mes',
                              'eh_mais_vendido', 'preco_indisponivel']

    print(f"[Step 3] {len(dim_categoria)} categorias, {len(dim_produto)} produtos, {len(fato_produtos)} linhas na fato.")
    return dim_categoria, dim_produto, fato_produtos


# ==========================================================
# STEP 4: Carga — salva os resultados finais
# ==========================================================
def step4_carga(dim_categoria, dim_produto, fato_produtos, pasta_saida='.'):
    print("[Step 4] Salvando resultados finais...")
    dim_categoria.to_csv(f'{pasta_saida}/dim_categoria_pipeline.csv', index=False)
    dim_produto.to_csv(f'{pasta_saida}/dim_produto_pipeline.csv', index=False)
    fato_produtos.to_csv(f'{pasta_saida}/fato_produtos_pipeline.csv', index=False)
    print("[Step 4] Pipeline concluído. Arquivos prontos para carga na Dadosfera.")


# ==========================================================
# EXECUÇÃO DO PIPELINE (conecta os 4 steps em sequência)
# ==========================================================
def executar_pipeline(caminho_csv_bruto):
    df_bruto = step1_extracao(caminho_csv_bruto)
    df_tratado = step2_qualidade(df_bruto)
    dim_categoria, dim_produto, fato_produtos = step3_modelagem(df_tratado)
    step4_carga(dim_categoria, dim_produto, fato_produtos)
    return dim_categoria, dim_produto, fato_produtos


# Executa o pipeline completo
dim_categoria, dim_produto, fato_produtos = executar_pipeline('produtos_hardware_eletronicos.csv')
```

## Resultado da execução

Output real da execução do pipeline no Google Colab:

```
[Step 1] Extraindo dados brutos...
[Step 1] 118338 registros carregados.
[Step 2] Aplicando regras de qualidade...
[Step 2] 4361 produtos marcados sem preço.
[Step 2] 16593 produtos sem avaliação (tratados como nulo).
[Step 2] 5 registros com título inválido removidos.
[Step 3] Gerando modelo dimensional...
[Step 3] 19 categorias, 118333 produtos, 118333 linhas na fato.
[Step 4] Salvando resultados finais...
[Step 4] Pipeline concluído. Arquivos prontos para carga na Dadosfera.
```

O notebook completo, com o código e a saída de execução, está disponível neste repositório: [`item8_pipeline.ipynb`](item8_pipeline.ipynb).

## Arquivos gerados pelo pipeline

Os 3 arquivos finais produzidos pelo Step 4 (Carga) também estão disponíveis neste repositório como evidência do resultado:

- [`dim_categoria_pipeline.csv`](dim_categoria_pipeline.csv) — 19 categorias
- [`dim_produto_pipeline.csv`](dim_produto_pipeline.csv) — 118.333 produtos
- [`fato_produtos_pipeline.csv`](fato_produtos_pipeline.csv) — 118.333 linhas de métricas, já com as flags de qualidade aplicadas (`preco_indisponivel`, `avaliacao_tratada`)

## Vantagem desse desenho

Cada Step é independente e testável isoladamente (pode-se rodar só o Step 2 para validar uma regra de qualidade nova, sem precisar re-executar a extração), e a saída de um Step alimenta diretamente o próximo — o mesmo princípio de encadeamento de um pipeline visual na Dadosfera. Se o Módulo de Inteligência estivesse disponível, cada uma dessas 4 funções se tornaria um Step separado no editor visual, conectados na mesma ordem.

## Catalogação do pipeline (adaptado)

Como não foi possível catalogar um pipeline nativo da Dadosfera, este documento markdown, junto ao notebook do Colab (`item8_pipeline.ipynb`), serve como a documentação e "catálogo" do pipeline desenvolvido — descrevendo entradas, transformações e saídas de cada etapa, seguindo o mesmo padrão de documentação aplicado aos demais ativos do case (Item 3).
