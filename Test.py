import streamlit as st

# Configurer la page avec le thème Streamlit
st.set_page_config(
    page_title="Répartition vin",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="🍷"
)

# Personnalisation du thème via le code directement (optionnel, mais plus simple)
st.markdown("""
    <style>
    /* Personnalisation du curseur (slider) via le thème */
    .stSlider > div > div > div {
        background-color: #ffffff;  /* Ligne du curseur en blanc */
    }

    .stSlider > div > div > input {
        background: transparent;  /* Rendre la barre transparente pour appliquer la couleur de la ligne */
    }
    </style>
""", unsafe_allow_html=True)

# Afficher l'image centrée
st.image("logo.webp", width=300, use_container_width=True)

# Formulaire pour le nombre total de litres
with st.form(key='repartition_form'):

    total_litres = st.number_input(
        "Nombre de litres de vin produits par an", min_value=0, value=10000, step=100
    )

    zone = st.selectbox(
        "Zone géographique de production",
        ["Région - Nord", "Région - Sud", "Région - Est", "Région - Ouest", "Autre / Préciser"]
    )
    if zone == "Autre / Préciser":
        zone = st.text_input("Précisez la zone géographique")

    # Proportions
    proportion_blanc = st.slider("Part du vin blanc dans la production (%)", 0, 100, 30)
    proportion_rouge = st.slider("Part du vin rouge dans la production (%)", 0, 100, 60)
    proportion_rose = st.slider("Part du vin rosé dans la production", 0, 100, 10)

    submit = st.form_submit_button("Calculer avec la solution W-platform")  # Bouton de soumission pour ce formulaire

# Calculs après soumission
if submit:

    somme_pct = proportion_blanc + proportion_rouge + proportion_rose
    if somme_pct > 100:
        st.warning("Erreur la proportion dépasse")
        factor = 100.0 / somme_pct
        proportion_blanc = round(proportion_blanc * factor, 2)
        proportion_rouge = round(proportion_rouge * factor, 2)
        proportion_rose = round(proportion_rose * factor, 2)

    litres_blanc = round(total_litres * (proportion_blanc / 100), 2)
    litres_rouge = round(total_litres * (proportion_rouge / 100), 2)
    litres_rose = round(total_litres * (proportion_rose / 100), 2)

    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        # Création des données
        df = pd.DataFrame({
            'Catégorie': ['Blanc', 'Rouge', 'Rosé'],
            'Litres': [litres_blanc, litres_rouge, litres_rose]
        })

        # Définir des teintes de vert plus claires
        couleurs = ['#007f3e', '#00974d', '#00b35c']

        # Créer le graphique plus petit
        fig, ax = plt.subplots(figsize=(3, 3))  # Taille réduite (5x5 pouces)
        ax.pie(df['Litres'], labels=df['Catégorie'], autopct='%1.1f%%', colors=couleurs)

        # Titre du graphique
        ax.set_title('Répartition de votre production')

        # Afficher le graphique
        st.pyplot(fig)



    except:
        st.info("Graphique indisponible — installez pandas et matplotlib.")
