
from rag_tool import RAGDocumentTool, theory_engine, stats_engine
from agents import TextualAgent, MathAgent, WebAgent
import openai



class MasterAgent:
    def __init__(self, theory_engine, stats_engine):
        # Initialisation des sous-agents
        self.text_agent = TextualAgent(rag_tool=theory_engine)
        self.math_agent = MathAgent(rag_tool=stats_engine)
        self.web_agent = WebAgent()

        # Initialisation de la mémoire
        self.chat_history = []
        
        self.system_prompt = (
            "Tu es l'Agent Master, le cerveau d'une application multi-experts. Analyse la requête en fonction de l'historique et de la question.\n"
            "Ton rôle est d'analyser la requête de l'utilisateur et de choisir l'action appropriée :\n"
            "1. Si la question porte sur des concepts théoriques ou de définition (ex: 'C'est quoi...'), utilise la THEORIE.\n"
            "2. Si la question demande des formules, des calculs ou des stats, utilise les MATHS.\n"
            "3. Si la question porte sur l'actualité ou demande des infos externes aux cours, utilise le WEB.\n"
            "4. Si c'est une salutation ou une conversation banale, réponds directement par toi-même.\n\n"
            "Réponds UNIQUEMENT avec l'un de ces mots-clés au début : [THEORIE], [MATHS], [WEB] ou [DIRECT]."
            "Si l'utilisateur pose une question de suivi (ex: 'Explique plus'), base-toi sur le dernier agent utilisé."

        )

    def answer(self, user_query: str):
        # 1. Préparer les messages pour le routing (avec mémoire pour comprendre les 'il', 'ça', 'encore')
        routing_messages = [{"role": "system", "content": self.system_prompt}]
        # On donne les 5 derniers échanges au router pour le contexte
        routing_messages.extend(self.chat_history[-5:]) 
        routing_messages.append({"role": "user", "content": user_query})
        
        routing_res = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=routing_messages,
            temperature=0.3
        )
        decision = routing_res.choices[0].message.content.upper()

        # 2. Délégation et récupération de la réponse
        if "[THEORIE]" in decision:
            print("🧠 Le Master délègue à l'Agent Textuel...")
            response = self.text_agent.answer(user_query)
        elif "[MATHS]" in decision:
            print("🔢 Le Master délègue à l'Agent Math...")
            response = self.math_agent.answer(user_query)
        elif "[WEB]" in decision:
            print("🌐 Le Master délègue à l'Agent Web...")
            response = self.web_agent.answer(user_query)
        else:
            # Conversation directe
            conv_messages = [{"role": "system", "content": "Tu es un assistant utile."}]
            conv_messages.extend(self.chat_history[-10:]) # Mémoire plus longue pour la parlote
            conv_messages.append({"role": "user", "content": user_query})
            
            res = openai.chat.completions.create(model="gpt-4o-mini", messages=conv_messages)
            response = res.choices[0].message.content

        # 3. MISE À JOUR DE LA MÉMOIRE
        self.chat_history.append({"role": "user", "content": user_query})
        self.chat_history.append({"role": "assistant", "content": response})
        
        return response
    
