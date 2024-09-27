from __future__ import annotations
import pygame
from random import random
from enum import Enum

GAME_TITLE = "Robot Game"
WORLD_WIDTH = 64
WORLD_HEIGHT = 48
TILE_SIZE = 16
FPS = 60


class GameApplication:
    def __init__(self) -> None:
        pygame.init()
        self.window_width = WORLD_WIDTH * TILE_SIZE
        self.window_height = WORLD_HEIGHT * TILE_SIZE
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        self.world = World(WORLD_WIDTH, WORLD_HEIGHT)

        self.run()

    def update(self) -> None:
        self.handle_events()

    def render(self) -> None:

        self.window.fill((0, 0, 0))  # clear window with solid color
        self.render_world()
        pygame.display.flip()

    def render_world(self) -> None:
        for i in range(self.world.width):
            for j in range(self.world.height):
                tile = self.world.get_tile_at_position(i, j)
                top_x = i * TILE_SIZE
                top_y = j * TILE_SIZE
                bototm_x = top_x + TILE_SIZE
                bototm_y = top_y + TILE_SIZE
                pygame.draw.rect(
                    self.window, tile.color, (top_x, top_y, bototm_x, bototm_y)
                )

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def run(self) -> None:
        while True:
            self.update()
            self.render()
            self.clock.tick(FPS)


class World:
    """
    A class representing a tile-based game world, on which to keep track of
    tiles to render and update. Tile types are currently defined using integer
    IDs.
    """

    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._tile_grid = self._generate_random_tiles()

    def _generate_random_tiles(self) -> None:
        tile_grid = []
        for i in range(self._width):
            tile_grid.append([])
            for j in range(self._height):
                tile_grid[i].append(
                    Tile.WALL.value if random() < 0.5 else Tile.FLOOR.value
                )
        return tile_grid

    def get_tile_at_position(self, x: int, y: int) -> Tile:
        return Tile(self._tile_grid[x][y])

    def set_tile_at_position(self, x: int, y: int, tile: Tile) -> None:
        self._tile_grid[x][y] = tile.value

    @property
    def width(self):
        """The width property."""
        return self._width

    @property
    def height(self):
        """The height property."""
        return self._height


class Tile(Enum):
    """
    An enumeration representing the different types of tiles that can be
    present in the game world. Each tile type has an ID, a color, and a flag
    indicating whether the tile is collidable or not.
    """

    FLOOR = (0, (120, 120, 120), False)
    WALL = (1, (160, 160, 160), True)

    def __new__(cls, tile_id, color, is_collidable):
        obj = object.__new__(cls)
        obj._value_ = tile_id
        obj.color = color
        obj.is_collidable = is_collidable
        return obj

if __name__ == "__main__":
    game = GameApplication()
