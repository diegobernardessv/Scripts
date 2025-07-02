import os
import shutil
import datetime

caminho_origem = "D:/Users/diego.b.silva/Desktop/Diego Bernardes"

mapa_pastas = {
    ".pdf":"D:/Users/diego.b.silva/Desktop/PDF",
    ".png":"D:/Users/diego.b.silva/Desktop/PNG",
    ".docx":"D:/Users/diego.b.silva/Desktop/DOCX",
    ".xlsx":"D:/Users/diego.b.silva/Desktop/XLSX",
    ".jpg":"D:/Users/diego.b.silva/Desktop/JPG",
    ".zip":"D:/Users/diego.b.silva/Desktop/ZIP",
    ".exe":"D:/Users/diego.b.silva/Desktop/EXE",
    ".pbix":"D:/Users/diego.b.silva/Desktop/PBIX"
}

for pasta in set(mapa_pastas.values()): 
    # os.makedirs com exist_ok=True não gera erro se a pasta já existe
    os.makedirs(pasta, exist_ok=True) 

def organizar_downloads():
    print(f"Monitorando a pasta: {"D:/Users/diego.b.silva/Desktop/Diego Bernardes"}")
    # Lista os arquivos no diretório de origem
    arquivos_origem = os.listdir("D:/Users/diego.b.silva/Desktop/Diego Bernardes")

    for nome_arquivo in arquivos_origem:
        caminho_completo_origem = os.path.join("D:/Users/diego.b.silva/Desktop/Diego Bernardes",nome_arquivo)

        # Verifica se é um arquivo (e não uma pasta)
        if os.path.isfile(caminho_completo_origem):
            # Obtém a extensão do arquivo
            _, extensao = os.path.splitext(nome_arquivo) 
            extensao = extensao.lower() # Normaliza para minúsculas


        # Verifica se a extensão está no nosso mapa
        if extensao in mapa_pastas:
            caminho_destino = mapa_pastas[extensao]
            caminho_completo_destino = os.path.join(caminho_destino, nome_arquivo)

            print(f"Movendo '{nome_arquivo}' para '{caminho_destino}'...")

            # Move o arquivo
            shutil.move(caminho_completo_origem, caminho_completo_destino)
        else:    
            print(f"Arquivo '{nome_arquivo}' com extensão '{extensao}' não tem pasta de destino definida.")


# Executa a função de organização
organizar_downloads()
print("Organização concluída")

