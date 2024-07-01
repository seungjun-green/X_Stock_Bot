import requests


    
def get_top5_news():
    res = ""
    url = "https://seekingalpha.com/api/v3/news/trending"
    headers = {
        f'Authorization': 'Bearer {API_KEY}'
    }

    response = requests.get(url)
    if response.status_code == 200:
        trending_news = response.json()
        top_5_news = trending_news['data'][:5]  # Get the top 5 news articles
        for idx, news in enumerate(top_5_news, 1):
            res+=f"{idx}. {news['attributes']['title']}\n"
            print(f"{idx}. {news['attributes']['title']}\n")
            print(res)
    else:
        print(f"Failed to retrieve trending news: {response.status_code}")
        
    return f"Topv 5 Trending News Now: \n {res.strip()}"


print(get_top5_news())