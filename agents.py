
import openai

class TextualAgent:
    def __init__(self, rag_tool):
        self.rag_tool = rag_tool
        self.system_prompt = (
            "Tu es un expert en analyse textuelle. Explique les concepts pédagogiquement. "
            "CONSIGNE : Ne donne JAMAIS de formules, concentre-toi sur les idées."
        )

    def answer(self, user_query: str):
        # CHANGEMENT : On appelle la méthode spécifique "theory"
        context = self.rag_tool.run_theory_search(user_query) 
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"CONTEXTE :\n{context}\n\nQUESTION : {user_query}"}
        ]
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.1)
        return response.choices[0].message.content

class MathAgent:
    def __init__(self, rag_tool):
        self.rag_tool = rag_tool
        self.system_prompt = (
            "Tu es un expert en mathématiques. Extrait les formules en format LaTeX ($$)."
            "Si aucune formule n'est trouvée, dis : 'Aucune équation détectée'."
        )

    def answer(self, user_query: str):
        # CHANGEMENT : On appelle la méthode spécifique "math"
        context = self.rag_tool.run_math_search(user_query)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"CONTEXTE :\n{context}\n\nQUESTION : {user_query}"}
        ]
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.1)
        return response.choices[0].message.content


class BiblioAgent:
    def __init__(self):
        self.web_tool = WebSearchTool()
        self.model = "gpt-4o-mini"
        self.system_prompt = (
            "Tu es un bibliothécaire universitaire. Ta mission est de proposer "
            "une bibliographie complémentaire rigoureuse. "
            "Présente les titres de livres ou articles et explique brièvement "
            "pourquoi ils sont importants pour approfondir le sujet."
        )

    def answer(self, topic: str):
        # 1. Recherche web
        raw_data = self.web_tool.search_bibliographies(topic)
        
        # 2. Mise en forme par GPT
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Sujet: {topic}\n\nRésultats web trouvés:\n{raw_data}"}
        ]
        response = openai.chat.completions.create(model=self.model, messages=messages, temperature=0.5)
        return response.choices[0].message.content
