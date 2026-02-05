from src.entities.inventory.itens import Item

CATALOGUE_ITEM = {
    "Small_Potion": {
        "type": "cura",
        "name": "Small Potion", #id
        "display_name": "Poção Pequena",#nome que deve ser exibido 
        "description": "Recupera 60 HP",
        "heal_value": 60  #valor de cura para funcionar no metodo heal
    },
    "Medium_Potion": {
        "type": "cura",
        "name": "Medium Potion",
        "display_name": "Poção Média",
        "description": "Recupera 150 HP",
        "heal_value": 150
    },
    "Big_Potion": {
        "type": "cura",
        "name": "Big Potion",
        "display_name": "Poção Grande",
        "description": "Recupera 350 HP",
        "heal_value": 350
    }
}