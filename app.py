import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from main import c_ox, current, F

st.set_page_config(page_title="Cronoamperometría Esférica", layout="wide")

st.title("Cronoamperometría en Electrodo Esférico")

# --- Parámetros de entrada ---
st.sidebar.header("Parámetros")
c_ox_star = st.sidebar.number_input("c*Ox [mol/m³]", value=1.0)
D_ox = st.sidebar.number_input("D_Ox [m²/s]", value=1e-9, format="%.1e")
r0 = st.sidebar.number_input("Radio del electrodo r₀ [m]", value=1e-4, format="%.1e")
A = st.sidebar.number_input("Área del electrodo [m²]", value=4 * np.pi * r0**2, format="%.2e")
E0 = st.sidebar.number_input("E⁰' [V]", value=0.0)
E = st.sidebar.slider("Potencial aplicado E [V]", min_value=-1.0, max_value=1.0, value=0.1)
n = st.sidebar.number_input("Número de electrones (n)", value=1, step=1)

# --- Tiempo y distancia ---
t_vals = np.logspace(-3, 1, 200)  # Tiempo de 1 ms a 10 s
r_vals = np.linspace(r0, 5*r0, 200)

# --- Gráfico de concentración vs radio ---
st.subheader("Perfil de concentración c_Ox(r, t)")

t_plot = st.slider("Selecciona un tiempo para el perfil de concentración [s]", float(t_vals[0]), float(t_vals[-1]), 1.0, step=0.1)
c_vals = c_ox(r_vals, t_plot, E, c_ox_star, D_ox, r0, E0)

fig1, ax1 = plt.subplots()
ax1.plot(r_vals * 1e6, c_vals)
ax1.set_xlabel("r (μm)")
ax1.set_ylabel("c_Ox (mol/m³)")
ax1.set_title(f"Perfil de concentración en t = {t_plot:.2f} s")
ax1.grid()
st.pyplot(fig1)

# --- Gráfico de corriente vs tiempo ---
st.subheader("Corriente vs tiempo I(t)")

I_vals = [current(E, t, n, F, A, c_ox_star, D_ox, r0, E0) for t in t_vals]

fig2, ax2 = plt.subplots()
ax2.plot(t_vals, I_vals)
ax2.set_xscale("log")
ax2.set_xlabel("Tiempo (s)")
ax2.set_ylabel("Corriente (A)")
ax2.set_title("Corriente vs Tiempo")
ax2.grid()
st.pyplot(fig2)
