from newsapi import NewsApiClient

from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='569869d589e24c9484621b4adecc323d')

# top_headlines = newsapi.get_top_headlines(q='stock market', sources='cnbc', language='en')
# print(top_headlines)

sources = newsapi.get_sources()

print(sources)