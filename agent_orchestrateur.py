from rag_tool import RAGDocumentTool
from agent_textuel import TextualAgent
from agent_formules import MathAgent
from agent_biblio import BiblioAgent # Nouveau !

# Initialisation
shared_rag = RAGDocumentTool(docs_dir=r"C:\Users\...\Data")
tuteur_texte = TextualAgent(shared_rag)
expert_math = MathAgent(shared_rag)
bibliothécaire = BiblioAgent() # Lui n'a pas besoin du RAG, il a le Web !

def interroger_tout_le_monde(question):
    print(f"\n--- ANALYSE COMPLÈTE : {question} ---")
    
    # 1. Le cours (RAG)
    print("\n[CONTENU DU COURS]")
    print(tuteur_texte.answer(question))
    
    # 2. Les maths (RAG)
    print("\n[FORMULES]")
    print(expert_math.answer(question))
    
    # 3. Au-delà du cours (WEB)
    print("\n[POUR ALLER PLUS LOIN - BIBLIOGRAPHIE]")
    print(bibliothécaire.answer(question))



if __name__ == "__main__":
    print("🚀 Système Multi-Agents activé.")
    print("Tape 'q' pour quitter.\n")

    while True:
        # On récupère la requête de l'utilisateur ici !
        user_query = input("❓ Posez votre question (Cours/Calculs) : ")
        
        if user_query.lower() in ['q', 'quit', 'exit']:
            print("Au revoir !")
            break
            
        # On passe la requête à la fonction qui gère les experts
        interroger_tout_le_monde(user_query)