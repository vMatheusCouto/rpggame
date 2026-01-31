class Inventario:
    def __init__(self):
        self.itens = []
    # Converter tudo para o inglês. Português apenas visual (menus, botões, golpes, etc.)

    def adicionar(self, novo_item):
        for item in self.itens:
            if item.nome == novo_item.nome:
                item.quantidade += novo_item.quantidade
                print(f"Adicionado +{novo_item.quantidade} ao item {item.nome} existente.")
                return

        self.itens.append(novo_item)
        print(f"Item {novo_item.nome} adicionado ao inventário.")
    
    def listar(self):
        print("--- INVENTÁRIO ---")
        if not self.itens:
            print("Vazio.")
        for i, item in enumerate(self.itens):
            print(f"{i + 1}. {item}")
        print("------------------")
