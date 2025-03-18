from abc import abstractmethod

from src.common_utils import normalise_movement_vector
from src.entities.entity import Entity
from src.enums.character_attribute_type import CharacterAttributeType
from src.enums.move_direction_type import MoveDirection
from src.enums.sprite_state import SpriteState
from src.sprites.character_sprite import CharacterSprite

CHARACTER_DRAW_SIZE = 200
INTERACTION_DISTANCE = CHARACTER_DRAW_SIZE // 2


class Character(Entity):
    ATTACK_COOLDOWN_IN_SECONDS = 0.5
    IN_COMBAT_STATE_TIME_IN_SECONDS = 5.0

    SPEED_SLOWED = 75
    SPEED_WALK = 150
    SPEED_RUN = 300

    def __init__(self, game_surface, map_id, x, y, draw_size, sprite_name, name, lvl, attributes, faction):
        super().__init__(
            game_surface=game_surface,
            map_id=map_id,
            x=x,
            y=y,
            draw_size=draw_size,
            name=name
        )

        if sprite_name is not None:
            self.animated_sprite = CharacterSprite(self.game_surface, sprite_name, self._draw_size)

        self.faction = faction
        self._lvl = lvl
        self.attributes = attributes

        self.movement_speed = self.SPEED_WALK
        self.is_moving_to_destination_row_and_column = False
        self.destination_row_and_column = (0, 0)
        self.move_to_destination_action = None
        self.path = None

        self.spells_handler = None

        self.was_dead = False
        self.death_time = float('-inf')

        self.last_attack_time = float('-inf')
        self.combat_start_time = float('-inf')

    @classmethod
    def setup_references(cls):
        from src.managers.gameplay.map_manager import MapManager

        cls.map_manager = MapManager.get_instance()

    def load_spells(self):
        from src.spells.spells_handler import SpellsHandler

        self.spells_handler = SpellsHandler(self.game_surface, self)

    @property
    def lvl(self) -> int:
        return self._lvl

    def set_sprite_state(self, state) -> None:
        self.animated_sprite.set_sprite_state(state)

    def reset_sprite_state(self) -> None:
        self.animated_sprite.set_sprite_state(SpriteState.IDLE)
        self.animated_sprite.set_direction(MoveDirection.DOWN)

    def set_sprite_direction_to_position(self, position: (float, float)) -> None:
        if position is not None:
            x, y = position
            if y < self.y:
                self.animated_sprite.set_direction(MoveDirection.UP)
            elif y > self.y:
                self.animated_sprite.set_direction(MoveDirection.DOWN)

            if x < self.x:
                self.animated_sprite.set_direction(MoveDirection.LEFT)
            elif x > self.x:
                self.animated_sprite.set_direction(MoveDirection.RIGHT)

    @abstractmethod
    def handle_death(self):
        pass

    def handle_spell_cast_finish(self) -> None:
        if self.spells_handler is not None:
            self.spells_handler.handle_spell_cast_finish()

    def cancel_spell_cast(self) -> None:
        if self.spells_handler is not None:
            self.spells_handler.cancel_spell_cast()

    def get_attribute(self, attribute_name):
        return self.attributes.get(attribute_name, 0)

    @property
    def damage(self) -> int:
        return self.attributes[CharacterAttributeType.DAMAGE]

    @property
    def attack_distance(self) -> int:
        return self.attributes[CharacterAttributeType.ATTACK_DISTANCE]

    def increase_hp(self, delta: int) -> None:
        if delta == -1:
            delta = self.get_attribute(CharacterAttributeType.MAX_HP)
        self.attributes[CharacterAttributeType.HP] = min(
            self.get_attribute(CharacterAttributeType.HP) + delta,
            self.get_attribute(CharacterAttributeType.MAX_HP)
        )

    def decrease_hp(self, delta: int) -> None:
        self.attributes[CharacterAttributeType.HP] = max(
            self.get_attribute(CharacterAttributeType.HP) - delta,
            0
        )

    def increase_mana(self, delta: int) -> None:
        if delta == -1:
            delta = self.get_attribute(CharacterAttributeType.MAX_MANA)
        self.attributes[CharacterAttributeType.MANA] = min(
            self.get_attribute(CharacterAttributeType.MANA) + delta,
            self.get_attribute(CharacterAttributeType.MAX_MANA)
        )

    def decrease_mana(self, delta: int) -> None:
        self.attributes[CharacterAttributeType.MANA] = max(
            self.get_attribute(CharacterAttributeType.MANA) - delta,
            0
        )

    @property
    def is_dead(self) -> bool:
        return self.get_attribute(CharacterAttributeType.HP) <= 0

    @property
    def died_right_now(self) -> bool:
        return self.is_dead and not self.was_dead

    @property
    def is_attack_ready(self) -> bool:
        return (self.game_clock.game_time - self.last_attack_time) > self.ATTACK_COOLDOWN_IN_SECONDS

    @property
    def is_in_combat(self) -> bool:
        return (self.game_clock.game_time - self.combat_start_time) < self.IN_COMBAT_STATE_TIME_IN_SECONDS

    def enter_combat_state(self) -> None:
        self.combat_start_time = self.game_clock.game_time

    def take_damage(self, amount) -> None:
        self.enter_combat_state()
        self.cancel_spell_cast()
        self.decrease_hp(amount)
        self.set_sprite_state(SpriteState.HURT)

    def set_attack_cooldown(self) -> None:
        self.last_attack_time = self.game_clock.game_time

    def perform_attack(self, target) -> bool:
        attack_conditions = [
            self.is_enemy(target),
            not self.is_dead,
            not target.is_dead,
            not target.is_immune,
            self.is_attack_ready,
            self.is_target_in_attack_distance(target)
        ]

        if all(attack_conditions):
            target.take_damage(self.damage)
            self.set_sprite_direction_to_position(target.position)
            self.animated_sprite.set_sprite_state(SpriteState.BASE_ATTACK)
            self.set_attack_cooldown()
            return True
        else:
            return False

    def set_state_dead(self) -> None:
        self.cancel_spell_cast()
        self.animated_sprite.set_sprite_state(SpriteState.DEAD)
        self.death_time = self.game_clock.game_time
        self.was_dead = True

    def set_state_alive(self) -> None:
        self.reset_sprite_state()
        self.was_dead = False

    @property
    def is_at_destination(self) -> bool:
        return (self.row == self.destination_row_and_column[0]
                and self.column == self.destination_row_and_column[1])

    def is_enemy(self, target) -> bool:
        return self.faction != target.faction

    def set_movement_speed(self, speed: int) -> None:
        self.movement_speed = speed

    def is_target_in_attack_distance(self, target) -> bool:
        return self.is_target_in_distance(target, self.attack_distance)

    def set_path(self, destination_x, destination_y) -> None:
        destination_row = self.map_manager.get_row(destination_y)
        destination_column = self.map_manager.get_column(destination_x)
        self.path = self.map_manager.a_star(
            self.row,
            self.column,
            destination_row,
            destination_column
        )
        if self.path:
            self.is_moving_to_destination_row_and_column = True
            self.destination_row_and_column = (destination_row, destination_column)

    def update_path(self) -> None:
        if self.is_moving_to_destination_row_and_column and self.path:
            if self.row == self.path[0][0] and self.column == self.path[0][1]:
                self.path.pop(0)

    def move_to_destination(self, delta_time: float) -> None:
        self.update_path()
        if self.path:
            movement_vector = [0, 0]

            player_row = self.row
            player_column = self.column
            target_row = self.path[0][0]
            target_column = self.path[0][1]

            if player_row < target_row:
                movement_vector[1] = 1
                self.animated_sprite.set_direction(MoveDirection.DOWN)
            elif player_row > target_row:
                movement_vector[1] = -1
                self.animated_sprite.set_direction(MoveDirection.UP)

            if player_column < target_column:
                movement_vector[0] = 1
                self.animated_sprite.set_direction(MoveDirection.RIGHT)
            elif player_column > target_column:
                movement_vector[0] = -1
                self.animated_sprite.set_direction(MoveDirection.LEFT)

            if len(self.path) > 1:
                if movement_vector[0] == 0:
                    if player_column < self.path[1][1]:
                        movement_vector[0] = 1
                        self.animated_sprite.set_direction(MoveDirection.RIGHT)
                    elif player_column > self.path[1][1]:
                        movement_vector[0] = -1
                        self.animated_sprite.set_direction(MoveDirection.LEFT)

                if movement_vector[1] == 0:
                    if player_row < self.path[1][0]:
                        movement_vector[1] = 1
                    elif player_row > self.path[1][0]:
                        movement_vector[1] = -1

            self.move(movement_vector, delta_time)

            if self.is_at_destination:
                self.is_moving_to_destination_row_and_column = False
                self.animated_sprite.set_sprite_state(SpriteState.IDLE)

    def move(self, movement_vector: [float, float], delta_time: float) -> None:
        if movement_vector != [0, 0]:
            self.cancel_spell_cast()
            self.animated_sprite.set_sprite_state(SpriteState.RUN)
            movement_vector = normalise_movement_vector(movement_vector)
            pixel_movement_vector = [movement_vector[0] * self.movement_speed * delta_time,
                                     movement_vector[1] * self.movement_speed * delta_time]
            new_x = self._x + pixel_movement_vector[0]
            new_y = self._y + pixel_movement_vector[1]
            new_row_nr = self.map_manager.get_row(new_y)
            new_column_nr = self.map_manager.get_column(new_x)
            if not self.map_manager.is_collision_on_field(new_row_nr, self.column):
                self._y = new_y
            if not self.map_manager.is_collision_on_field(self.row, new_column_nr):
                self._x = new_x
