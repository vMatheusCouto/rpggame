class Item:
    def __init__(self, tipo, nome, descricao, quantidade=1):
        self.__tipo = tipo
        self.__nome = nome
        self.__descricao = descricao
        self.quantidade = quantidade  

    @property
    def tipo(self):
        return self.__tipo

    @property
    def nome(self):
        return self.__nome

    @property
    def descricao(self):
        return self.__descricao

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, valor):
        self.__quantidade = max(0, valor) 

    def usar(self):
        if self.__quantidade > 0:
            self.__quantidade -= 1
            return True
        return False

    def __str__(self):
        return f"[{self.__nome}] x{self.__quantidade} - {self.__descricao}"