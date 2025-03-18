from typing import override

from src.entities.objects.object import Object
from src.enums.sprite_state import SpriteState


class LootableObject(Object):
    def __init__(self, game_surface, map_id, x, y, draw_size, name, sprite_name):
        super().__init__(game_surface, map_id, x, y, draw_size, name, sprite_name)

    @override
    def interact(self):
        if self.is_active:
            self.loot_manager.generate_loot((self._x, self._y))
            self.animated_sprite.set_sprite_state(SpriteState.INTERACT)
            self.animated_sprite.set_sprite_state(SpriteState.FINAL)
            self.is_active = False
