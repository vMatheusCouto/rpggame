from src.entities.inventory.itens import Item


class Inventory:
    def __init__(self,auto_loand=False):
        self.itens = {}
        if auto_loand:
            lista_temp = Item.loand_itens()
            for Item in lista_temp:
                self.add()
            
                        
    def add(self, new_item):
        tipo = new_item.type
        
        
        if tipo not in self.itens:
            self.itens[tipo] = []
            
        lista_categoria = self.itens[tipo]
        for item in lista_categoria:
            if item.name == new_item.name:
                item.amount += new_item.amount
                print(f"Adicionado +{new_item.amount} ao item {item.name} existente.")
                return
        lista_categoria.append(new_item)
        
        print(f"Item {new_item.name} adicionado ao inventory.") 
    def transform_list(self):
        lista_plana = []
        for categoria in self.itens.values():
            lista_plana.extend(categoria)
        return  lista_plana
    def liste(self):
            if not self.itens:
                print("Vazio.")
                return
            
            for categoria, lista_itens in self.itens.items():
                print(f"--{categoria.upper()}--")
                for Item in lista_itens:
                    print(f"    {Item}")