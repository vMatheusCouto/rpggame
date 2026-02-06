from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJECT_ROOT / "src"
SAVES_DIR = PROJECT_ROOT / "saves"

ASSETS_DIR = PROJECT_ROOT / "assets"
CHARACTER_ASSETS = ASSETS_DIR / "character"
WORLD_ASSETS = ASSETS_DIR / "world"
BATTLE_ASSETS =  ASSETS_DIR / "battle"
SOUNDS_DIR = ASSETS_DIR / "sound"
