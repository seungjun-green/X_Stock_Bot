import yfinance as yf
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import requests
from pytz import timezone
matplotlib.use('Agg')


### Markwt summary Image

def get_performance(ticker, price_ticker=None):
    stock_data = yf.Ticker(ticker).history(period="5d")
    if stock_data.empty:
        return None, None
    open_price = stock_data['Close'].iloc[-2]
    close_price = stock_data['Close'].iloc[-1]
    change = ((close_price - open_price) / open_price) * 100
    
    if price_ticker:
        price_data = yf.Ticker(price_ticker).history(period="1d")
        if not price_data.empty:
            close_price = price_data['Close'].iloc[-1]
    
    return change, close_price

def get_summary_img():
    today = datetime.now()
    formatted_date = today.strftime("%B %d, %Y")
    
    data = []
    
    for item in stock_info:
        name, ticker = item[0], item[1]
        price_ticker = item[2] if len(item) > 2 else ticker
        change, price = get_performance(ticker, price_ticker)
        
        data.append({
            'Name': name,
            'Ticker': twitter_style[price_ticker] if price_ticker in twitter_style else twitter_style[ticker],
            'Change': change,
            'Price': format_price(price, ticker)
        })
    
    df = pd.DataFrame(data)
    return df, formatted_date

def create_twitter_friendly_image(df, date):
    sections = [
        ("Stock Indices:", df[:4]),
        ("Volatility & Commodities:", df[4:9]),
        ("Other:", df[9:])
    ]

    # Calculate required height based on content
    num_items = sum(len(section_df) for _, section_df in sections)
    fig_height = 2 + (num_items * 0.4) + (len(sections) * 0.4)  # Adjust multipliers as needed
    
    fig, ax = plt.subplots(figsize=(8, fig_height))
    fig.patch.set_facecolor('#1e2129')
    ax.set_facecolor('#1e2129')

    # Title
    ax.text(0.5, 0.98, f"Market Summary: {date}", fontsize=20, fontweight='bold', 
            ha='center', va='top', color='white', transform=ax.transAxes)

    y_offset = 0.90
    for title, section_df in sections:
        ax.text(0.05, y_offset, title, fontsize=16, fontweight='bold', color='white')
        y_offset -= 0.06
        
        for _, row in section_df.iterrows():
            color = 'lime' if row['Change'] >= 0 else 'red'
            change_sign = '+' if row['Change'] >= 0 else ''
            name_text = f"{row['Name']}:"
            change_text = f"{change_sign}{row['Change']:.2f}%"
            price_text = f"{row['Price']}"
            
            ax.text(0.08, y_offset, name_text, fontsize=14, color='white')
            ax.text(0.65, y_offset, change_text, fontsize=14, color=color)
            ax.text(0.82, y_offset, price_text, fontsize=14, color='white')
            
            y_offset -= 0.06
        
        y_offset -= 0.04
        
    ax.text(0.99, -0.025, "@TodayUSMarkets", fontsize=14, color='white', ha='right', va='bottom', transform=ax.transAxes)

    ax.axis('off')

    # Create border effect without using Rectangle patch
    fig.patch.set_linewidth(2)
    fig.patch.set_edgecolor('gray')

    plt.tight_layout()
    plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
    plt.savefig('market_summary_tweet.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()


### market summary text

def get_summary_txt():
    today = datetime.now()
    formatted_date = today.strftime("%B %d, %Y")
    summary = [bold(f"𝗠𝗮𝗿𝗸𝗲𝘁 𝗦𝘂𝗺𝗺𝗮𝗿𝘆: {formatted_date}") + "\n"]

    summary.append("◆ Stock Indices:")
    for item in stock_info[:4]:
        name, ticker = item[0], item[1]
        price_ticker = item[2] if len(item) > 2 else ticker
        change, cp = get_performance(ticker)
        emoji = '🟩' if change >= 0 else '🟥'
        sign = '+' if change >= 0 else ''
        summary.append(f"{emoji} ${twitter_style[price_ticker]} {sign}{change:.2f}%")

    summary.append("\n◆ Volatility & Commodities:")
    for item in stock_info[4:9]:
        name, ticker = item[0], item[1]
        change, cp = get_performance(ticker)
        emoji = '🟩' if change >= 0 else '🟥'
        sign = '+' if change >= 0 else ''
        summary.append(f"{emoji} ${twitter_style[ticker]} {sign}{change:.2f}%")

    summary.append("\n◆ Other:")
    for item in stock_info[9:]:
        name, ticker = item[0], item[1]
        change, cp = get_performance(ticker)
        emoji = '🟩' if change >= 0 else '🟥'
        sign = '+' if change >= 0 else ''
        summary.append(f"{emoji} ${twitter_style[ticker]} {sign}{change:.2f}%")

    return "\n".join(summary)


### Pre Marker Summary
def get_premarket_performance(ticker, price_ticker=None):
    stock_data = yf.Ticker(ticker).history(period="5d")
    if stock_data.empty:
        return None, None
    open_price = stock_data['Close'].iloc[-2]
    close_price = stock_data['Open'].iloc[-1]
    change = ((close_price - open_price) / open_price) * 100
    
    if price_ticker:
        price_data = yf.Ticker(price_ticker).history(period="1d")
        if not price_data.empty:
            close_price = price_data['Close'].iloc[-1]
    
    return change, close_price

def get_premarket_summary_txt():
    today = datetime.now()
    formatted_date = today.strftime("%B %d, %Y")
    summary = [bold(f"Pre-𝗠𝗮𝗿𝗸𝗲𝘁 𝗦𝘂𝗺𝗺𝗮𝗿𝘆: {formatted_date}") + "\n"]
    
    summary.append("◆ Stock Indices:")
    for item in stock_info[:4]:
        name, ticker = item[0], item[1]
        price_ticker = item[2] if len(item) > 2 else ticker
        change, cp = get_premarket_performance(ticker=ticker)
        emoji = '🟩' if change >= 0 else '🟥'
        sign = '+' if change >= 0 else ''
        summary.append(f"{emoji} ${twitter_style[price_ticker]} {sign}{change:.2f}%")
    
    return "\n".join(summary)
        
        
        
### Votiale

def format_volume(volume):
    if volume >= 1_000_000_000:
        return f"{volume / 1_000_000_000:.2f}B"
    elif volume >= 1_000_000:
        return f"{volume / 1_000_000:.2f}M"
    else:
        return str(volume)
    
def get_votaile():
    params = {
    'function': 'TOP_GAINERS_LOSERS',
    'apikey': "JPT24Z0LF859O60N"
    }
    
    response = requests.get('https://www.alphavantage.co/query', params=params)
    data = response.json()
    
    res=""
    if 'most_actively_traded' in data:
        sorted_stocks = sorted(data['most_actively_traded'], key=lambda x: int(x['volume']), reverse=True)

        today = datetime.now(timezone('US/Eastern')).date().strftime("%B %d, %Y")
        res += f"Top 5 Stocks by Trading Volume - {today}:\n\n"
        for idx, stock in enumerate(sorted_stocks[:5]):
            formatted_volume = format_volume(int(stock['volume']))
            res += f"{idx+1}. ${stock['ticker']:<4} | Vol: {formatted_volume}, Price: ${stock['price']}\n"
    else:
        print("Unable to find 'most_actively_traded' in the API response. Here's what the response contains:")
        print(data.keys())
    
    return res.strip()



### Top5

def get_top5_news():
    res = ""
    url = "https://seekingalpha.com/api/v3/news/trending"

    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        print("!!ssss")
        trending_news = response.json()
        top_5_news = trending_news['data'][:5]  # Get the top 5 news articles
        print("soww")
        for idx, news in enumerate(top_5_news, 1):
            res+=f"{idx}. {news['attributes']['title']}\n"
            print(f"{idx}. {news['attributes']['title']}\n")
            print(res)
    else:
        print(f"Failed to retrieve trending news: {response.status_code}")
        
    return f"Top 5 Trending News Now: \n {res.strip()}"




### Helper

def bold(input_text):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold_chars = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
    output = ""
    for character in input_text:
        if character in chars:
            output += bold_chars[chars.index(character)]
        else:
            output += character 
    return output


def format_price(price, ticker):
    if price is None:
        return "N/A"
    if ticker in ["^TNX", "^VIX"]:
        return f"{price:.2f}"
    elif ticker in ["JPY=X", "EUR=X"]:
        return f"{price:.4f}"
    else:
        return f"${price:.2f}"
    
    
stock_info = [
    ("S&P 500", "SPY", "SPY"),
    ("Nasdaq", "QQQ", "QQQ"),
    ("Dow Jones", "^DJI", "DIA"),
    ("Russell 2000", "IWM", "IWM"),
    ("VIX", "^VIX"),
    ("Crude Oil", "CL=F"),
    ("Gold", "GC=F"),
    ("Silver", "SI=F"),
    ("10Y Treasury Yield", "^TNX"),
    ("USD/JPY", "JPY=X"),
    ("EUR/USD", "EUR=X")
]

twitter_style = {
    "SPY": "SPY",
    "QQQ": "QQQ",
    "DIA": "DJI",
    "IWM": "IWM",
    "^VIX": "VIX",
    "CL=F": "CLF",
    "GC=F": "GCF",
    "SI=F": "SIF",
    "^TNX": "TNX",
    "JPY=X": "JPY",
    "EUR=X": "EUR"
    }
