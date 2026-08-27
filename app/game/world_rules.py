import random


BASE_TRAVELS = 4
MYSTERY_TOWN_CHANCE = 0.08
RISKY_TRAVEL_AMBUSH_CHANCE = 0.35

ACADEMY_TOWN = "academy"
MYSTERY_TOWN = "veilcross"
STANDARD_TOWNS = (ACADEMY_TOWN, "highfield", "lunewater", "stonevein")

TOWNS = {
    ACADEMY_TOWN: {
        "name": "Arcana Academy",
        "region": "Academy Grounds",
        "description": "The Academy Square is the center of your adventure and the safest place to regain your bearings.",
        "places": [
            {"id": "healer", "name": "Healer", "description": "Restore your health before another dangerous outing."},
            {"id": "weapons", "name": "Weapon Shop", "description": "Buy stronger weapons and trade in your current blade."},
            {"id": "armor", "name": "Armor Shop", "description": "Upgrade your protection before entering the wilds."},
            {"id": "bank", "name": "Academy Bank", "description": "Protect gold from death and earn New Day interest."},
        ],
    },
    "highfield": {
        "name": "Highfield",
        "region": "The Open Plains",
        "description": "A broad human settlement surrounded by wheat, wagon roads, ranches, and endless grasslands.",
        "places": [
            {"id": "stable", "name": "Highfield Stable", "description": "Buy a mount that improves your daily travel range."},
            {"id": "bar", "name": "The Copper Cup", "description": "A noisy plains bar where travelers recover over food and ale."},
            {"id": "pawn", "name": "Pawn Shop", "description": "Sell equipped weapons or armor when you need quick gold."},
            {"id": "merchant", "name": "Plains Merchant", "description": "Buy provisions useful for another stretch of road."},
        ],
    },
    "lunewater": {
        "name": "Lunewater",
        "region": "The Silverwater Shore",
        "description": "An elven town of pale bridges, willow lanterns, and graceful buildings reflected in a vast blue lake.",
        "places": [
            {"id": "jeweler", "name": "Moonstone Jeweler", "description": "Purchase rare elven jewelry made from gems and silverglass."},
            {"id": "river_market", "name": "Moonwater Market", "description": "A quiet waterside market selling restorative elven goods."},
            {"id": "waterside_inn", "name": "The Willow Inn", "description": "Rest beside the water and recover from the road."},
            {"id": "alchemist", "name": "Silverleaf Alchemist", "description": "Buy a concentrated draught that restores Mana."},
        ],
    },
    "stonevein": {
        "name": "Stonevein",
        "region": "The Ironspine Mountains",
        "description": "A dwarven mountain town carved directly into black granite beneath smoking forge chimneys.",
        "places": [
            {"id": "rune_hall", "name": "Rune Hall", "description": "Train your arcane capacity and permanently increase maximum Mana."},
            {"id": "deep_forge", "name": "The Deep Forge", "description": "A mountain forge connected to Arcana's weapon and armor trade."},
            {"id": "gem_broker", "name": "Gem Broker", "description": "Sell raw gems to dwarven cutters for dependable gold."},
            {"id": "dwarf_bar", "name": "Stonebarrel Tavern", "description": "Strong food and stronger drink restore weary adventurers."},
        ],
    },
    MYSTERY_TOWN: {
        "name": "Veilcross",
        "region": "Somewhere Between Roads",
        "description": "A town that should not be here. Its lamps glow without flame, its streets never map the same way twice, and no road leads back once you leave.",
        "places": [
            {"id": "whispering_well", "name": "Whispering Well", "description": "Offer a gem to refill your Mana completely."},
            {"id": "curio_dealer", "name": "The Curio Dealer", "description": "Trade strange valuables with a merchant who never gives a name."},
            {"id": "lanternless_inn", "name": "The Lanternless Inn", "description": "A silent inn where wounds seem to close while nobody is looking."},
            {"id": "lost_stable", "name": "The Lost Stable", "description": "A rare stable offering a mount that seems to know roads that do not exist."},
        ],
    },
}

MOUNTS = {
    "": {"name": "No mount", "travel_bonus": 0},
    "plains_courser": {"name": "Plains Courser", "travel_bonus": 1},
    "mistwalker": {"name": "Mistwalker", "travel_bonus": 2},
}

JEWELRY = {
    "": {"name": "No jewelry", "gem_bonus": 0.0},
    "moonwater_pendant": {"name": "Moonwater Pendant", "gem_bonus": 0.02},
}


def town_info(town_id):
    return TOWNS.get(town_id, TOWNS[ACADEMY_TOWN])


def town_places(town_id):
    return list(town_info(town_id)["places"])


def direct_destinations(current_town):
    return [
        {"id": town_id, **TOWNS[town_id]}
        for town_id in STANDARD_TOWNS
        if town_id != current_town
    ]


def mount_info(mount_id):
    return MOUNTS.get(mount_id or "", MOUNTS[""])


def jewelry_info(jewelry_id):
    return JEWELRY.get(jewelry_id or "", JEWELRY[""])


def travels_per_day(mount_id=""):
    return BASE_TRAVELS + mount_info(mount_id)["travel_bonus"]


def wander_destination(current_town, rng=None):
    rng = rng or random
    if rng.random() < MYSTERY_TOWN_CHANCE:
        return MYSTERY_TOWN
    choices = [town_id for town_id in STANDARD_TOWNS if town_id != current_town]
    return rng.choice(choices or list(STANDARD_TOWNS))


def risky_travel_ambush(rng=None):
    rng = rng or random
    return rng.random() < RISKY_TRAVEL_AMBUSH_CHANCE


def build_travel_enemy(player_level, rng=None):
    rng = rng or random
    level = max(1, int(player_level))
    names = ["Roadside Marauder", "Highway Cutthroat", "Wandering Brigand", "Masked Road Raider"]
    hp = 10 + level * 6 + rng.randint(0, 4)
    return {
        "id": f"travel-{level}",
        "name": rng.choice(names),
        "level": level,
        "hp": hp,
        "max_hp": hp,
        "attack": 2 + level * 2,
        "defense": max(0, level - 1),
        "gold": (max(2, level * 4), max(4, level * 8)),
        "xp": (max(3, level * 6), max(5, level * 10)),
        "hunt_mode": "travel",
        "kind": "travel",
    }
