import random
import unittest

from app.game.world_rules import (
    ACADEMY_TOWN,
    MYSTERY_TOWN,
    STANDARD_TOWNS,
    build_travel_enemy,
    direct_destinations,
    jewelry_info,
    town_places,
    travels_per_day,
    wander_destination,
)


class FixedMysteryRng:
    def random(self):
        return 0.0

    def choice(self, values):
        return values[0]


class WorldTravelRulesTests(unittest.TestCase):
    def test_base_safe_travels_follow_logd_style_daily_allowance(self):
        self.assertEqual(travels_per_day(""), 4)
        self.assertEqual(travels_per_day("plains_courser"), 5)
        self.assertEqual(travels_per_day("mistwalker"), 6)

    def test_direct_travel_never_lists_mystery_town(self):
        destinations = direct_destinations(ACADEMY_TOWN)
        destination_ids = {destination["id"] for destination in destinations}
        self.assertNotIn(MYSTERY_TOWN, destination_ids)
        self.assertEqual(destination_ids, set(STANDARD_TOWNS) - {ACADEMY_TOWN})

    def test_aimless_wandering_can_reveal_veilcross(self):
        self.assertEqual(wander_destination(ACADEMY_TOWN, FixedMysteryRng()), MYSTERY_TOWN)

    def test_each_standard_town_has_local_places(self):
        for town_id in STANDARD_TOWNS:
            with self.subTest(town=town_id):
                self.assertGreaterEqual(len(town_places(town_id)), 4)

    def test_highfield_contains_stable_and_bar(self):
        place_ids = {place["id"] for place in town_places("highfield")}
        self.assertIn("stable", place_ids)
        self.assertIn("bar", place_ids)
        self.assertIn("pawn", place_ids)
        self.assertIn("merchant", place_ids)

    def test_lunewater_contains_jeweler(self):
        place_ids = {place["id"] for place in town_places("lunewater")}
        self.assertIn("jeweler", place_ids)

    def test_stonevein_contains_mana_rune_hall(self):
        place_ids = {place["id"] for place in town_places("stonevein")}
        self.assertIn("rune_hall", place_ids)

    def test_mystery_town_has_unique_services(self):
        place_ids = {place["id"] for place in town_places(MYSTERY_TOWN)}
        self.assertIn("whispering_well", place_ids)
        self.assertIn("lost_stable", place_ids)

    def test_moonwater_pendant_adds_gem_find_bonus(self):
        self.assertGreater(jewelry_info("moonwater_pendant")["gem_bonus"], 0)

    def test_travel_enemy_is_a_travel_encounter(self):
        enemy = build_travel_enemy(5, random.Random(1))
        self.assertEqual(enemy["kind"], "travel")
        self.assertEqual(enemy["level"], 5)
        self.assertGreater(enemy["hp"], 0)


if __name__ == "__main__":
    unittest.main()
