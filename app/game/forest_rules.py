import random
from datetime import datetime, timezone


GAME_DAY_SECONDS = 6 * 60 * 60  # four Arcana game days per real day
BASE_FOREST_FIGHTS = 10
BASE_SPECIALTY_USES = 5
BANK_INTEREST_RATE = 0.05
MAX_LEVEL = 15


FOREST_CREATURES = {
    1: ["Thorn Hare", "Cellar Rat", "Moss Imp"],
    2: ["Goblin Scout", "Mire Spider", "Wild Hound"],
    3: ["Bandit Initiate", "Briar Wolf", "Cave Slime"],
    4: ["Orc Forager", "Grave Bat", "Rootling"],
    5: ["Forest Brigand", "Dire Boar", "Ash Skeleton"],
    6: ["Bog Hag", "Stoneback Bear", "Moon Wraith"],
    7: ["Orc Reaver", "Venom Drake", "Hollow Knight"],
    8: ["Crypt Warden", "Young Treant", "Bloodfang Wolf"],
    9: ["Runed Golem", "Night Stalker", "Warlock Adept"],
    10: ["Wyvern", "Ogre Champion", "Spectral Knight"],
    11: ["Dread Minotaur", "Frost Troll", "Abyss Hound"],
    12: ["Storm Elemental", "Bone Colossus", "Dark Enchanter"],
    13: ["Ancient Treant", "Demon Knight", "Crystal Hydra"],
    14: ["Void Reaver", "Dragon Priest", "Titan Construct"],
    15: ["Elder Drake", "Arcane Behemoth", "Emerald Wyrm"],
}


MASTER_NAMES = {
    1: "Master Elowen",
    2: "Master Brann",
    3: "Master Caelis",
    4: "Master Dorian",
    5: "Master Eira",
    6: "Master Fenric",
    7: "Master Galen",
    8: "Master Hestia",
    9: "Master Ilyra",
    10: "Master Joren",
    11: "Master Kael",
    12: "Master Lyra",
    13: "Master Merek",
    14: "Archmaster Nyx",
}


WEAPONS = [
    {"name": "Practice Blade", "power": 0, "cost": 0},
    {"name": "Iron Shortsword", "power": 2, "cost": 45},
    {"name": "Tempered Saber", "power": 4, "cost": 95},
    {"name": "Runed Longsword", "power": 6, "cost": 170},
    {"name": "Moonsteel Blade", "power": 8, "cost": 275},
    {"name": "Emberbrand", "power": 10, "cost": 420},
    {"name": "Storm Saber", "power": 12, "cost": 620},
    {"name": "Griffin Talon", "power": 14, "cost": 875},
    {"name": "Spellforged Claymore", "power": 16, "cost": 1180},
    {"name": "Wyrmfang", "power": 18, "cost": 1540},
    {"name": "Voidsteel Edge", "power": 20, "cost": 1960},
    {"name": "Astral Greatsword", "power": 22, "cost": 2450},
    {"name": "Titanbreaker", "power": 24, "cost": 3010},
    {"name": "Starforged Blade", "power": 26, "cost": 3640},
    {"name": "Archmage's Edge", "power": 28, "cost": 4350},
    {"name": "Dragonbane", "power": 31, "cost": 5150},
]


ARMORS = [
    {"name": "Academy Robes", "power": 0, "cost": 0},
    {"name": "Leather Jerkin", "power": 1, "cost": 45},
    {"name": "Studded Leather", "power": 2, "cost": 95},
    {"name": "Iron Mail", "power": 3, "cost": 170},
    {"name": "Runed Mail", "power": 4, "cost": 275},
    {"name": "Moonsteel Mail", "power": 5, "cost": 420},
    {"name": "Ember Plate", "power": 6, "cost": 620},
    {"name": "Griffin Guard", "power": 7, "cost": 875},
    {"name": "Spellforged Plate", "power": 8, "cost": 1180},
    {"name": "Wyrmscale", "power": 9, "cost": 1540},
    {"name": "Voidsteel Plate", "power": 10, "cost": 1960},
    {"name": "Astral Armor", "power": 11, "cost": 2450},
    {"name": "Titan Aegis", "power": 12, "cost": 3010},
    {"name": "Starforged Plate", "power": 13, "cost": 3640},
    {"name": "Archmage's Aegis", "power": 14, "cost": 4350},
    {"name": "Dragonscale Aegis", "power": 16, "cost": 5150},
]


TITLES = [
    (0, "Academy Initiate"),
    (1, "Dragon Slayer"),
    (3, "Arcane Knight"),
    (5, "Wyrm Hunter"),
    (10, "Champion of Arcana"),
    (20, "Legend of Arcana"),
    (50, "Mythic Dragonlord"),
]


