import requests

url = "https://api.github.com" 
response = requests.get(url)
if response.status_code == 200: 
    print("Sucesso!") 
else: 
    print(f"Falha com código de status: {response.status_code}")

dados = response.json()
print(dados['current_user_url'])

# Procurando repositórios Python populares no GitHub 
url_busca = "https://api.github.com/search/repositories" 
parametros = {"q": "language:python", "sort": "stars", "order": "desc"}

response = requests.get(url_busca,params=parametros)

resultados_populares = response.json()['items']
for repo in resultados_populares[:3]:
    print(f'Nome:{repo['name']}, Estrelas: {repo['stargazers_count']}')