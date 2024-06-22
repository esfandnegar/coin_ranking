from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import URLError
from time import sleep

def get_coin_ranking_prices():
    html_coin_ranking = urlopen('https://coinranking.com/')
    bs_coin_ranking = BeautifulSoup(html_coin_ranking.read(), 'lxml')
    table_rows_coin_ranking = bs_coin_ranking.find_all('div', {'class': 'coin-list__body'})
    
    prices_coin_ranking = {}
    for row in table_rows_coin_ranking[:10]:  # First 10 coins
        symbol = row.find('span', {'class': 'coin-name'}).get_text().strip()
        price_string = row.find('div', {'class': 'coin-list__price'}).get_text().replace('$', '').replace(" ", "").replace("\n", "").replace(",", "")
        price = float(price_string)
        prices_coin_ranking[symbol] = price
    return prices_coin_ranking

def get_coin_market_cap_prices():
    html_coin_market_cap = urlopen('https://coinmarketcap.com/')
    bs_coin_market_cap = BeautifulSoup(html_coin_market_cap.read(), 'lxml')
    table_rows_coin_market_cap = bs_coin_market_cap.find_all('tr', {'class': 'cmc-table-row'})
    
    prices_coin_market_cap = {}
    for row in table_rows_coin_market_cap[:10]:  # First 10 coins
        symbol = row.find('td', {'class': 'cmc-table_cell--sort-by_symbol'}).get_text().strip()
        price_string = row.find('td', {'class': 'cmc-table_cell--sort-by_price'}).get_text().replace('$', '').replace(" ", "").replace("\n", "").replace(",", "")
        price = float(price_string)
        prices_coin_market_cap[symbol] = price
    return prices_coin_market_cap

while True:
    try:
        prices_coin_ranking = get_coin_ranking_prices()
        prices_coin_market_cap = get_coin_market_cap_prices()

        for symbol in prices_coin_ranking:
            if symbol in prices_coin_market_cap:
                price_ranking = prices_coin_ranking[symbol]
                price_market_cap = prices_coin_market_cap[symbol]
                if price_ranking < price_market_cap:
                    print(f"{symbol}: Coin Ranking")
                else:
                    print(f"{symbol}: Coin Market Cap")

    except URLError as e:
        print('you should connect to internet')
        sleep(1)