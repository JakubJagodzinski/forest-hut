import textwrap
from typing import override

import pygame

from database.game_database_table_columns_names import ItemsTable, AttributesTable, ItemAttributesTable
from src.colors import BLACK, WHITE, RARITY_COLORS
from src.fonts import FONT_ARIAL_18, FONT_ARIAL_16
from src.interface.interface_constants import BORDER_WIDTH, INTERFACE_TILE_SIZE
from src.interface.interface_tile import InterfaceTile


class ItemTile(InterfaceTile):
    QUANTITY_TILE_SIZE = INTERFACE_TILE_SIZE // 2
    QUANTITY_FONT = FONT_ARIAL_16

    MARGIN_OFFSET = 5
    INFO_FONT = FONT_ARIAL_18
    ITEM_INFO_WINDOW_MAX_WIDTH_IN_CHARS = 50

    player_manager = None
    item_icons_manager = None

    def __init__(self, game_surface, x, y):
        super().__init__(
            game_surface=game_surface,
            x=x,
            y=y
        )

        self.item_info = None
        self.item_quantity = None
        self.icon = self.item_icons_manager.get_item_icon(self.EMPTY_INTERFACE_TILE_NAME)

    @classmethod
    def setup_references(cls):
        from src.managers.ui.item_icons_manager import ItemIconsManager
        from src.managers.gameplay.player_manager import PlayerManager

        cls.player_manager = PlayerManager.get_instance()
        cls.item_icons_manager = ItemIconsManager.get_instance()

    @override
    @property
    def is_empty(self):
        return self.item_info is None

    @override
    def are_requirements_met(self):
        return self.is_empty or self.player_manager.lvl >= self.item_info[ItemsTable.REQUIRED_LVL]

    def set_item(self, item_info, item_quantity):
        self.item_info = item_info
        self.item_quantity = item_quantity

        if self.is_empty:
            icon_name = None
        else:
            icon_name = self.item_info[ItemsTable.ICON_NAME]
        self.icon = self.item_icons_manager.get_item_icon(icon_name)

    def get_item_formatted_info(self, item_info, item_attributes=None) -> list[str]:
        lines = [f'{item_info[ItemsTable.RARITY_ID]}']

        if item_attributes is not None:
            for attribute in item_attributes:
                attribute_value = item_attributes[ItemAttributesTable.ATTRIBUTE_VALUE]
                sign = '-' if attribute_value < 0 else '+'
                lines.append(f'{sign}{attribute_value} {attribute[AttributesTable.ATTRIBUTE_NAME]}')

        if item_info[ItemsTable.ITEM_DESCRIPTION] is not None:
            item_description = f'"{item_info[ItemsTable.ITEM_DESCRIPTION]}"'
            chunks = textwrap.wrap(item_description, width=self.ITEM_INFO_WINDOW_MAX_WIDTH_IN_CHARS)
            for chunk in chunks:
                lines.append(chunk)

        if item_info[ItemsTable.REQUIRED_LVL] > 0:
            lines.append(f'Requires level {item_info[ItemsTable.REQUIRED_LVL]}')

        lines.append(f'Value: {item_info[ItemsTable.ITEM_VALUE]}')

        return lines

    def draw_item_quantity(self):
        if self.item_quantity is not None and self.item_quantity > 1:
            quantity_text = self.QUANTITY_FONT.render(str(self.item_quantity), False, WHITE)
            quantity_rect = pygame.Rect(
                self.rect.x + self.QUANTITY_TILE_SIZE,
                self.rect.y + self.QUANTITY_TILE_SIZE,
                self.QUANTITY_TILE_SIZE,
                self.QUANTITY_TILE_SIZE
            )

            # draw black background
            pygame.draw.rect(
                self.game_surface,
                BLACK,
                quantity_rect,
                border_radius=10
            )

            # draw white border
            pygame.draw.rect(
                self.game_surface,
                WHITE,
                quantity_rect,
                width=BORDER_WIDTH,
                border_radius=10
            )

            quantity_text_x = (quantity_rect.x
                               + (self.QUANTITY_TILE_SIZE // 2)
                               - (quantity_text.get_width() // 2))
            quantity_text_y = (quantity_rect.y
                               + (self.QUANTITY_TILE_SIZE // 2)
                               - (quantity_text.get_height() // 2))

            self.game_surface.blit(quantity_text, (quantity_text_x, quantity_text_y))

    @override
    def draw(self):
        self.draw_icon()
        self.draw_item_quantity()

    @override
    def draw_hover_info(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not self.is_empty:
            name_text = self.NAME_FONT.render(
                self.item_info[ItemsTable.ITEM_NAME],
                False,
                RARITY_COLORS[self.item_info[ItemsTable.RARITY_ID]]
            )
            infos = [name_text]
            infos_widths = [name_text.get_width()]
            info_lines = self.get_item_formatted_info(self.item_info)
            for line in info_lines:
                info_text = self.INFO_FONT.render(line, False, WHITE)
                infos.append(info_text)
                infos_widths.append(info_text.get_width())
            info_window_width = max(infos_widths) + (2 * self.MARGIN_OFFSET)
            info_window_height = len(infos) * (self.INFO_FONT.get_height() + self.MARGIN_OFFSET)
        elif self.name == self.EMPTY_INTERFACE_TILE_NAME:
            info_window_width = self.EMPTY_INTERFACE_TILE_NAME_TEXT.get_width() + (2 * self.MARGIN_OFFSET)
            info_window_height = self.INFO_FONT.get_height() + (2 * self.MARGIN_OFFSET)
            infos = [self.EMPTY_INTERFACE_TILE_NAME_TEXT]
        else:
            info_window_width = self.name_text.get_width() + (2 * self.MARGIN_OFFSET)
            info_window_height = self.INFO_FONT.get_height() + (2 * self.MARGIN_OFFSET)
            infos = [self.name_text]

        if mouse_x < self.game_surface.get_width() // 2:
            window_x_pos = self.rect.x + INTERFACE_TILE_SIZE
        else:
            window_x_pos = self.rect.x - info_window_width

        if mouse_y + info_window_height < self.game_surface.get_height():
            window_y_pos = mouse_y
        else:
            window_y_pos = mouse_y - info_window_height

        # draw black background
        pygame.draw.rect(
            self.game_surface, BLACK,
            (window_x_pos,
             window_y_pos,
             info_window_width,
             info_window_height),
            border_radius=10
        )

        # draw white border
        pygame.draw.rect(
            self.game_surface, WHITE,
            (window_x_pos,
             window_y_pos,
             info_window_width,
             info_window_height),
            width=BORDER_WIDTH,
            border_radius=10
        )

        for info_nr in range(len(infos)):
            self.game_surface.blit(
                infos[info_nr],
                (
                    window_x_pos + self.MARGIN_OFFSET,
                    window_y_pos + (info_nr * (self.INFO_FONT.get_height() + self.MARGIN_OFFSET))
                )
            )
