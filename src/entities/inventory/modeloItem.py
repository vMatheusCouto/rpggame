from src.entities.inventory.itens import CATALOGUE_ITEM
class Item:
    def __init__(self, type, name, description):
        self._type = type
        self._name = name
        self._description = description

    # Converter tudo para o inglês. Português apenas visual (menus, botões, golpes, etc.)
    def Crete(id_item):
        if id_item in CATALOGUE_ITEM:
            dados = CATALOGUE_ITEM[id_item]

            return Item(
                tipo=dados["type"],
                nome=dados["name"],
                descricao=dados["description"],

            )
        else:
            print(f"ERRO: O item '{id_item}' não existe no catálogo.")
            return None

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

   
    def usar(self):
        if self._quantidade > 0:
            self._quantidade -= 1
            return True
        return False

    def __str__(self):
        return f"[{self._name}]  - {self._description}"
class Potion(Item):
    super().__init__()