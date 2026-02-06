import pandas as pd
import streamlit as st
import plotly.express as px
import pycountry


#Config do Head da página
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide" 
)

#Carregamento de Dados
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

#aplicando iso3 para a localidade das empresas
def iso2_to_iso3(code):
        try:
            return pycountry.countries.get(alpha_2=code).alpha_3
        except AttributeError:
            return None
        
df["iso3_empresa"] = df["empresa"].apply(iso2_to_iso3)

#Criação da sideBar
st.sidebar.header('Filtros🔎') 

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# Filtragem do DataFrame
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

#conteúdo Principal
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ""


col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

# --- Análises Visuais com Plotly ---
st.subheader("Análise Sobre Modelo de Trabalho")

#Grafico sobre a Distribuição salarial dos modelos de trabalho
if not df_filtrado.empty:
        grafico_distr_modelTrabalho = px.box(
            df_filtrado,
            x='remoto',
            y='usd',
            title='Distribuição dos modelos de trabalho por salário',
            points='outliers',   
            labels={'remoto': 'Modelos de trabalho', 'usd': 'Distribuição Salarial'})
        st.plotly_chart(grafico_distr_modelTrabalho, use_container_width=True)  
else:
         st.warning('dados não existem')

#Grafico sobre a distribuição salarial dos modelos de trabalhos através da senioridade
if not df_filtrado.empty:

            grafico_media_x_senioridade = px.box(
                 df_filtrado,
                 x='remoto',
                 y='usd',
                 facet_col='senioridade',
                 hover_data=('senioridade', 'cargo', 'empresa'),
                 points='outliers',
                 title='Distribuição salarial por modelo de trabalho e senioridade')
            st.plotly_chart(grafico_media_x_senioridade, use_container_width=True)

            qtd_por_grupo = df_filtrado.groupby(
                ['remoto', 'senioridade']
            ).agg(
                qtd_modelo_trabalho=('usd', 'count'),
                mediana=('usd', 'median'),
                media=('usd', 'mean')
            ).reset_index()

            st.dataframe(qtd_por_grupo) 
else:
         st.warning('dados não existem')

st.subheader('Análise sobre Cargo e localidade')

#Grafico dos cargos mais frequentes, com mais registros
if not df_filtrado.empty:
        top_cargos = (df_filtrado['cargo'].value_counts().head(10).index)       
        df_top_cargo = df_filtrado[df_filtrado['cargo'].isin(top_cargos)]
        top_cargos_dados = df_top_cargo.groupby('cargo').agg(media=('usd','mean'), qtd_cargo=('usd', 'count')).reset_index()
        grafico_cargo = px.bar(
                top_cargos_dados,
                x='media',
                y='cargo',
                hover_data=['qtd_cargo'],
                labels={'media': 'Média Salarial'}, 
                title='Média salarial dos 10 cargos mais frequentes'
        )
        grafico_cargo.update_layout(title_x=0.2)
        st.plotly_chart(grafico_cargo, use_container_width=True)        

#Grafico mundial da variancia de media salarial do cargo de cientista de dados
if not df_filtrado.empty:
    top_cargos = (df_filtrado['cargo'].value_counts().head(10).index)       
    df_top_cargo = df_filtrado[df_filtrado['cargo'].isin(top_cargos)]
    media_ds_pais = df_top_cargo.groupby('iso3_empresa').agg(salario_mediana_paises = ('usd', 'median'), qtd_paises = ('usd', 'count')).reset_index()
    media_ds_pais = media_ds_pais[media_ds_pais['qtd_paises'] >= 20]
    grafico_paises = px.choropleth(media_ds_pais,
        locations='iso3_empresa',
        color='salario_mediana_paises',
        color_continuous_scale='blues',
        title='Salário médio dos 10 cargos mais frequentes nos paises',
        labels={'salario_mediana_paises': 'Salário médio (USD)', 'residencia_iso3': 'País', 'qtd_paises' : 'Quantidade de Registros'},
        hover_data=['qtd_paises'])
    grafico_paises.update_layout(title_x=0.2)
    st.plotly_chart(grafico_paises, use_container_width=True)       
else:
    st.warning("Nenhum dado para exibir no gráfico de países.")

st.markdown("""
### Conclusões da Análise Salarial

A análise dos dados indica que o modelo de trabalho (remoto ou presencial) não apresenta diferenças salariais relevantes no mercado de dados. As distribuições de salários são semelhantes entre os modelos, mesmo considerando diferenças no volume de registros.

A senioridade(experiencia) exerce influência direta no aumento salarial, com progressão consistente conforme o nível de experiência do profissional.

Entretanto, o fator que demonstra maior impacto sobre a variação salarial é a localização da empresa. Empresas situadas em países com mercados tecnológicos mais maduros apresentam salários médios significativamente mais elevados, independentemente do modelo de trabalho adotado.
            
Países da América do Norte apresentam médias salariais mais elevadas, especialmente devido à presença de valores extremos nos Estados Unidos. Esses salários muito altos ampliam a média, enquanto mercados como o europeu apresentam remunerações mais concentradas e estáveis, resultando em médias menores.
""")


# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
