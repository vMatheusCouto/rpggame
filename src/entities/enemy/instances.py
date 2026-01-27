from src.entities.enemy.enemies import Enemy
Orc = Enemy(
    name="orc",
    hp=80,
    damage=10,
    drop_xp=15,
    path="orc"
)

Skeleton = Enemy(
    name="skeleton",
    hp=100,
    damage=12,
    drop_xp=20,
    path="skeleton"
)

OrcRogue = Enemy(
    name="orc_rogue",
    hp=120,
    damage=16,
    drop_xp=30,
    path="orc_rogue"
)

SkeletonRogue = Enemy(
    name="skeleton_rogue",
    hp=140,
    damage=18,
    drop_xp=40,
    path="skeleton_rogue"
)

OrcWarrior = Enemy(
    name="orc_warrior",
    hp=170,
    damage=22,
    drop_xp=55,
    path="orc_warrior"
)

SkeletonWarrior = Enemy(
    name="skeleton_warrior",
    hp=200,
    damage=25,
    drop_xp=70,
    path="skeleton_warrior"
)

OrcShaman = Enemy(
    name="orc_shaman",
    hp=230,
    damage=30,
    drop_xp=90,
    path="orc_shaman"
)

SkeletonMage = Enemy(
    name="skeleton_mage",
    hp=260,
    damage=35,
    drop_xp=120,
    path="skeleton_mage"
)
