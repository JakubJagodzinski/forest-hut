from typing import override

from src.entities.objects.object_types.location_changer import LocationChanger
from src.enums.chat_message_color_type import ChatMessageColorType
from src.enums.error_message_type import ErrorMessageType
from src.enums.quote_type import QuoteType
from src.managers.gameplay.map_manager import MAP_COLLISION_TILE, TOWN_MAP_ID
from src.spells.spell import Spell
from src.sprites.object_sprite import ObjectSprite


class OpenPortalToTownSpell(Spell):
    CAST_TIME_IN_SECONDS = 5.0
    COOLDOWN_TIME_IN_SECONDS = 0.0

    TOWN_X = 20 * MAP_COLLISION_TILE
    TOWN_Y = 20 * MAP_COLLISION_TILE

    PORTAL_TO_TOWN_SPRITE_NAME = 'green_portal'
    PORTAL_IN_TOWN_SPRITE_NAME = 'red_portal'

    def __init__(self, caster_reference):
        super().__init__(
            caster_reference=caster_reference,
            cast_time_in_seconds=self.CAST_TIME_IN_SECONDS,
            cooldown_time_in_seconds=self.COOLDOWN_TIME_IN_SECONDS
        )

        self.casting_portal_sprite = ObjectSprite(
            self.caster_reference.game_surface,
            self.PORTAL_TO_TOWN_SPRITE_NAME,
            self.caster_reference.draw_size
        )

    @override
    def begin_cast(self):
        if self.caster_reference.is_dead:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.YOU_ARE_DEAD)
        elif self.caster_reference.is_in_town:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.YOU_ARE_ALREADY_IN_TOWN)
        elif not self.is_being_casted():
            self.caster_reference.is_moving_to_destination_row_and_column = False
            self.caster_reference.chat_manager.push_message_to_chat(
                f'{self.caster_reference.character_name}: {self.quotes_manager.get_random_common_quote(QuoteType.RETURN_TO_TOWN)}',
                ChatMessageColorType.PLAYER
            )
            super().begin_cast()

    @override
    def during_cast_action(self):
        pass

    @override
    def final_action(self):
        self.caster_reference.portal_to_town = LocationChanger(
            game_surface=self.caster_reference.game_surface,
            map_id=self.caster_reference.map_id,
            x=self.caster_reference.x,
            y=self.caster_reference.y,
            destination_map_id=TOWN_MAP_ID,
            destination_x=self.TOWN_X,
            destination_y=self.TOWN_Y,
            draw_size=self.caster_reference.draw_size,
            name=None,
            sprite_name=self.PORTAL_TO_TOWN_SPRITE_NAME
        )

        self.caster_reference.portal_in_town = LocationChanger(
            game_surface=self.caster_reference.game_surface,
            map_id=TOWN_MAP_ID,
            x=self.TOWN_X,
            y=self.TOWN_Y,
            destination_map_id=self.caster_reference.map_id,
            destination_x=self.caster_reference.x,
            destination_y=self.caster_reference.y,
            draw_size=self.caster_reference.draw_size,
            name=self.caster_reference.map_manager.get_location_name(),
            sprite_name=self.PORTAL_IN_TOWN_SPRITE_NAME
        )

        self.caster_reference.portal_to_town.interact()

    @override
    def draw_casting_animation(self):
        self.casting_portal_sprite.draw(self.caster_reference.draw_position)
        self.draw_casting_bar()
