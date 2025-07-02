import requests

url_scrape = 'https://quotes.toscrape.com'
response = requests.get(url_scrape)
html_bruto = response.text

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_bruto,'html.parser')

# Encontra todas as citações
citacoes = soup.find_all('span', class_='text')

# Encontra todos os autores
autores = soup.find_all('small', class_='author')

for i in range(len(citacoes)):
    # Extrai apenas o conteúdo textual da tag
    print(f'Citação: {citacoes[i].text}')
    print(f'Autor: {autores[i].text}\n')