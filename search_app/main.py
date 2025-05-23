from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import List, Dict

app = FastAPI()

# Stub function to simulate search engine results
def search_engine(name: str, query: str) -> List[Dict[str, str]]:
    results = []
    for i in range(1, 16):
        results.append({
            'title': f'{name} Result {i} for {query}',
            'url': f'https://{name.lower()}.com/search?q={query}&result={i}',
            'score': 1.0 / i
        })
    return results


def aggregate_results(query: str) -> List[Dict[str, str]]:
    engines = ['Google', 'Bing', 'DuckDuckGo', 'Brave']
    all_results = []
    for engine in engines:
        all_results.extend(search_engine(engine, query))
    all_results.sort(key=lambda x: x['score'], reverse=True)
    return all_results[:5]


FORM = """
<!DOCTYPE html>
<html>
<head><title>Search Aggregator</title></head>
<body>
    <h1>Search Aggregator</h1>
    <form method='get'>
        <input type='text' name='q' value='{query}' required>
        <button type='submit'>Search</button>
    </form>
    {results}
</body>
</html>
"""


def render_results(query: str, results: List[Dict[str, str]]) -> str:
    if not results:
        return ""
    items = ''.join(
        f"<li><a href='{r['url']}'>{r['title']}</a> - score {r['score']:.2f}</li>"
        for r in results
    )
    return f"<h2>Top Results for '{query}'</h2><ul>{items}</ul>"


@app.get('/', response_class=HTMLResponse)
async def get_form(q: str | None = None):
    query = q or ''
    results_html = ''
    if q:
        results = aggregate_results(q)
        results_html = render_results(q, results)
    html = FORM.format(query=query, results=results_html)
    return HTMLResponse(content=html)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
