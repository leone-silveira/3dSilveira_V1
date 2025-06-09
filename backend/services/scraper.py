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
