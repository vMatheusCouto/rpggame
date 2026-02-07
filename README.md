# RPG Game

⚠️ Suporte PARCIAL ao Windows, pode ocorrer erro no carregamento de fontes, saves e ocasionar crash.

Um rpg de **top down** em pixel art (16x + 32x) construído através da biblioteca **pygame** e com base em conceitos de POO.

Assets desenvolvidos a partir de tiles, sprites e previews do pack **Pixel Crawler**, de _Anokolisa_.

## Funcionalidades

- Andar pelo mapa
- Colidir com paredes
- Atravessar mapas
- Correr
- Entrar em batalha
- Gerenciar vida
- Subir de nível
- Usar diferentes ataques com animações próprias

# Gerenciamento de tiles / criação de mapas
Ferramenta própria criada através do V0 para seleção de tiles e eventos (retorna um json com cada tile e o "type" dele)
> https://v0-grid-map-tool.vercel.app/

# Steps

Funcionamento garantido para o Python 3.13.11. 3.14.\* pode ocasionar problemas e impedir que o app inicie.

```
python3 -m venv .venv
source .venv/bin/activate # Considerar o terminal atual
pip install pygame
python -m src.main
```

# Estrutura

```bash
rpggame/
├── src/
│   ├── entities/ # Character, inimigos, inventário e moves
│   ├── scenarios/ # Gerenciamento de cenas e mapas
│   ├── utils/
│   ├── main.py # Container do loop
│   ├── frames.py # Definição do frame atual
│   ├── context.py # Valores globais
│   └── save.py
├── assets/
│   ├── battle/ # Backgrounds de batalha e hud de vida
│   ├── world/ # Todos os mapas, com background e toplayer
│   └── character/ # Sprites de todos os characters
├── saves/
│   ├── save_1.json # Criado dinamicamente
│   ├── save_2.json # Criado dinamicamente
│   └── save_3.json # Criado dinamicamente
├── README.md
└── package.json
```


