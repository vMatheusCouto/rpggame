from src.entities.inventoryPlayer.modeloItem import Item
# Converter em JSON
CATALOGO_ITENS = {
    "Small_Potion": {
        "type": "cura",
        "name": "Poção Pequena",
        "description": "Recupera 20 HP"
    },
    "Big_Potion": {
        "type": "cura",
        "name": "Poção Grande",
        "description": "Recupera 60 HP"
    },
    "sword_Iron": {
        "type": "arma",
        "name": "Espada simples de ferro",
        "description": "aumenta em +10 o ataque"
    },
    "Iron_Axe":{
        "type": "arma",
        "name": "Machado de ferro",     
        "description": "aumenta em +15 o ataque"
    },
    "Iron_Armor": { 
        "type": "Armor",
        "name": "Armadura de ferro",
        "description": "Adiciona +5 de def ao personagem"
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
