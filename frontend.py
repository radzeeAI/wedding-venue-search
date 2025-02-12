import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Configuration de la page
st.set_page_config(page_title="Mariage Finder", layout="wide")

# CSS pour un design moderne et épuré
def load_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #F5F5F7;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        }
        .stButton > button {
            background-color: #9b51e0;
            color: white;
            border-radius: 8px;
            font-size: 16px;
            padding: 10px;
        }
        .stTextInput, .stNumberInput, .stMultiselect, .stSelectbox {
            border-radius: 10px;
            padding: 10px;
        }
        .result-card {
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Charger le CSS
load_css()

# --- En-tête principal ---
st.image("https://via.placeholder.com/150", width=120)
st.title("Trouvez votre lieu de mariage idéal")
st.subheader("Recherchez selon votre ville, rayon et critères spécifiques")

# --- Barre latérale pour les filtres ---
st.sidebar.header("Filtres de recherche")
ville = st.sidebar.text_input("Ville", placeholder="Ex: Paris, Lyon...")
rayon = st.sidebar.slider("Rayon de recherche (km)", 5, 100, 20)
mots_cles = st.sidebar.text_input("Mots-clés", placeholder="Ex: salle de réception, château, jardin")
prix_max = st.sidebar.number_input("Budget maximum (€)", min_value=1000, step=500, value=5000)
capacite = st.sidebar.number_input("Capacité minimale", min_value=10, step=10, value=50)

# Bouton de recherche
if st.sidebar.button("Rechercher"):
    query_params = {"ville": ville, "rayon": rayon, "mots_cles": mots_cles, "prix_max": prix_max, "capacite": capacite}
    try:
        response = requests.get("http://127.0.0.1:8000/venues", params=query_params)
        if response.status_code == 200:
            lieux = response.json()
        else:
            st.error("Erreur lors de la récupération des données.")
            lieux = []
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        lieux = []

    # --- Affichage des résultats ---
    if lieux:
        st.write("### Résultats trouvés")
        
        # Liste détaillée
        for lieu in lieux:
            st.markdown(f"""
            <div class='result-card'>
                <h3>{lieu.get('name', 'Nom du lieu')}</h3>
                <p><strong>Adresse :</strong> {lieu.get('address', 'Non renseigné')}</p>
                <p><strong>Capacité :</strong> {lieu.get('capacity', 'Non spécifié')} personnes</p>
                <p><strong>Prix :</strong> {lieu.get('price', 'Non spécifié')} €</p>
                <p><strong>Site web :</strong> <a href='{lieu.get('website', '#')}' target='_blank'>{lieu.get('website', 'Non disponible')}</a></p>
                <p><strong>Contact :</strong> {lieu.get('phone', 'Non disponible')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Carte interactive
        st.write("### Carte interactive")
        map_center = [48.8566, 2.3522]
        folium_map = folium.Map(location=map_center, zoom_start=12)
        for lieu in lieux:
            lat = lieu.get("latitude", 48.8566)
            lon = lieu.get("longitude", 2.3522)
            popup_text = lieu.get("name", "Lieu inconnu")
            folium.Marker(location=[lat, lon], popup=popup_text).add_to(folium_map)
        st_folium(folium_map, width=800, height=500)
    else:
        st.info("Aucun résultat trouvé. Essayez d'affiner votre recherche.")