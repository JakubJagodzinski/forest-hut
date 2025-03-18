from src.interface.item_tiles_grid import ItemTilesGrid
from src.managers.core.mouse_manager import MouseManager


class ScrollableItemTilesGrid(ItemTilesGrid):

    def __init__(self, game_surface, x, y, total_rows, total_columns, visible_rows, visible_columns):
        super().__init__(game_surface, x, y, visible_rows, visible_columns)
        self.total_rows = total_rows
        self.total_columns = total_columns
        self.row_offset = 0

    def reset_row_offset(self):
        self.row_offset = 0

    def get_max_row_offset(self) -> int:
        return self.total_rows - self.rows

    def increase_row_offset(self):
        self.row_offset = min(self.get_max_row_offset(), self.row_offset + 1)

    def decrease_row_offset(self):
        self.row_offset = max(0, self.row_offset - 1)

    def handle_scrolling(self, event) -> bool:
        if self.is_hovered:
            if MouseManager.is_scrolled_up(event):
                self.decrease_row_offset()
                return True
            if MouseManager.is_scrolled_down(event):
                self.increase_row_offset()
                return True
        return False

    def handle_mouse_events(self, event):
        if self.handle_scrolling(event):
            return True

    def draw(self):
        for row_nr in range(self.rows):
            for column_nr in range(self.columns):
                self.tiles[row_nr + self.row_offset][column_nr].draw()

    def draw_hovered(self):
        for row_nr in range(self.rows):
            for column_nr in range(self.columns):
                self.tiles[row_nr + self.row_offset][column_nr].draw_hovered()
