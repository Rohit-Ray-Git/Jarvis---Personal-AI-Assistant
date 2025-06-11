# web.py
# Placeholder for web search and scraping commands 

import requests
from bs4 import BeautifulSoup
from commands.llm import get_llm_response

def search_and_summarize(query, num_results=3):
    url = f'https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for a in soup.select('.result__a', limit=num_results):
            title = a.get_text()
            href = a['href']
            snippet_tag = a.find_parent('div', class_='result').find('a', class_='result__snippet')
            snippet = snippet_tag.get_text() if snippet_tag else ''
            results.append(f"{title}\n{href}\n{snippet}")
        if not results:
            return "No web results found."
        # Summarize using LLM if available
        summary_prompt = "Summarize the following web search results for the query: '" + query + "'\n\n" + "\n\n".join(results)
        summary = get_llm_response(summary_prompt)
        return summary + "\n\n" + "\n\n".join(results)
    except Exception as e:
        return f"Web search failed: {e}" 