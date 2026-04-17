import openai
from rag_tool import RAGDocumentTool

class TextualAgent:
    def __init__(self, rag_tool: RAGDocumentTool):
        self.rag_tool = rag_tool
        self.model = "gpt-4o-mini"
        # Le System Prompt définit la personnalité et la concision
        self.system_prompt = (
            "Tu es un expert en analyse textuelle et un tuteur pédagogique. "
            "Ta mission est d'expliquer les concepts de manière claire et concise. "
            "Utilise EXCLUSIVEMENT le contexte fourni pour répondre. "
            "Si l'information est absente, dis-le simplement. "
            "Ne donne JAMAIS de formules mathématiques complexes, concentre-toi sur les idées!."
        )

    def answer(self, user_query: str):
        # 1. L'agent utilise l'outil pour récupérer la matière première (le texte brut)
        context = self.rag_tool.run(user_query) 

        # 2. L'agent traite l'information avec son propre "cerveau"
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"CONTEXTE RÉCUPÉRÉ :\n{context}\n\nQUESTION : {user_query}"}
        ]

        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1 # Bas pour éviter les inventions
        )

        return response.choices[0].message.content
    
# --- LE BLOC QUI MANQUAIT PEUT-ÊTRE ---
if __name__ == "__main__":
    # 1. Charger l'outil (Vérifie bien ton chemin !)
    PATH_DATA = r"C:\Users\Utilisateur\Desktop\Panthéon-Sorbonne VII\Assistant_Intelligent_Multi-agents\data"
    
    print("🤖 Initialisation de l'Agent Textuel...")
    shared_rag = RAGDocumentTool(docs_dir=PATH_DATA)
    
    # 2. Initialiser l'agent
    agent = TextualAgent(rag_tool=shared_rag)
    
    # 3. Test interactif
    print("\n✅ Agent prêt ! (Tape 'q' pour quitter)")
    while True:
        q = input("\nQuestion (Texte) : ")
        if q.lower() == 'q':
            break
        
        reponse = agent.answer(q)
        print("\nREPONSE DE L'AGENT :")
        print("-" * 30)
        print(reponse)
        print("-" * 30)