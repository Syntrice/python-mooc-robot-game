from __future__ import annotations
import pygame
from random import random
from enum import Enum

GAME_TITLE = "Robot Game"  # the title for the game caption
WORLD_WIDTH = 24  # the world width in tiles
WORLD_HEIGHT = 24  # the world height in tiles
CAMERA_WIDTH = 7  # the camera width in tiles
CAMERA_HEIGHT = 7  # the camera height in tiles
TILE_SIZE = 86  # tile size in pixels
FPS = 60  # fps of the game


class GameApplication:
    def __init__(self) -> None:
        pygame.init()

        # set the width and height of the window in pixels
        self.window_width = CAMERA_WIDTH * TILE_SIZE
        self.window_height = CAMERA_HEIGHT * TILE_SIZE
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()
        
        # set world and camera
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT)
        self.camera = Camera(CAMERA_WIDTH, CAMERA_HEIGHT, self.world, TILE_SIZE)

        # load images
        self.robot_img = pygame.image.load("src/robot.png")
        self.monster_img = pygame.image.load("src/monster.png")
        self.door_img = pygame.image.load("src/door.png")
        self.coin_img = pygame.image.load("src/coin.png")

        # create entities
        self.player = ImageEntity(self.robot_img, 6, 6)
        self.monster = ImageEntity(self.monster_img, 4, 4)
        self.coin = ImageEntity(self.coin_img, 6, 4)
        self.door = ImageEntity(self.door_img, 4, 6)

        self.run()

    def update(self) -> None:
        self.handle_events()
        
        # center camera on player
        self.camera.pos_x = self.player.x_pos - self.camera.width // 2
        self.camera.pos_y = self.player.y_pos - self.camera.height // 2

    def render(self) -> None:

        self.window.fill((0, 0, 0))  # clear window with solid color
        self.camera.render(self.window)
        
        # render image entities
        self.camera.render_image_entity(self.window, self.player)
        self.camera.render_image_entity(self.window, self.monster)
        self.camera.render_image_entity(self.window, self.coin)
        self.camera.render_image_entity(self.window, self.door)
        
        pygame.display.flip()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                match (event.key):
                    case pygame.K_UP:
                        self.player.y_pos -= 1
                    case pygame.K_DOWN:
                        self.player.y_pos += 1
                    case pygame.K_LEFT:
                        self.player.x_pos -= 1
                    case pygame.K_RIGHT:
                        self.player.x_pos += 1

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

        # Check if the position is out of bounds. If so, return a bounds tile.
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return Tile.BOUNDS

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

    # The bounds tile represents a tile that is outside the bounds of a world
    BOUNDS = (-1, (0, 0, 0), True)

    def __new__(cls, tile_id, color, is_collidable):
        obj = object.__new__(cls)
        obj._value_ = tile_id
        obj.color = color
        obj.is_collidable = is_collidable
        return obj


class Camera:
    """
    A class which represents a camera of a given width and height. It keeps
    track of the position of the camera in the world, and is used to aid in
    rendering the world to the screen.
    """

    def __init__(
        self,
        width: int,
        height: int,
        world: World,
        tile_size: int,
        pos_x: int = 0,
        pos_y: int = 0,
    ) -> None:

        self._width = width
        self._height = height
        self._world = world
        self._tile_size = tile_size
        self.pos_x = pos_x
        self.pos_y = pos_y

    def render(self, surface: pygame.Surface) -> None:
        """
        Renders the camera view to the given surface.
        """
        for i in range(0, self.width):
            for j in range(0, self.height):
                tile = self._world.get_tile_at_position(i + self.pos_x, j + self.pos_y)
                top_x = i * self._tile_size
                top_y = j * self._tile_size
                bototm_x = top_x + self._tile_size
                bototm_y = top_y + self._tile_size
                pygame.draw.rect(
                    surface, tile.color, (top_x, top_y, bototm_x, bototm_y)
                )

    def render_image_entity(self, surface: pygame.Surface, entity: ImageEntity) -> None:
        """
        Renders the entity to the surface relative to the game world.
        The image associated with the entity is rendered at the entity's
        position in the camera view, centered on the tile.
        """

        # check if in bounds
        if entity.x_pos < 0 or entity.x_pos > self.pos_x + self.width:
            return
        if entity.y_pos < 0 or entity.y_pos > self.pos_y + self.height:
            return

        # center the entity image on the tile
        x_offset = self._tile_size // 2 - entity.image.get_width() // 2
        y_offset = self._tile_size // 2 - entity.image.get_height() // 2

        entity_x = (entity.x_pos - self.pos_x) * self._tile_size + x_offset
        entity_y = (entity.y_pos - self.pos_y) * self._tile_size + y_offset

        surface.blit(entity.image, (entity_x, entity_y))

    @property
    def width(self):
        """The width property."""
        return self._width

    @property
    def height(self):
        """The height property."""
        return self._height


class ImageEntity:
    """
    A game entity that has an pygame.Surface image object associated with it.
    """

    def __init__(
        self,
        image: pygame.Surface,
        x_pos: int,
        y_pos: int,
    ) -> None:
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos


if __name__ == "__main__":
    game = GameApplication()
