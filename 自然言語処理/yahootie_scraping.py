
import pandas as pd
import requests
from bs4 import BeautifulSoup

def read_urls_from_csv(file_path):
    df = pd.read_csv(file_path)
    # 仮にURLが 'url' というカラム名で保存されているとする
    return df['url'].tolist()

def sitescraping(url):
    # ページの内容を取得
    response = requests.get(url)
    response.raise_for_status()  # リクエストが成功したか確認

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(response.text, 'html.parser')

    # 特定の要素を抽出
    element = soup.find('p', class_="yjSlinkDirectlink ClapLv1TextBlock_Chie-TextBlock__Text__1jsQC ClapLv1TextBlock_Chie-TextBlock__Text--mediumRelative__3HSR8 ClapLv1TextBlock_Chie-TextBlock__Text--SpaceOut__3kF8R ClapLv1TextBlock_Chie-TextBlock__Text--preLine__2SRma")

    # テキスト内容を抽出
    if element:
        text_content = element.get_text(strip=True)
    else:
        text_content = "指定された要素が見つかりませんでした。"
    return text_content

def main(input_csv_path, output_csv_path):
    urls = read_urls_from_csv(input_csv_path)
    results = []

    for url in urls:
        print(f"Processing URL: {url}")
        text_content = sitescraping(url)
        results.append({"URL": url, "Content": text_content})

    # DataFrameを作成してCSVに書き込む
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_csv_path, index=False, encoding='shift-jis', errors='ignore')

# 入力CSVファイルのパスと出力CSVファイルのパスを指定して実行
input_csv_path = 'urls.csv'
output_csv_path = 'scraped_content.csv'
main(input_csv_path, output_csv_path)
