from src.entities.inventory.modeloItem import Item

CATALOGO_ITENS = {
    "Small_Potion": {
        "type": "cura",
        "name": "Poção Pequena",
        "description": "Recupera 50 HP"
    },
    "Medium_Potion": {
        "type": "cura",
        "name": "Poção Media",
        "description": "Recupera 150 HP"
    },
    "Big_Potion": {
        "type": "cura",
        "name": "Poção Grande",
        "description": "recupera 350 hp"
    }
}

def criar_item_por_id(id_item, quantidade=1):
    if id_item in CATALOGO_ITENS:
        dados = CATALOGO_ITENS[id_item]

        return Item(
            tipo=dados["type"],
            nome=dados["name"],
            descricao=dados["description"],
            quantidade=quantidade
        )
    else:
        print(f"ERRO: O item '{id_item}' não existe no catálogo.")
        return None
