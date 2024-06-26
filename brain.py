import yfinance as yf
from datetime import datetime
from prettytable import PrettyTable
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('Agg')


stock_info = [
    ("S&P 500", "^GSPC", "SPY"),
    ("Nasdaq", "^IXIC", "QQQ"),
    ("Dow Jones", "^DJI", "DIA"),
    ("Russell 2000", "^RUT", "IWM"),
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
    "DIA": "DIA",
    "IWM": "IWM",
    "^VIX": "VIX",
    "CL=F": "CLF",
    "GC=F": "GCF",
    "SI=F": "SIF",
    "^TNX": "TNX",
    "JPY=X": "JPY",
    "EUR=X": "EUR"
    }


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


def format_price(price, ticker):
    if price is None:
        return "N/A"
    if ticker in ["^TNX", "^VIX"]:
        return f"{price:.2f}"
    elif ticker in ["JPY=X", "EUR=X"]:
        return f"{price:.4f}"
    else:
        return f"${price:.2f}"


def get_summary():
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
    
    
# df, date_str = get_summary()
# create_twitter_friendly_image(df, date_str)