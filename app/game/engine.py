import random
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

GridPos = Tuple[int, int]


@dataclass
class Entity:
    id: str
    name: str
    hp: int
    attack: int
    range: int
    position: GridPos
    is_player: bool = False
    action_points: int = 2

    def alive(self) -> bool:
        return self.hp > 0


@dataclass
class GameMap:
    width: int
    height: int
    tiles: List[List[str]]  # "floor" or "wall"

    def in_bounds(self, pos: GridPos) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, pos: GridPos) -> bool:
        if not self.in_bounds(pos):
            return False
        x, y = pos
        return self.tiles[y][x] == "floor"


@dataclass
class GameState:
    id: str
    user_id: int
    game_map: GameMap
    entities: Dict[str, Entity]
    turn_order: List[str]
    current_turn_index: int = 0

    def current_entity(self) -> Entity:
        return self.entities[self.turn_order[self.current_turn_index]]

    def advance_turn(self) -> None:
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        # refresh AP at start of turn
        self.current_entity().action_points = 2

    def living_entities(self) -> List[Entity]:
        return [e for e in self.entities.values() if e.alive()]


def build_demo_map() -> GameMap:
    width, height = 10, 10
    tiles = [["floor" for _ in range(width)] for _ in range(height)]
    # add a border of walls
    for x in range(width):
        tiles[0][x] = "wall"
        tiles[height - 1][x] = "wall"
    for y in range(height):
        tiles[y][0] = "wall"
        tiles[y][width - 1] = "wall"
    # interior obstacles
    for x in range(3, 7):
        tiles[4][x] = "wall"
    return GameMap(width=width, height=height, tiles=tiles)


def distance(a: GridPos, b: GridPos) -> int:
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


class GameService:
    """
    Simple in-memory turn-based engine.
    """

    def __init__(self):
        self.sessions: Dict[str, GameState] = {}

    def create_session(self, user_id: int) -> GameState:
        game_map = build_demo_map()

        player = Entity(
            id="player",
            name="You",
            hp=20,
            attack=5,
            range=10,
            position=(1, 5),
            is_player=True,
        )
        goblin = Entity(
            id="goblin",
            name="Goblin",
            hp=10,
            attack=3,
            range=10,
            position=(8, 5),
            is_player=False,
        )

        entities = {player.id: player, goblin.id: goblin}
        turn_order = [player.id, goblin.id]

        session_id = str(uuid.uuid4())
        state = GameState(
            id=session_id,
            user_id=user_id,
            game_map=game_map,
            entities=entities,
            turn_order=turn_order,
            current_turn_index=0,
        )
        self.sessions[session_id] = state
        return state

    def get_session(self, session_id: str, user_id: int) -> Optional[GameState]:
        state = self.sessions.get(session_id)
        if state and state.user_id == user_id:
            return state
        return None

    def move(self, state: GameState, entity_id: str, direction: str) -> Optional[str]:
        entity = state.entities.get(entity_id)
        if not entity or not entity.alive():
            return "Invalid entity"
        if entity.action_points <= 0:
            return "No action points"

        dx, dy = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }.get(direction, (0, 0))
        if dx == dy == 0:
            return "Invalid direction"

        new_pos = (entity.position[0] + dx, entity.position[1] + dy)
        if not state.game_map.walkable(new_pos):
            return "Blocked"

        # prevent stacking on other entities
        if any(e.position == new_pos and e.alive() for e in state.entities.values()):
            return "Tile occupied"

        entity.position = new_pos
        entity.action_points -= 1
        return None

    def attack(self, state: GameState, attacker_id: str, target_id: str) -> Optional[str]:
        attacker = state.entities.get(attacker_id)
        target = state.entities.get(target_id)
        if not attacker or not target or not attacker.alive() or not target.alive():
            return "Invalid attacker/target"
        if attacker.action_points <= 0:
            return "No action points"

        if distance(attacker.position, target.position) > attacker.range:
            return "Out of range"

        damage = attacker.attack
        target.hp -= damage
        attacker.action_points -= 1

        if target.hp <= 0:
            target.hp = 0
        return None

    def end_turn(self, state: GameState) -> None:
        state.advance_turn()

    def ai_take_turn(self, state: GameState) -> None:
        current = state.current_entity()
        if current.is_player or not current.alive():
            return

        player = next(e for e in state.entities.values() if e.is_player)
        # simple AI: move toward player, then attack if in range
        while current.action_points > 0 and current.alive():
            if distance(current.position, player.position) <= current.range:
                err = self.attack(state, current.id, player.id)
                if err:
                    break
            else:
                dx = 1 if player.position[0] > current.position[0] else -1 if player.position[0] < current.position[0] else 0
                dy = 1 if player.position[1] > current.position[1] else -1 if player.position[1] < current.position[1] else 0
                # prioritize horizontal move if possible
                move_dir = None
                if dx != 0:
                    move_dir = "right" if dx > 0 else "left"
                elif dy != 0:
                    move_dir = "down" if dy > 0 else "up"
                if move_dir:
                    err = self.move(state, current.id, move_dir)
                    if err:
                        break
                else:
                    break
        self.end_turn(state)


def state_to_dict(state: GameState) -> Dict:
    return {
        "session_id": state.id,
        "map": {
            "width": state.game_map.width,
            "height": state.game_map.height,
            "tiles": state.game_map.tiles,
        },
        "entities": [
            {
                "id": e.id,
                "name": e.name,
                "hp": e.hp,
                "attack": e.attack,
                "range": e.range,
                "position": e.position,
                "is_player": e.is_player,
                "action_points": e.action_points,
            }
            for e in state.entities.values()
        ],
        "turn_order": state.turn_order,
        "current_turn": state.turn_order[state.current_turn_index],
    }
