from .modeloItem import Item 

CATALOGO_ITENS = {
    "Small_Potion": {
        "tipo": "cura",
        "nome": "Poção Pequena",
        "descricao": "Recupera 20 HP"
    },
    "Big_Potion": {
        "tipo": "cura",
        "nome": "Poção Grande",
        "descricao": "Recupera 60 HP"
    },
    "espada_Ferro": {
        "tipo": "arma",
        "nome": "Espada simples de ferro",
        "descricao": "Ataque +10"
    }
}

def criar_item_por_id(id_item, quantidade=1):
    if id_item in CATALOGO_ITENS: 
        dados = CATALOGO_ITENS[id_item]
         
        return Item(
            tipo=dados["tipo"],
            nome=dados["nome"],
            descricao=dados["descricao"],
            quantidade=quantidade
        )
    else:
        print(f"ERRO: O item '{id_item}' não existe no catálogo.")
        return None