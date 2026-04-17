import streamlit as st
import time
from agents import TextualAgent, MathAgent, BiblioAgent
from agent_orchestrateur import MasterAgent
from rag_tool import RAGDocumentTool

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="IA-Master: ML & Stats Assistant",
    page_icon="🤖",
    layout="wide"
)

# Style CSS personnalisé pour une interface "stylée"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatMessage { border-radius: 15px; border: 1px solid #ddd; margin-bottom: 10px; }
    .source-tag { 
        font-size: 0.8em; color: #007bff; background: #e7f3ff; 
        padding: 2px 8px; border-radius: 10px; font-weight: bold;
    }
    .formula-zone {
        background-color: #1e1e1e; color: #ffffff; padding: 20px;
        border-radius: 10px; border-left: 5px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DU SYSTÈME (SESSION STATE) ---
if "master" not in st.session_state:
    with st.spinner("🛠️ Initialisation du cerveau IA et des index FAISS..."):
        # 1. L'outil (chargé une seule fois)
        rag = RAGDocumentTool(docs_dir="data/") 
        
        # 2. Les agents spécialisés
        txt_agent = TextualAgent(rag)
        math_agent = MathAgent(rag)
        bib_agent = BiblioAgent()
        
        # 3. Le Maître
        st.session_state.master = MasterAgent(txt_agent, math_agent, bib_agent)
        st.session_state.chat_history = []

# --- LAYOUT : COLONNE GAUCHE (CHAT) / COLONNE DROITE (LABO MATHS) ---
col_chat, col_lab = st.columns([0.6, 0.4], gap="large")

with col_chat:
    st.title("🤖 Master IA Assistant")
    st.caption("Expert en Machine Learning & Statistiques (Corpus Anglais)")

    # Zone d'affichage des messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Zone d'invite claire et spacieuse
    if query := st.chat_input("Posez votre question sur le ML ou les Stats..."):
        # Affichage immédiat du message utilisateur
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)

        # Réponse du Master Agent
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("🔍 *Le Maître consulte les experts...*")
            
            response = st.session_state.master.process_request(query)
            
            placeholder.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

with col_lab:
    st.subheader("🧮 Laboratoire de Formules")
    st.info("Cette zone s'active pour visualiser les paramètres des modèles détectés.")

    # EXEMPLE INTERACTIF : Régression Linéaire
    # (On pourrait automatiser cela en fonction de la détection de l'Agent Math)
    with st.expander("Simulateur : Régression Linéaire (y = wx + b)", expanded=True):
        st.latex(r"f(x) = w \cdot x + b")
        
        # Sliders pour jongler avec les paramètres
        w = st.slider("Poids (Weight - w)", -10.0, 10.0, 2.0)
        b = st.slider("Biais (Bias - b)", -20.0, 20.0, 5.0)
        x_val = st.number_input("Entrée (x)", value=10.0)
        
        y_val = w * x_val + b
        
        st.markdown(f"""
        <div class="formula-zone">
            <strong>Résultat du calcul :</strong><br>
            Prediction (y) = {y_val:.2f}
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**Description des variables :**")
        st.write("- **w** : La pente de la droite (importance de l'entrée).")
        st.write("- **b** : L'ordonnée à l'origine (valeur si x=0).")
        st.write("- **x** : Ta donnée d'entrée (Feature).")

# --- FOOTER ---
st.divider()
st.caption("Projet Generative AI - Multi-Agent System avec RAG & FAISS.")
