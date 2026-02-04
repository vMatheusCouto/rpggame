class Item:
    def __init__(self, tipo, nome, descricao, quantidade=1):
        self._tipo = tipo
        self._nome = nome
        self._descricao = descricao
        self._quantidade = quantidade

    # Converter tudo para o inglês. Português apenas visual (menus, botões, golpes, etc.)

    @property
    def tipo(self):
        return self._tipo

    @property
    def nome(self):
        return self._nome

    @property
    def descricao(self):
        return self._descricao

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor):
        self._quantidade = max(0, valor)

    def usar(self):
        if self._quantidade > 0:
            self._quantidade -= 1
            return True
        return False

    def __str__(self):
        return f"[{self._nome}] x{self._quantidade} - {self._descricao}"
