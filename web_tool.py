from duckduckgo_search import DDGS

class WebSearchTool:
    def __init__(self, max_results=3):
        self.max_results = max_results

    def search_bibliographies(self, topic: str):
        """Cherche des références de livres ou articles sur un sujet."""
        query = f"bibliographie officielle et livres de référence sur : {topic}"
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=self.max_results))
        
        if not results:
            return "Aucune bibliographie trouvée sur le web."
        
        formatted_results = []
        for r in results:
            formatted_results.append(f"- {r['title']}\n  Lien: {r['href']}")
            
        return "\n\n".join(formatted_results)