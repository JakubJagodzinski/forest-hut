import pygame

from src.interface.interface_constants import INTERFACE_TILE_SIZE
from src.interface.item_tile import ItemTile
from src.managers.ui.item_icons_manager import ItemIconsManager


class ItemTilesGrid:

    def __init__(self, game_surface, x, y, rows, columns, max_tiles=None):
        self.game_surface = game_surface
        self.rows = rows
        self.columns = columns
        if max_tiles is None:
            self.max_tiles = rows * columns
        else:
            self.max_tiles = max_tiles
        self.rect = pygame.Rect(
            x,
            y,
            self.rows * INTERFACE_TILE_SIZE,
            self.columns * INTERFACE_TILE_SIZE
        )
        self.item_icons_manager = ItemIconsManager.get_instance()
        self.tiles = []
        self.create_grid()

    def create_grid(self):
        tiles_added = 0
        for row_nr in range(self.rows):
            row = []
            for column_nr in range(self.columns):
                if tiles_added == self.max_tiles:
                    break
                row.append(
                    ItemTile(
                        self.game_surface,
                        self.rect.x + (column_nr * INTERFACE_TILE_SIZE),
                        self.rect.y + (row_nr * INTERFACE_TILE_SIZE)
                    )
                )
                tiles_added += 1
            self.tiles.append(row)
            if tiles_added == self.max_tiles:
                break

    @property
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @property
    def grid_size(self):
        return self.rows * self.columns

    def get_row_and_column(self, item_nr):
        return item_nr // self.columns, item_nr % self.columns

    def clear(self):
        tile_nr = 0
        for row_nr in range(self.rows):
            for column_nr in range(self.columns):
                if tile_nr == self.max_tiles:
                    return
                self.tiles[row_nr][column_nr].set_item(None, None)
                tile_nr += 1

    def get_tile_name(self, row, column):
        return self.tiles[row][column].name

    def set_tile_name(self, row, column, tile_name):
        self.tiles[row][column].set_name(tile_name)

    def set_tile_item(self, row, column, item_info, item_quantity):
        self.tiles[row][column].set_item(item_info, item_quantity)

    def set_item(self, slot_nr, item_info, item_quantity):
        row_nr, column_nr = self.get_row_and_column(slot_nr)
        self.set_tile_item(row_nr, column_nr, item_info, item_quantity)

    def set_items(self, items):
        self.clear()
        for item_nr, (item_info, item_quantity) in enumerate(items):
            if item_nr >= self.grid_size:
                return
            row_nr, column_nr = self.get_row_and_column(item_nr)
            self.tiles[row_nr][column_nr].set_item(item_info, item_quantity)

    def get_left_clicked_tile_nr(self) -> int | None:
        tile_nr = 0
        for row_nr in range(self.rows):
            for column_nr in range(self.columns):
                if tile_nr == self.max_tiles:
                    return row_nr
                if self.tiles[row_nr][column_nr].is_left_clicked():
                    return (row_nr * self.columns) + column_nr
                tile_nr += 1
        return None

    def get_right_clicked_tile_nr(self) -> int | None:
        tile_nr = 0
        for row_nr in range(self.rows):
            for column_nr in range(self.columns):
                if tile_nr == self.max_tiles:
                    return row_nr
                if self.tiles[row_nr][column_nr].is_right_clicked():
                    return (row_nr * self.columns) + column_nr
                tile_nr += 1
        return None

    def draw(self):
        tile_nr = 0
        for row_nr in range(self.rows):
            for column_nr in range(self.columns):
                if tile_nr == self.max_tiles:
                    return
                self.tiles[row_nr][column_nr].draw()
                tile_nr += 1

    def draw_hovered(self):
        tile_nr = 0
        for row_nr in range(self.rows):
            for column_nr in range(self.columns):
                if tile_nr == self.max_tiles:
                    return
                self.tiles[row_nr][column_nr].draw_hovered()
                tile_nr += 1
