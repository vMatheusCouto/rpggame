from src.entities.inventory.modeloItem import Item
# Converter em JSON
CATALOGO_ITENS = {
    "Small_Potion": {
        "type": "cura",
        "name": "Poção Pequena",
        "description": "Recupera 20 HP"
    },
    "Medium_Potion": {
        "type": "cura",
        "name": "Poção Grande",
        "description": "Recupera 60 HP"
    },
    "Big_Potion": {
        "type": "cura",
        "name": "Pocao Grande",
        "description": "recupera 150 hp"
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
