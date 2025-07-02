from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol

class EstrategiaOrganizacao(Protocol):
    """Interface para estratégias de organização"""
    def obter_destino(self, arquivo: Path) -> Path | None:
        """Retorna o destino do arquivo ou None se não deve ser movido"""
        ...

class OrganizacaoPorExtensao:
    """Estratégia: organizar por extensão de arquivo"""
    def __init__(self, mapa_extensoes: dict[str, Path]):
        self.mapa_extensoes = mapa_extensoes
    
    def obter_destino(self, arquivo: Path) -> Path | None:
        extensao = arquivo.suffix.lower()
        if extensao in self.mapa_extensoes:
            return self.mapa_extensoes[extensao] / arquivo.name
        return None

class OrganizacaoPorTamanho:
    """Nova estratégia: organizar por tamanho (extensível!)"""
    def __init__(self, pasta_pequenos: Path, pasta_grandes: Path, limite_mb: int = 10):
        self.pasta_pequenos = pasta_pequenos
        self.pasta_grandes = pasta_grandes
        self.limite_bytes = limite_mb * 1024 * 1024
    
    def obter_destino(self, arquivo: Path) -> Path | None:
        tamanho = arquivo.stat().st_size
        if tamanho < self.limite_bytes:
            return self.pasta_pequenos / arquivo.name
        else:
            return self.pasta_grandes / arquivo.name

class OrganizacaoPorData:
    """Nova estratégia: organizar por data de criação (extensível!)"""
    def __init__(self, pasta_base: Path):
        self.pasta_base = pasta_base
    
    def obter_destino(self, arquivo: Path) -> Path | None:
        import datetime
        timestamp = arquivo.stat().st_ctime
        data = datetime.datetime.fromtimestamp(timestamp)
        pasta_ano = self.pasta_base / str(data.year)
        pasta_mes = pasta_ano / f"{data.month:02d}-{data.strftime('%B')}"
        return pasta_mes / arquivo.name

class OrganizadorExtensivel:
    """Organizador que aceita diferentes estratégias (OCP!)"""
    def __init__(self, estrategia: EstrategiaOrganizacao):
        self.estrategia = estrategia
    
    def definir_estrategia(self, nova_estrategia: EstrategiaOrganizacao):
        """Permite trocar estratégia sem modificar a classe"""
        self.estrategia = nova_estrategia
    
    def organizar(self, caminho_origem: Path) -> None:
        for arquivo in caminho_origem.iterdir():
            if arquivo.is_file():
                destino = self.estrategia.obter_destino(arquivo)
                if destino:
                    destino.parent.mkdir(parents=True, exist_ok=True)
                    arquivo.rename(destino)
                    print(f"Movido: {arquivo.name} → {destino.parent}")

# Exemplo de uso:
# organizador = OrganizadorExtensivel(OrganizacaoPorExtensao(mapa_extensoes))
# organizador.organizar(caminho_origem)
# 
# # Mudança de estratégia sem modificar código existente
# organizador.definir_estrategia(OrganizacaoPorTamanho(pasta_pequenos, pasta_grandes))
# organizador.organizar(caminho_origem) 