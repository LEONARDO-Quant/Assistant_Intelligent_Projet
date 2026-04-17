import openai
from web_tool import WebSearchTool

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
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content