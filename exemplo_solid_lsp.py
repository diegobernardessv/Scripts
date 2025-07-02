from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class ProcessadorArquivo(ABC):
    """Classe base que define contrato para processadores"""
    
    @abstractmethod
    def processar(self, arquivo: Path) -> bool:
        """
        Processa um arquivo.
        Retorna True se processado com sucesso, False caso contrário.
        Não deve modificar o arquivo original sem permissão.
        """
        pass
    
    @abstractmethod
    def pode_processar(self, arquivo: Path) -> bool:
        """Verifica se pode processar este tipo de arquivo"""
        pass

class ProcessadorImagem(ProcessadorArquivo):
    """Processador que respeita o contrato da classe pai (LSP correto)"""
    
    def __init__(self, pasta_destino: Path):
        self.pasta_destino = pasta_destino
        self.extensoes_suportadas = {'.jpg', '.png', '.gif', '.bmp'}
    
    def pode_processar(self, arquivo: Path) -> bool:
        return arquivo.suffix.lower() in self.extensoes_suportadas
    
    def processar(self, arquivo: Path) -> bool:
        """Move imagem mantendo o contrato (não modifica original)"""
        if not self.pode_processar(arquivo):
            return False
        
        try:
            destino = self.pasta_destino / arquivo.name
            destino.parent.mkdir(parents=True, exist_ok=True)
            arquivo.rename(destino)
            return True
        except Exception:
            return False

class ProcessadorDocumento(ProcessadorArquivo):
    """Processador que respeita o contrato da classe pai (LSP correto)"""
    
    def __init__(self, pasta_destino: Path):
        self.pasta_destino = pasta_destino
        self.extensoes_suportadas = {'.pdf', '.docx', '.txt', '.xlsx'}
    
    def pode_processar(self, arquivo: Path) -> bool:
        return arquivo.suffix.lower() in self.extensoes_suportadas
    
    def processar(self, arquivo: Path) -> bool:
        """Move documento mantendo o contrato"""
        if not self.pode_processar(arquivo):
            return False
        
        try:
            destino = self.pasta_destino / arquivo.name
            destino.parent.mkdir(parents=True, exist_ok=True)
            arquivo.rename(destino)
            return True
        except Exception:
            return False

class ProcessadorArquivo_VIOLACAO_LSP(ProcessadorArquivo):
    """EXEMPLO DE VIOLAÇÃO DO LSP - NÃO FAZER ISSO!"""
    
    def pode_processar(self, arquivo: Path) -> bool:
        return arquivo.suffix.lower() == '.txt'
    
    def processar(self, arquivo: Path) -> bool:
        """VIOLA LSP: modifica arquivo original!"""
        if not self.pode_processar(arquivo):
            return False
        
        # VIOLAÇÃO: modifica o arquivo original!
        with open(arquivo, 'a') as f:
            f.write("\n--- Processado ---")
        
        # VIOLAÇÃO: pode lançar exceção inesperada!
        raise Exception("Processamento falhou!")

class GerenciadorProcessamento:
    """Classe que funciona com qualquer ProcessadorArquivo (LSP)"""
    
    def __init__(self):
        self.processadores: List[ProcessadorArquivo] = []
    
    def adicionar_processador(self, processador: ProcessadorArquivo):
        """Aceita qualquer processador que implemente corretamente a interface"""
        self.processadores.append(processador)
    
    def processar_pasta(self, caminho: Path) -> None:
        """Funciona com qualquer processador que respeite o contrato"""
        for arquivo in caminho.iterdir():
            if arquivo.is_file():
                for processador in self.processadores:
                    if processador.pode_processar(arquivo):
                        sucesso = processador.processar(arquivo)
                        if sucesso:
                            print(f"✓ {arquivo.name} processado por {type(processador).__name__}")
                            break
                        else:
                            print(f"✗ Falha ao processar {arquivo.name}")

# Exemplo de uso demonstrando LSP:
# gerenciador = GerenciadorProcessamento()
# gerenciador.adicionar_processador(ProcessadorImagem(Path("./imagens")))
# gerenciador.adicionar_processador(ProcessadorDocumento(Path("./documentos")))
# 
# # Qualquer processador pode ser substituído sem quebrar o código
# gerenciador.processar_pasta(Path("./origem")) 