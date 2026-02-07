# Projeto-dados-Imersao-python-alura-2026
# 📊 Análise Salarial na Área de Tecnologia

Este projeto tem como objetivo analisar padrões salariais na área de tecnologia a partir de dados públicos, buscando responder principalmente **quais fatores mais influenciam o salário**.

O foco da análise não é prever salários, mas **entender tendências globais** considerando:
- cargo
- senioridade
- modelo de trabalho
- localização da empresa

Os resultados são apresentados em um **dashboard interativo** desenvolvido com Streamlit.

---

## 🔍 Perguntas que a análise busca responder

- Existe uma diferença salarial relevante entre modelos de trabalho (remoto, híbrido, presencial)?
- A senioridade impacta mais o salário do que o cargo em si?
- O país da empresa influencia significativamente o salário médio?
- Quais cargos são mais frequentes e quais apresentam melhores médias salariais?

---

## 📈 Principais insights

- O **modelo de trabalho**, isoladamente, não apresenta grandes diferenças salariais.
- A **senioridade** impacta fortemente o salário, com crescimento consistente conforme o nível.
- A **localização da empresa** é um dos fatores mais relevantes:
  - Países da América do Norte concentram as maiores médias salariais.
  - Diferenças regionais superam, em muitos casos, a variação entre cargos.
- Alguns cargos menos frequentes apresentam **médias salariais mais altas**, indicando que recorrência não implica maior remuneração.

> A análise sugere que fatores macroeconômicos e regionais têm peso maior que o cargo isolado.

---

## 🛠️ Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- Plotly
- ISO country codes (ISO-2 → ISO-3 para visualização geográfica)

---

🔗 Acesse o dashboard online: [Meu Projeto no Streamlit](https://projeto-dados-imersao-python-alura-2026-etwxr9zziqu4rufj2yxn9z.streamlit.app/)

---

## ▶️ Como executar o projeto localmente

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate
```
3. Instale as dependências:
```bash
Instale as dependências
```
4.Execute o aplicativo:
```bash
streamlit run app.py
```
