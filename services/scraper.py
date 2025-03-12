import requests
from bs4 import BeautifulSoup
import json

LIMITED_FILAMENTS = 10


def get_mercadolivre_filaments():
    url = "https://lista.mercadolivre.com.br/filamento-pla-1.75mm"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script', {'type': 'application/ld+json'})

    filamentos = []

    if response.status_code != 200:
        print("Erro ao acessar o Mercado Livre")
        return []

    for script in scripts:
        try:
            data = json.loads(script.string)
            if "@graph" in data:
                for item in data["@graph"]:
                    if item.get("@type") == "Product":
                        nome = item.get("name", "N/A")
                        preco = item.get("offers", {}).get("price", "N/A")
                        url = item.get("offers", {}).get("url", "N/A")
                        brand = item.get("brand", {}).get("name", "N/A")
                        filamentos.append(
                            {
                                "name": nome,
                                "brand": brand,
                                "price": preco,
                                "url": url
                            })
        except json.JSONDecodeError:
            continue

    filamentos.sort(key=lambda x: float(
        x["price"]) if x["price"] != "N/A" else float('inf'))

    return filamentos[:LIMITED_FILAMENTS]


def get_amazon_filaments():
    url = "https://www.amazon.com.br/s?k=filamento+3d+1kg+pla+1.75mm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Erro ao acessar a Amazon")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    filaments = []
    print(soup)
    results = soup.find_all("div", {"data-component-type": "s-search-result"})

    for item in results:
        try:
            name = item.find("span", class_="a-size-medium").text.strip()
            price_whole = item.find("span", class_="a-price-whole")
            price_fraction = item.find("span", class_="a-price-fraction")
            price = f"{price_whole.text},{price_fraction.text}" if price_whole and price_fraction else "N/A"
            url = "https://www.amazon.com.br" + item.find("a", class_="a-link-normal")["href"]

            filaments.append({"name": name, "price": price, "url": url})

        except AttributeError:
            continue

    return filaments

a = get_amazon_filaments()
