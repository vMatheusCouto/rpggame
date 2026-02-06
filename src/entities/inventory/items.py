from src.entities.inventory.catalogue import CATALOGUE_ITEM

class Item:
    def __init__(self, type, name, description,amount=1):
        self._type = type
        self._name = name
        self._description = description
        self._amount = amount

    @property

    @staticmethod
    def Create(id_item,amount=1):
        if id_item not in CATALOGUE_ITEM:
            print(f"Item {id_item} Não existe no catalogo, impossivel criar")
            return None
        data = CATALOGUE_ITEM[id_item]
        if data["type"]=="cura":
            return Potion(
                type=data["type"],
                name=data["display_name"],
                description=data["description"],
                amount=amount,
                heal_amount=data.get("heal_value", 0)
            )
        else:
            return Item(
                type=data["type"],
                name=data["display_name"],
                description=data["description"],
                amount=amount
            )
    @classmethod
    def loand_itens(cls):
        all_items= []
        for item_id, data in CATALOGUE_ITEM.items():
            new_item = Item.Creat(item_id,amount = 1)
            if new_item:
                all_items.append(new_item)
        return all_items


    def use(self):
        #apenas diminuir qtd
        if self.amount > 0:
            self.amount -= 1
            return True
        return False

    def __str__(self):
        return f"[{self._name}] - {self._description}"

class Potion(Item):
    def __init__(self,type,name,description,amount,heal_amount):
        super().__init__(type,name,description,amount)
        self.heal_amount = heal_amount
    def use(self, target):
        if super().use():
            target.hp += self.heal_amount
            print(f"Usou {self.name} e Recuperou {self.heal_amount} HP.")
            return True
        return False