def game_day_key(now=None):
    moment = now or datetime.now(timezone.utc)
    return int(moment.timestamp() // GAME_DAY_SECONDS)


def xp_required(level):
    return max(50, int(level) * 50)


def forest_fights_per_day(dragon_fights=0):
    return BASE_FOREST_FIGHTS + max(0, int(dragon_fights))


def title_for_dragon_kills(dragon_kills):
    title = TITLES[0][1]
    for required, candidate in TITLES:
        if dragon_kills >= required:
            title = candidate
    return title


def weapon_for_tier(tier):
    return WEAPONS[max(0, min(int(tier), len(WEAPONS) - 1))]


def armor_for_tier(tier):
    return ARMORS[max(0, min(int(tier), len(ARMORS) - 1))]


def purchase_price(catalog, current_tier, new_tier):
    current_tier = max(0, min(int(current_tier), len(catalog) - 1))
    new_tier = max(0, min(int(new_tier), len(catalog) - 1))
    if new_tier <= current_tier:
        return None
    trade_in = catalog[current_tier]["cost"] // 2
    return max(0, catalog[new_tier]["cost"] - trade_in)


def effective_attack(base_attack, weapon_tier):
    return max(1, int(base_attack) + weapon_for_tier(weapon_tier)["power"])


def effective_defense(base_defense, armor_tier):
    return max(0, int(base_defense) + armor_for_tier(armor_tier)["power"])


def healing_cost(current_hp, max_hp, level):
    missing = max(0, int(max_hp) - int(current_hp))
    return missing * max(1, int(level))


def xp_after_death(xp):
    return max(0, int(int(xp) * 0.90))


def build_forest_creature(player_level, hunt_mode="normal", rng=None):
    rng = rng or random
    player_level = max(1, min(int(player_level), MAX_LEVEL))
    offset = {"slum": -1, "normal": 0, "thrill": 1}.get(hunt_mode, 0)
    creature_level = max(1, min(player_level + offset, MAX_LEVEL))
    name = rng.choice(FOREST_CREATURES[creature_level])

    reward_mult = 0.8 if hunt_mode == "slum" else 1.25 if hunt_mode == "thrill" else 1.0
    hp = 7 + creature_level * 6 + rng.randint(0, 4)
    attack = 1 + creature_level * 2
    defense = max(0, creature_level - 1)
    gold_low = max(1, int(creature_level * 5 * reward_mult))
    gold_high = max(gold_low, int(creature_level * 9 * reward_mult))
    xp_low = max(1, int(creature_level * 8 * reward_mult))
    xp_high = max(xp_low, int(creature_level * 13 * reward_mult))

    return {
        "id": f"forest-{creature_level}-{name.lower().replace(' ', '-')}",
        "name": name,
        "level": creature_level,
        "hp": hp,
        "max_hp": hp,
        "attack": attack,
        "defense": defense,
        "gold": (gold_low, gold_high),
        "xp": (xp_low, xp_high),
        "hunt_mode": hunt_mode,
        "kind": "forest",
    }


def build_master(player_level):
    player_level = max(1, min(int(player_level), MAX_LEVEL - 1))
    target_level = player_level + 1
    hp = 18 + target_level * 8
    return {
        "id": f"master-{player_level}",
        "name": MASTER_NAMES[player_level],
        "level": target_level,
        "hp": hp,
        "max_hp": hp,
        "attack": 3 + target_level * 2,
        "defense": target_level,
        "gold": (0, 0),
        "xp": (0, 0),
        "kind": "master",
    }


def build_dragon(dragon_kills=0):
    scaling = min(max(0, int(dragon_kills)), 25)
    hp = 180 + scaling * 5
    return {
        "id": "emerald-archdragon",
        "name": "Emerald Archdragon",
        "level": MAX_LEVEL + 2,
        "hp": hp,
        "max_hp": hp,
        "attack": 34 + scaling,
        "defense": 18 + scaling // 3,
        "gold": (0, 0),
        "xp": (0, 0),
        "kind": "dragon",
    }


def roll_player_damage(base_attack, weapon_tier, target_defense, rng=None):
    rng = rng or random
    raw = effective_attack(base_attack, weapon_tier) + rng.randint(0, 3)
    return max(1, raw - int(target_defense))


def roll_enemy_damage(enemy_attack, base_defense, armor_tier, rng=None):
    rng = rng or random
    raw = int(enemy_attack) + rng.randint(0, 2)
    return max(1, raw - effective_defense(base_defense, armor_tier))


def dragon_reset_stats(dragon_attack=0, dragon_defense=0, dragon_hp=0):
    return {
        "level": 1,
        "xp": 0,
        "hp": 20 + max(0, int(dragon_hp)) * 5,
        "max_hp": 20 + max(0, int(dragon_hp)) * 5,
        "attack": 5 + max(0, int(dragon_attack)),
        "defense": 2 + max(0, int(dragon_defense)),
        "weapon_level": 0,
        "armor_level": 0,
    }
