import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from main import c_ox, current_density

st.set_page_config(page_title="Cronoamperometría Esférica", layout="wide")
st.title("Cronoamperometría en Electrodo Esférico")

# --- Parámetros de entrada ---
st.sidebar.header("Parámetros del sistema")
c_ox_star = st.sidebar.number_input("c*Ox [mol/m³]", value=1.0)
D_ox = st.sidebar.number_input("D_Ox [m²/s]", value=1e-9, format="%.1e")
r0 = st.sidebar.number_input("Radio del electrodo r₀ [m]", value=1e-4, format="%.1e")
E0 = st.sidebar.number_input("E⁰' [V]", value=0.0)
E = st.sidebar.slider("Potencial aplicado E [V]", min_value=-1.0, max_value=1.0, value=0.1)
t_max = st.sidebar.slider("Duración del experimento [s]", min_value=1.0, max_value=20.0, value=10.0, step=1.0)
n_frames = st.sidebar.slider("Número de frames", min_value=10, max_value=200, value=100)

# --- Tiempo y distancia ---
t_vals = np.linspace(0.01, t_max, n_frames)
r_vals = np.linspace(r0, 5 * r0, 200)

# --- Contenedor para los gráficos ---
col1, col2 = st.columns(2)
placeholder1 = col1.empty()
placeholder2 = col2.empty()

# --- Botón para ejecutar la animación ---
if st.button("▶ Reproducir animación"):
    j_vals = []

    for i, t in enumerate(t_vals):
        # Perfil de concentración
        c_vals = c_ox(r_vals, t, E, c_ox_star, D_ox, r0, E0)
        fig1, ax1 = plt.subplots()
        ax1.plot(r_vals * 1e6, c_vals)
        ax1.set_xlabel("r (μm)")
        ax1.set_ylabel("c_Ox (mol/m³)")
        ax1.set_title(f"Perfil de concentración (t = {t:.2f} s)")
        ax1.grid()
        placeholder1.pyplot(fig1)

        # Densidad de corriente acumulada
        j_vals.append(current_density(E, t, c_ox_star, D_ox, r0, E0))
        fig2, ax2 = plt.subplots()
        ax2.plot(t_vals[:i+1], j_vals)
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel("Densidad de corriente (A/m²)")
        ax2.set_title("Densidad de corriente vs tiempo")
        ax2.grid()
        placeholder2.pyplot(fig2)

        time.sleep(0.05)  # Control de velocidad de animación
