import serpapi

params = {
  "q": "YOUR_KEYWORD",
  "api_key": "YOUR_KEY"
}

results = serpapi.search(params)
snippet = results['featured_snippet']['text']

# Rewrite your content to match snippet length
optimal_length = len(snippet.split())
