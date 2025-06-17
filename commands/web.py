# web.py
# Placeholder for web search and scraping commands 

import os
import requests
from commands.llm import get_llm_response

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_and_summarize(query, num_results=5):
    if not TavilyClient or not TAVILY_API_KEY:
        return {'summary': "Tavily API not configured. Please install tavily-python and set TAVILY_API_KEY in your .env.", 'results': []}
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        tavily_results = client.search(query, max_results=num_results)
        results = []
        for r in tavily_results.get("results", []):
            results.append({
                'title': r.get('title', ''),
                'url': r.get('url', ''),
                'snippet': r.get('content', '')
            })
        if not results:
            return {'summary': "No web results found.", 'results': []}
        # Summarize using LLM if available
        summary_prompt = "Summarize the following web search results for the query: '" + query + "'\n\n"
        for r in results:
            summary_prompt += f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}\n\n"
        summary = get_llm_response(summary_prompt)
        # Format as markdown
        md = f"**Web Summary:**\n\n{summary}\n\n---\n"
        for r in results:
            md += f"- [{r['title']}]({r['url']})  "
            md += f"<br><span style='color:gray'>{r['url']}</span>  "
            if r['snippet']:
                md += f"<br><i>{r['snippet']}</i>"
            md += "\n\n"
        return {'summary': md, 'results': results}
    except Exception as e:
        return {'summary': f"Web search failed: {e}", 'results': []} 