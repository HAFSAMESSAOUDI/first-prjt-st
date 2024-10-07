import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Simulation de la diffusion avec réactions chimiques")

# Sélection de l'ordre de la réaction
reaction_order = st.selectbox(
    'Choisissez l\'ordre de la réaction chimique',
    ('Ordre 1', 'Pseudo-premier ordre', 'Ordre 2', 'Ordre 3')
)

# Entrée des paramètres généraux
C_A_i = st.number_input('Concentration initiale C_A^i', value=1.0)
C_A_L = st.number_input('Concentration limite C_A^L', value=0.2)
D_A = st.number_input('Coefficient de diffusion D_A', value=0.1)
delta = st.number_input('Épaisseur delta', value=1.0)

# Entrée des paramètres spécifiques selon l'ordre de réaction
if reaction_order in ['Ordre 1', 'Pseudo-premier ordre']:
    k1 = st.number_input('Constante de réaction k1', value=0.5)

elif reaction_order == 'Ordre 2':
    k2 = st.number_input('Constante de réaction k2', value=0.5)

elif reaction_order == 'Ordre 3':
    k3 = st.number_input('Constante de réaction k3', value=0.5)

# Création des données et calcul des profils de concentration
x = np.linspace(0, delta, 100)

if reaction_order == 'Ordre 1':
    # Equation pour réaction d'ordre 1
    lambda_ = np.sqrt(k1 / D_A)
    C_A = C_A_i * np.cosh(lambda_ * x) + (C_A_L - C_A_i * np.cosh(lambda_ * delta)) / np.sinh(lambda_ * delta) * np.sinh(lambda_ * x)

elif reaction_order == 'Pseudo-premier ordre':
    # Equation pour pseudo-premier ordre
    lambda_ = np.sqrt(k1 * C_A_i / D_A)
    C_A = C_A_i * np.cosh(lambda_ * x) + (C_A_L - C_A_i * np.cosh(lambda_ * delta)) / np.sinh(lambda_ * delta) * np.sinh(lambda_ * x)

elif reaction_order == 'Ordre 2':
    # Equation pour réaction d'ordre 2
    C_A = 1 / ((np.sqrt(2 * k2 / D_A) * x + 2 / np.sqrt(C_A_i)) ** 2)

elif reaction_order == 'Ordre 3':
    # Equation pour réaction d'ordre 3
    C_A = 1 / (-np.sqrt(2 * k3 / D_A) * x + 1 / C_A_i)

# Tracé du profil de concentration
fig, ax = plt.subplots()
ax.plot(x, C_A, label=f"Concentration {reaction_order}")
ax.set_xlabel("Distance x")
ax.set_ylabel("Concentration C_A")
ax.set_title(f"Profil de concentration pour une {reaction_order}")
ax.legend()

# Affichage du graphique dans Streamlit
st.pyplot(fig)

# Ajout d'une fonctionnalité de comparaison
compare = st.checkbox("Comparer avec d'autres ordres de réaction")

if compare:
    # Tracé des différents ordres sur un même graphique pour comparaison
    fig_compare, ax_compare = plt.subplots()

    # Ordre 1
    lambda_1 = np.sqrt(0.5 / D_A)
    C_A1 = C_A_i * np.cosh(lambda_1 * x) + (C_A_L - C_A_i * np.cosh(lambda_1 * delta)) / np.sinh(lambda_1 * delta) * np.sinh(lambda_1 * x)
    ax_compare.plot(x, C_A1, label="Ordre 1")

    # Pseudo-premier ordre
    lambda_pseudo = np.sqrt(0.5 * C_A_i / D_A)
    C_A_pseudo = C_A_i * np.cosh(lambda_pseudo * x) + (C_A_L - C_A_i * np.cosh(lambda_pseudo * delta)) / np.sinh(lambda_pseudo * delta) * np.sinh(lambda_pseudo * x)
    ax_compare.plot(x, C_A_pseudo, label="Pseudo-premier ordre")

    # Ordre 2
    C_A2 = 1 / ((np.sqrt(2 * 0.5 / D_A) * x + 2 / np.sqrt(C_A_i)) ** 2)
    ax_compare.plot(x, C_A2, label="Ordre 2")

    # Ordre 3
    C_A3 = 1 / (-np.sqrt(2 * 0.5 / D_A) * x + 1 / C_A_i)
    ax_compare.plot(x, C_A3, label="Ordre 3")

    ax_compare.set_xlabel("Distance x")
    ax_compare.set_ylabel("Concentration C_A")
    ax_compare.set_title("Comparaison des profils de concentration")
    ax_compare.legend()

    st.pyplot(fig_compare)
