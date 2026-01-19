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
n_frames = st.sidebar.slider("Número de frames (perfil concentración)", min_value=10, max_value=200, value=100)

# --- Tiempo y distancia ---
t_highres = np.arange(0.01, t_max + 0.01, 0.01)  # Resolución fija para j(t)
t_frames = np.linspace(0.01, t_max, n_frames)    # Frames para animación
r_vals = np.linspace(r0, 5 * r0, 200)

# --- Contenedor para los gráficos ---
col1, col2 = st.columns(2)
placeholder1 = col1.empty()
placeholder2 = col2.empty()

# --- Sesión de estado para guardar resultados después de animación ---
if "done_anim" not in st.session_state:
    st.session_state.done_anim = False
if "c_profiles" not in st.session_state:
    st.session_state.c_profiles = None
if "j_vals" not in st.session_state:
    st.session_state.j_vals = None

# --- Botón para ejecutar animación ---
if st.button("▶ Reproducir animación"):
    st.session_state.done_anim = False
    st.session_state.c_profiles = []
    st.session_state.j_vals = [current_density(E, t, c_ox_star, D_ox, r0, E0) for t in t_highres]

    for t in t_frames:
        # Perfil de concentración
        c_vals = c_ox(r_vals, t, E, c_ox_star, D_ox, r0, E0)
        st.session_state.c_profiles.append(c_vals)

        fig1, ax1 = plt.subplots()
        ax1.plot(r_vals * 1e6, c_vals)
        ax1.set_xlabel("r (μm)")
        ax1.set_ylabel("c_Ox (mol/m³)")
        ax1.set_title(f"Perfil de concentración (t = {t:.2f} s)")
        ax1.grid()
        placeholder1.pyplot(fig1)

        # Densidad de corriente
        fig2, ax2 = plt.subplots()
        ax2.plot(t_highres, st.session_state.j_vals, label="j(t)")
        ax2.axvline(t, color='red', linestyle='--', label=f"t = {t:.2f} s")
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel("Densidad de corriente (A/m²)")
        ax2.set_title("Densidad de corriente vs tiempo")
        ax2.legend()
        ax2.grid()
        placeholder2.pyplot(fig2)

        time.sleep(0.05)

    st.session_state.done_anim = True

# --- Revisión manual post-animación ---
if st.session_state.done_anim and st.session_state.c_profiles is not None:
    st.subheader("🔍 Revisión manual del perfil de concentración")
    t_idx = st.slider("Selecciona un tiempo (post-animación)", 0, len(t_frames)-1, len(t_frames)//2)
    t_selected = t_frames[t_idx]
    c_vals = st.session_state.c_profiles[t_idx]

    # Perfil de concentración
    fig1, ax1 = plt.subplots()
    ax1.plot(r_vals * 1e6, c_vals)
    ax1.set_xlabel("r (μm)")
    ax1.set_ylabel("c_Ox (mol/m³)")
    ax1.set_title(f"Perfil de concentración (t = {t_selected:.2f} s)")
    ax1.grid()
    placeholder1.pyplot(fig1)

    # Densidad de corriente con línea vertical
    fig2, ax2 = plt.subplots()
    ax2.plot(t_highres, st.session_state.j_vals, label="j(t)")
    ax2.axvline(t_selected, color='red', linestyle='--', label=f"t = {t_selected:.2f} s")
    ax2.set_xlabel("Tiempo (s)")
    ax2.set_ylabel("Densidad de corriente (A/m²)")
    ax2.set_title("Densidad de corriente vs tiempo")
    ax2.legend()
    ax2.grid()
    placeholder2.pyplot(fig2)
