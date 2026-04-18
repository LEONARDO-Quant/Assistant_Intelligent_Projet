import streamlit as st
from agent_Master import MasterAgent
from rag_tool import theory_engine, stats_engine
from schema_tool import SchemaTool

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="IA Multi-Agents Pro", layout="wide")

# --- STYLE CSS (DARK MODE & DESIGN) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    /* Style pour la colonne latérale ou les onglets */
    [data-testid="stSidebar"] {
        background-color: #161B22;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DES AGENTS ET DE LA MÉMOIRE ---
if "master_agent" not in st.session_state:
    # On initialise l'agent une seule fois
    st.session_state.master_agent = MasterAgent(theory_engine, stats_engine)
    st.session_state.messages = []
    st.session_state.schemas = []  # Pour la page 2

# Instance de l'outil de rendu
schema_tool = SchemaTool()

# --- NAVIGATION ---
page = st.sidebar.selectbox("Navigation", ["💬 Chat Principal", "🧠 Laboratoire de Schémas"])

# ---------------------------------------------------------
# PAGE 1 : CHAT PRINCIPAL
# ---------------------------------------------------------
if page == "💬 Chat Principal":
    st.title("🤖 Assistant Intelligent Multi-Agents")
    st.caption("Expert en Théorie, Stats, Web et Visualisation")

    # Affichage de l'historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrée utilisateur
    if prompt := st.chat_input("Posez votre question ici..."):
        # Afficher le message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Appel à l'Agent Master
        with st.chat_message("assistant"):
            with st.spinner("L'IA réfléchit..."):
                # On passe l'historique pour le contexte
                response = st.session_state.master_agent.answer(
                    prompt, 
                    history=st.session_state.messages
                )
                
                # Récupération du schéma s'il y en a un nouveau
                if st.session_state.master_agent.current_schema:
                    new_schema = st.session_state.master_agent.current_schema
                    if new_schema not in st.session_state.schemas:
                        st.session_state.schemas.append(new_schema)
                    st.info("💡 Un nouveau schéma a été généré dans le Laboratoire !")

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------------------------------------------
# PAGE 2 : LABORATOIRE DE SCHÉMAS
# ---------------------------------------------------------
elif page == "🧠 Laboratoire de Schémas":
    st.title("Visualisation Graphique")
    st.write("Retrouvez ici tous les schémas, mindmaps et graphiques générés durant la session.")

    if not st.session_state.schemas:
        st.info("Aucun schéma n'a encore été généré. Demandez un schéma ou une carte mentale dans le chat !")
    else:
        # On affiche les schémas du plus récent au plus ancien
        for i, sc in enumerate(reversed(st.session_state.schemas)):
            with st.expander(f"Schéma #{len(st.session_state.schemas) - i}", expanded=True):
                schema_tool.render(sc)
                st.code(sc, language="mermaid") # Optionnel : afficher le code source en dessous