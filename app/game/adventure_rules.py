import random
from typing import Tuple

VALID_ACTIONS = {"attack", "spell", "defend", "run"}

INTENT_STRIKE = "strike"
INTENT_HEAVY = "heavy"
INTENT_GUARD = "guard"

INTENT_MESSAGES = {
    INTENT_STRIKE: "is preparing a quick strike.",
    INTENT_HEAVY: "is winding up a crushing attack.",
    INTENT_GUARD: "raises its guard and braces for impact.",
}


def roll_monster_intent(rng=random) -> str:
    """Return a weighted, telegraphed monster action for the next exchange."""
    roll = rng.random()
    if roll < 0.55:
        return INTENT_STRIKE
    if roll < 0.80:
        return INTENT_HEAVY
    return INTENT_GUARD


def intent_message(monster_name: str, intent: str) -> str:
    return f"{monster_name} {INTENT_MESSAGES.get(intent, INTENT_MESSAGES[INTENT_STRIKE])}"


def calculate_player_damage(
    attack: int,
    monster_defense: int,
    action: str,
    monster_intent: str,
    rng=random,
) -> Tuple[int, bool]:
    """Resolve player damage and whether a physical attack critically hit."""
    if action == "defend":
        return 0, False

    variance = rng.randint(0, 2)

    if action == "spell":
        # Spells are the answer to guarding enemies: stronger, partially armor-piercing,
        # and unaffected by the guard intent, but controlled by a cooldown in the route.
        effective_defense = max(0, monster_defense // 2)
        damage = max(1, round(attack * 1.5) - effective_defense + variance)
        return damage, False

    damage = max(1, attack - monster_defense + variance)
    critical = rng.random() < 0.15
    if critical:
        damage *= 2

    if monster_intent == INTENT_GUARD:
        damage = max(1, damage // 2)

    return damage, critical


def calculate_monster_damage(
    monster_attack: int,
    player_defense: int,
    monster_intent: str,
    defending: bool,
    rng=random,
) -> int:
    """Resolve the telegraphed monster action against the player's response."""
    if monster_intent == INTENT_GUARD:
        return 0

    multiplier = 1.6 if monster_intent == INTENT_HEAVY else 1.0
    damage = max(
        1,
        round(monster_attack * multiplier) - player_defense + rng.randint(0, 2),
    )

    if defending:
        # Defend sacrifices outgoing damage to heavily blunt the incoming hit.
        damage = max(1, damage // 3)

    return damage


def training_cost(level: int) -> int:
    """Keep permanent stat growth useful without letting a flat price trivialize late game."""
    return 20 + max(0, level - 1) * 5


def defeat_gold_loss(gold: int) -> int:
    """Lose 10% of carried gold on defeat, with a small early-game floor."""
    if gold <= 0:
        return 0
    return min(gold, max(5, int(gold * 0.10)))


def is_dragon_boss(monster_id: str) -> bool:
    return monster_id in {"dragon", "abyssal_dragon"}
