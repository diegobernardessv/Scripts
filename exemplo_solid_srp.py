import os
import shutil
from typing import Dict
from pathlib import Path

class ConfiguracaoOrganizador:
    """Responsabilidade única: gerenciar configurações"""
    def __init__(self):
        self.caminho_origem = Path("D:/Users/diego.b.silva/Desktop/DiegoBernardes")
        self.mapa_extensoes = {
            ".pdf": Path("D:/Users/diego.b.silva/Desktop/PDF"),
            ".png": Path("D:/Users/diego.b.silva/Desktop/PNG"),
            ".docx": Path("D:/Users/diego.b.silva/Desktop/DOCX"),
            ".xlsx": Path("D:/Users/diego.b.silva/Desktop/XLSX"),
            ".jpg": Path("D:/Users/diego.b.silva/Desktop/JPG"),
            ".zip": Path("D:/Users/diego.b.silva/Desktop/ZIP"),
            ".exe": Path("D:/Users/diego.b.silva/Desktop/EXE")
        }

class GerenciadorDiretorios:
    """Responsabilidade única: criar e gerenciar diretórios"""
    @staticmethod
    def criar_diretorios(caminhos: set[Path]) -> None:
        for caminho in caminhos:
            caminho.mkdir(parents=True, exist_ok=True)

class OrganizadorArquivos:
    """Responsabilidade única: mover arquivos"""
    def __init__(self, configuracao: ConfiguracaoOrganizador):
        self.config = configuracao
    
    def organizar(self) -> None:
        # Criar diretórios necessários
        GerenciadorDiretorios.criar_diretorios(set(self.config.mapa_extensoes.values()))
        
        # Organizar arquivos
        for arquivo in self.config.caminho_origem.iterdir():
            if arquivo.is_file():
                self._mover_arquivo(arquivo)
    
    def _mover_arquivo(self, arquivo: Path) -> None:
        extensao = arquivo.suffix.lower()
        if extensao in self.config.mapa_extensoes:
            destino = self.config.mapa_extensoes[extensao] / arquivo.name
            shutil.move(str(arquivo), str(destino))
            print(f"Movido: {arquivo.name} → {destino.parent.name}") 