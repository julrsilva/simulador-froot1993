
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Gestão de Risco - Froot (1993)", layout="centered")

st.title("🎯 Simulador de Gestão de Risco Corporativo")
st.subheader("Baseado em Froot, Scharfstein e Stein (1993)")

st.markdown("""
Este simulador ilustra como a **gestão de risco** (uso de hedge) pode preservar ou aumentar o valor da empresa 
quando o **fluxo de caixa interno é volátil** e o **financiamento externo é custoso**.

A função de retorno do investimento é **côncava** e segue a forma: \( R(I) = a \cdot I - b \cdot I^2 \)
""")

# Entradas do usuário
investimento = st.slider("Investimento pretendido (I)", 50, 200, 100)
a = st.slider("Parâmetro a (retorno marginal inicial)", 0.5, 5.0, 2.0)
b = st.slider("Parâmetro b (retornos decrescentes)", 0.001, 0.05, 0.01)
r_base = st.slider("Custo base do capital externo (%)", 0.0, 0.3, 0.10, step=0.01)
lambda_sens = st.slider("Sensibilidade do custo ao financiamento externo (λ)", 0.0, 0.01, 0.002, step=0.0005)
custo_hedge_pct = st.slider("Custo do hedge (% do investimento)", 0.0, 0.05, 0.01)

# Fluxos de caixa simulados
cf_vals = np.array([100, 80, 60, 40, 20])
npv_sem_hedge = []
npv_com_hedge = []

# Função de retorno
def retorno(I):
    return a * I - b * I**2

for cf in cf_vals:
    f1 = max(0, investimento - cf)
    r1 = r_base + lambda_sens * f1
    custo1 = cf + f1 * (1 + r1)
    npv1 = retorno(investimento) - custo1
    npv_sem_hedge.append(npv1)

    # Com hedge, assume menor necessidade de financiamento externo
    f2 = max(0, investimento - cf * 1.1)
    r2 = r_base + lambda_sens * f2
    custo2 = cf + f2 * (1 + r2) + custo_hedge_pct * investimento
    npv2 = retorno(investimento) - custo2
    npv_com_hedge.append(npv2)

# Mostrar gráfico
st.subheader("📈 Resultado: NPV com e sem Hedge")
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(cf_vals, npv_sem_hedge, marker='o', label='Sem Hedge')
ax.plot(cf_vals, npv_com_hedge, marker='s', label='Com Hedge')
ax.set_xlabel("Fluxo de Caixa Interno")
ax.set_ylabel("NPV")
ax.set_title("Valor do Projeto em Diferentes Níveis de Fluxo de Caixa")
ax.legend()
ax.grid(True)
ax.invert_xaxis()
st.pyplot(fig)

# Mostrar tabela
df_result = pd.DataFrame({
    "Fluxo de Caixa Interno": cf_vals,
    "NPV sem Hedge": npv_sem_hedge,
    "NPV com Hedge": npv_com_hedge
})
st.dataframe(df_result, use_container_width=True)
