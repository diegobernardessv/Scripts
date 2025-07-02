from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol, Dict, List

# VIOLAÇÃO DO ISP - Interface muito "gorda"
class ProcessadorCompleto_VIOLACAO(ABC):
    """VIOLAÇÃO ISP: Interface muito grande forçando implementações desnecessárias"""
    
    @abstractmethod
    def mover_arquivo(self, origem: Path, destino: Path) -> bool:
        pass
    
    @abstractmethod
    def copiar_arquivo(self, origem: Path, destino: Path) -> bool:
        pass
    
    @abstractmethod
    def comprimir_arquivo(self, arquivo: Path) -> bool:
        pass
    
    @abstractmethod
    def criptografar_arquivo(self, arquivo: Path) -> bool:
        pass
    
    @abstractmethod
    def gerar_thumbnail(self, imagem: Path) -> bool:
        pass
    
    @abstractmethod
    def extrair_metadados(self, arquivo: Path) -> Dict:
        pass

# APLICAÇÃO CORRETA DO ISP - Interfaces segregadas e específicas

class Movimentador(Protocol):
    """Interface específica para mover arquivos"""
    def mover(self, origem: Path, destino: Path) -> bool:
        ...

class Copiador(Protocol):
    """Interface específica para copiar arquivos"""
    def copiar(self, origem: Path, destino: Path) -> bool:
        ...

class Compressor(Protocol):
    """Interface específica para compressão"""
    def comprimir(self, arquivo: Path) -> Path:
        ...

class ProcessadorImagem(Protocol):
    """Interface específica para processamento de imagens"""
    def gerar_thumbnail(self, imagem: Path, tamanho: tuple) -> Path:
        ...
    
    def redimensionar(self, imagem: Path, largura: int, altura: int) -> Path:
        ...

class ExtractorMetadados(Protocol):
    """Interface específica para extração de metadados"""
    def extrair_metadados(self, arquivo: Path) -> Dict:
        ...

# Implementações que usam apenas as interfaces necessárias (ISP)

class MovimentadorBasico:
    """Implementa apenas movimentação - não precisa de outras funcionalidades"""
    
    def mover(self, origem: Path, destino: Path) -> bool:
        try:
            destino.parent.mkdir(parents=True, exist_ok=True)
            origem.rename(destino)
            return True
        except Exception:
            return False

class CopiadorBasico:
    """Implementa apenas cópia - não precisa de outras funcionalidades"""
    
    def copiar(self, origem: Path, destino: Path) -> bool:
        try:
            import shutil
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origem, destino)
            return True
        except Exception:
            return False

class ProcessadorImagemAvancado:
    """Implementa apenas processamento de imagem"""
    
    def __init__(self, pasta_thumbnails: Path):
        self.pasta_thumbnails = pasta_thumbnails
    
    def gerar_thumbnail(self, imagem: Path, tamanho: tuple = (150, 150)) -> Path:
        # Simulação - em produção usaria PIL/Pillow
        thumbnail_path = self.pasta_thumbnails / f"thumb_{imagem.name}"
        thumbnail_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Aqui seria o código real de geração de thumbnail
        thumbnail_path.touch()  # Simula criação
        return thumbnail_path
    
    def redimensionar(self, imagem: Path, largura: int, altura: int) -> Path:
        # Simulação de redimensionamento
        novo_nome = f"{imagem.stem}_{largura}x{altura}{imagem.suffix}"
        novo_path = imagem.parent / novo_nome
        novo_path.touch()  # Simula criação
        return novo_path

class OrganizadorArquivos:
    """
    Classe que usa composição com interfaces específicas (ISP)
    Cada funcionalidade é injetada conforme necessário
    """
    
    def __init__(self, 
                 movimentador: Movimentador,
                 copiador: Copiador | None = None,
                 processador_imagem: ProcessadorImagem | None = None):
        self.movimentador = movimentador
        self.copiador = copiador
        self.processador_imagem = processador_imagem
    
    def organizar_por_tipo(self, origem: Path, mapa_destinos: Dict[str, Path]):
        """Usa apenas a interface de movimentação"""
        for arquivo in origem.iterdir():
            if arquivo.is_file():
                extensao = arquivo.suffix.lower()
                if extensao in mapa_destinos:
                    destino = mapa_destinos[extensao] / arquivo.name
                    self.movimentador.mover(arquivo, destino)
    
    def backup_com_organizacao(self, origem: Path, backup: Path, mapa_destinos: Dict[str, Path]):
        """Usa interfaces de cópia E movimentação quando disponíveis"""
        if not self.copiador:
            raise ValueError("Copiador necessário para backup")
        
        for arquivo in origem.iterdir():
            if arquivo.is_file():
                # Primeiro faz backup
                backup_arquivo = backup / arquivo.name
                self.copiador.copiar(arquivo, backup_arquivo)
                
                # Depois organiza
                extensao = arquivo.suffix.lower()
                if extensao in mapa_destinos:
                    destino = mapa_destinos[extensao] / arquivo.name
                    self.movimentador.mover(arquivo, destino)
    
    def processar_imagens(self, pasta_imagens: Path):
        """Usa interface de processamento de imagem quando disponível"""
        if not self.processador_imagem:
            raise ValueError("Processador de imagem necessário")
        
        extensoes_imagem = {'.jpg', '.png', '.gif', '.bmp'}
        
        for arquivo in pasta_imagens.iterdir():
            if arquivo.suffix.lower() in extensoes_imagem:
                self.processador_imagem.gerar_thumbnail(arquivo)

# Exemplo de uso demonstrando ISP:
# 
# # Cliente que só precisa mover arquivos
# organizador_simples = OrganizadorArquivos(
#     movimentador=MovimentadorBasico()
# )
# 
# # Cliente que precisa de backup + organização
# organizador_backup = OrganizadorArquivos(
#     movimentador=MovimentadorBasico(),
#     copiador=CopiadorBasico()
# )
# 
# # Cliente completo com processamento de imagem
# organizador_completo = OrganizadorArquivos(
#     movimentador=MovimentadorBasico(),
#     copiador=CopiadorBasico(),
#     processador_imagem=ProcessadorImagemAvancado(Path("./thumbnails"))
# ) 