import unittest

from app.game.engine import GameService, build_demo_map, distance, state_to_dict


class GameMapTests(unittest.TestCase):
    def test_demo_map_has_blocking_border_and_walkable_interior(self):
        game_map = build_demo_map()
        self.assertFalse(game_map.walkable((0, 0)))
        self.assertFalse(game_map.walkable((9, 9)))
        self.assertTrue(game_map.walkable((1, 1)))
        self.assertFalse(game_map.walkable((3, 4)))

    def test_manhattan_distance(self):
        self.assertEqual(distance((1, 2), (4, 6)), 7)


class GameServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = GameService()
        self.state = self.service.create_session(user_id=42)

    def test_sessions_are_scoped_to_owning_user(self):
        self.assertIs(self.service.get_session(self.state.id, 42), self.state)
        self.assertIsNone(self.service.get_session(self.state.id, 99))

    def test_blocked_move_does_not_spend_action_point(self):
        player = self.state.entities["player"]
        before = player.action_points
        error = self.service.move(self.state, "player", "left")
        self.assertEqual(error, "Blocked")
        self.assertEqual(player.position, (1, 5))
        self.assertEqual(player.action_points, before)

    def test_attack_applies_damage_and_spends_action_point(self):
        player = self.state.entities["player"]
        goblin = self.state.entities["goblin"]
        error = self.service.attack(self.state, "player", "goblin")
        self.assertIsNone(error)
        self.assertEqual(goblin.hp, 5)
        self.assertEqual(player.action_points, 1)

    def test_turn_advance_refreshes_next_entity_action_points(self):
        goblin = self.state.entities["goblin"]
        goblin.action_points = 0
        self.service.end_turn(self.state)
        self.assertEqual(self.state.current_entity().id, "goblin")
        self.assertEqual(goblin.action_points, 2)

    def test_serialization_exposes_client_contract(self):
        payload = state_to_dict(self.state)
        self.assertEqual(payload["session_id"], self.state.id)
        self.assertEqual(payload["map"]["width"], 10)
        self.assertEqual(payload["current_turn"], "player")
        self.assertEqual({entity["id"] for entity in payload["entities"]}, {"player", "goblin"})


if __name__ == "__main__":
    unittest.main()
