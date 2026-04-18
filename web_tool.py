import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()  # Charge les variables d'environnement depuis le fichier .env

class WebSearchTool:
    def __init__(self, api_key=None, max_results=3):
        # Remplace par ta clé API Tavily (gratuite sur leur site)
        actual_key = api_key or os.getenv("TAVILY_API_KEY")
        
        if not actual_key:
            raise ValueError("❌ Clé API Tavily non trouvée. Vérifiez votre fichier .env")
            
        self.client = TavilyClient(api_key=actual_key)
        self.max_results = max_results

    def search(self, query: str):
        """Recherche via l'API Tavily et donne des réponses pertinentes."""
        try:
            # Effectue une recherche simple
            response = self.client.search(query=query, max_results=self.max_results)
            results = response.get('results', [])
            
            if not results:
                return "❌ Aucun résultat trouvé."
            
            formatted_results = []
            for r in results:
                # Formatage propre : Titre, Lien, et un extrait (content)
                formatted_results.append(f"🔹 {r['title']}\n   {r['url']}\n   {r['content'][:150]}...")
            
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            return f"⚠️ Erreur Tavily : {str(e)}"

tavily_tool = WebSearchTool()
