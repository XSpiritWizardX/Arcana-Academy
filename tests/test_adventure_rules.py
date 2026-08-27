import unittest

from app.game.adventure_rules import (
    INTENT_GUARD,
    INTENT_HEAVY,
    INTENT_STRIKE,
    calculate_monster_damage,
    calculate_player_damage,
    defeat_gold_loss,
    is_dragon_boss,
    roll_monster_intent,
    training_cost,
)


class FixedRandom:
    def __init__(self, random_values=None, randint_values=None):
        self.random_values = list(random_values or [0.99])
        self.randint_values = list(randint_values or [0])

    def random(self):
        return self.random_values.pop(0)

    def randint(self, _low, _high):
        return self.randint_values.pop(0)


class AdventureIntentTests(unittest.TestCase):
    def test_intent_weights_cover_strike_heavy_and_guard(self):
        self.assertEqual(roll_monster_intent(FixedRandom([0.10])), INTENT_STRIKE)
        self.assertEqual(roll_monster_intent(FixedRandom([0.60])), INTENT_HEAVY)
        self.assertEqual(roll_monster_intent(FixedRandom([0.90])), INTENT_GUARD)


class AdventureDamageTests(unittest.TestCase):
    def test_physical_attack_can_crit(self):
        damage, critical = calculate_player_damage(
            attack=10,
            monster_defense=2,
            action="attack",
            monster_intent=INTENT_STRIKE,
            rng=FixedRandom(random_values=[0.05], randint_values=[0]),
        )
        self.assertTrue(critical)
        self.assertEqual(damage, 16)

    def test_guard_reduces_physical_attack(self):
        damage, critical = calculate_player_damage(
            attack=10,
            monster_defense=2,
            action="attack",
            monster_intent=INTENT_GUARD,
            rng=FixedRandom(random_values=[0.90], randint_values=[0]),
        )
        self.assertFalse(critical)
        self.assertEqual(damage, 4)

    def test_spell_pierces_half_defense_and_ignores_guard(self):
        damage, critical = calculate_player_damage(
            attack=10,
            monster_defense=6,
            action="spell",
            monster_intent=INTENT_GUARD,
            rng=FixedRandom(randint_values=[0]),
        )
        self.assertFalse(critical)
        self.assertEqual(damage, 12)

    def test_defend_sacrifices_player_damage(self):
        damage, critical = calculate_player_damage(
            attack=10,
            monster_defense=2,
            action="defend",
            monster_intent=INTENT_HEAVY,
            rng=FixedRandom(),
        )
        self.assertEqual(damage, 0)
        self.assertFalse(critical)

    def test_defend_strongly_reduces_heavy_attack(self):
        undefended = calculate_monster_damage(
            monster_attack=12,
            player_defense=3,
            monster_intent=INTENT_HEAVY,
            defending=False,
            rng=FixedRandom(randint_values=[0]),
        )
        defended = calculate_monster_damage(
            monster_attack=12,
            player_defense=3,
            monster_intent=INTENT_HEAVY,
            defending=True,
            rng=FixedRandom(randint_values=[0]),
        )
        self.assertEqual(undefended, 16)
        self.assertEqual(defended, 5)

    def test_guarding_monster_does_not_attack(self):
        damage = calculate_monster_damage(
            monster_attack=12,
            player_defense=3,
            monster_intent=INTENT_GUARD,
            defending=False,
            rng=FixedRandom(),
        )
        self.assertEqual(damage, 0)


class AdventureProgressionTests(unittest.TestCase):
    def test_training_cost_scales_with_level(self):
        self.assertEqual(training_cost(1), 20)
        self.assertEqual(training_cost(10), 65)

    def test_defeat_loss_scales_but_never_exceeds_carried_gold(self):
        self.assertEqual(defeat_gold_loss(0), 0)
        self.assertEqual(defeat_gold_loss(3), 3)
        self.assertEqual(defeat_gold_loss(40), 5)
        self.assertEqual(defeat_gold_loss(500), 50)

    def test_dragon_boss_tracking_excludes_dragonling(self):
        self.assertTrue(is_dragon_boss("dragon"))
        self.assertTrue(is_dragon_boss("abyssal_dragon"))
        self.assertFalse(is_dragon_boss("dragonling"))


if __name__ == "__main__":
    unittest.main()
