import requests
from bs4 import BeautifulSoup
import pandas as pd

# 商品情報をスクレイピングする関数
def scrape_amazon_product(asin):
    url = f'https://www.amazon.com/dp/{asin}'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find(id='productTitle').text.strip()
        try:
            price = soup.find('span', 'a-price').find('span', 'a-offscreen').text
        except AttributeError:
            price = 'Price not found'
        return {
            'ASIN': asin,
            'Title': title,
            'Price': price
        }
    else:
        return {
            'ASIN': asin,
            'Title': 'Product not found',
            'Price': 'N/A'
        }

# ASINリスト
asins = ['B08N5LNQCX', 'B07PGL2ZSL']  # 例

# 商品情報の取得
products = [scrape_amazon_product(asin) for asin in asins]

# Pandas DataFrameに変換
df = pd.DataFrame(products)

# Excelファイルに保存
df.to_excel('amazon_products.xlsx', index=False)
