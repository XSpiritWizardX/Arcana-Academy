import random
import unittest
from datetime import datetime, timezone

from app.game.forest_rules import (
    ARMORS,
    BASE_MANA,
    BASIC_SPECIAL_COST,
    WEAPONS,
    armor_for_tier,
    build_dragon,
    build_forest_creature,
    build_master,
    dragon_reset_stats,
    effective_attack,
    effective_defense,
    forest_fights_per_day,
    game_day_key,
    healing_cost,
    purchase_price,
    roll_player_damage,
    roll_special_damage,
    title_for_dragon_kills,
    weapon_for_tier,
    xp_after_death,
    xp_required,
)


class ForestProgressionRulesTests(unittest.TestCase):
    def test_game_day_changes_every_six_hours(self):
        first = datetime(2026, 8, 27, 0, 0, tzinfo=timezone.utc)
        same_day = datetime(2026, 8, 27, 5, 59, tzinfo=timezone.utc)
        next_day = datetime(2026, 8, 27, 6, 0, tzinfo=timezone.utc)
        self.assertEqual(game_day_key(first), game_day_key(same_day))
        self.assertEqual(game_day_key(first) + 1, game_day_key(next_day))

    def test_xp_threshold_scales_by_level(self):
        self.assertEqual(xp_required(1), 50)
        self.assertEqual(xp_required(7), 350)
        self.assertEqual(xp_required(15), 750)

    def test_dragon_fight_point_adds_daily_forest_fight(self):
        self.assertEqual(forest_fights_per_day(0), 10)
        self.assertEqual(forest_fights_per_day(4), 14)

    def test_thrillseeking_generates_higher_level_creature(self):
        creature = build_forest_creature(5, "thrill", random.Random(1))
        self.assertEqual(creature["level"], 6)
        self.assertEqual(creature["hunt_mode"], "thrill")

    def test_slumming_never_drops_below_level_one(self):
        creature = build_forest_creature(1, "slum", random.Random(1))
        self.assertEqual(creature["level"], 1)

    def test_master_advances_target_level(self):
        master = build_master(8)
        self.assertEqual(master["kind"], "master")
        self.assertEqual(master["level"], 9)

    def test_dragon_scales_with_prior_kills(self):
        first = build_dragon(0)
        veteran = build_dragon(10)
        self.assertGreater(veteran["hp"], first["hp"])
        self.assertGreater(veteran["attack"], first["attack"])

    def test_death_loses_ten_percent_xp(self):
        self.assertEqual(xp_after_death(1000), 900)
        self.assertEqual(xp_after_death(3), 2)

    def test_healer_cost_scales_with_missing_hp_and_level(self):
        self.assertEqual(healing_cost(15, 20, 1), 5)
        self.assertEqual(healing_cost(15, 20, 5), 25)

    def test_shop_upgrade_uses_trade_in_value(self):
        expected = WEAPONS[2]["cost"] - WEAPONS[1]["cost"] // 2
        self.assertEqual(purchase_price(WEAPONS, 1, 2), expected)
        self.assertIsNone(purchase_price(ARMORS, 3, 2))

    def test_equipment_tiers_affect_combat_stats(self):
        self.assertEqual(effective_attack(5, 0), 5)
        self.assertEqual(effective_attack(5, 3), 5 + weapon_for_tier(3)["power"])
        self.assertEqual(effective_defense(2, 4), 2 + armor_for_tier(4)["power"])

    def test_starter_mana_and_special_cost(self):
        self.assertEqual(BASE_MANA, 10)
        self.assertEqual(BASIC_SPECIAL_COST, 5)

    def test_arcane_strike_doubles_one_round_damage(self):
        normal_rng = random.Random(7)
        special_rng = random.Random(7)
        normal = roll_player_damage(8, 2, 4, normal_rng)
        special = roll_special_damage(8, 2, 4, special_rng)
        self.assertEqual(special, normal * 2)

    def test_dragon_titles_are_persistent_progression(self):
        self.assertEqual(title_for_dragon_kills(0), "Academy Initiate")
        self.assertEqual(title_for_dragon_kills(1), "Dragon Slayer")
        self.assertEqual(title_for_dragon_kills(50), "Mythic Dragonlord")

    def test_dragon_reset_keeps_allocated_permanent_stats(self):
        reset = dragon_reset_stats(dragon_attack=2, dragon_defense=3, dragon_hp=4)
        self.assertEqual(reset["level"], 1)
        self.assertEqual(reset["attack"], 7)
        self.assertEqual(reset["defense"], 5)
        self.assertEqual(reset["max_hp"], 40)
        self.assertEqual(reset["weapon_level"], 0)
        self.assertEqual(reset["armor_level"], 0)


if __name__ == "__main__":
    unittest.main()
