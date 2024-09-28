from __future__ import annotations
import pygame
import math
from random import randint
from enum import Enum

# Constants

GAME_TITLE = "Robot Game"  # the title for the game caption
CAMERA_WIDTH = 7  # the camera width in tiles
CAMERA_HEIGHT = 7  # the camera height in tiles
TILE_SIZE = 86  # tile size in pixels
FPS = 60  # fps of the game
COIN_COUNT = 100 # number of coins on the screen
MONSTER_COUNT = 20 # number of coins on the screen

MAP = [
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

PLAYER_MOVE_EVENT = pygame.USEREVENT + 1

class GameApplication:
    def __init__(self) -> None:
        pygame.init()
        self.window_width = CAMERA_WIDTH * TILE_SIZE  # in pixels
        self.window_height = CAMERA_HEIGHT * TILE_SIZE  # in pixels
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        # set world and camera
        self.world = World(MAP)
        self.camera = Camera(CAMERA_WIDTH, CAMERA_HEIGHT, self.world, TILE_SIZE)

        # pre game setup
        self.load_resources()
        
        self.world.place_coins(self.images[3])
        self.world.add_monsters(self.images[1])
        self.player = Player(self.images[0], 6, 6)
        
        self.setup_events()

        # start game loop
        self.run()

    def load_resources(self) -> None:
        self.images = []
        self.images.append(pygame.image.load("src/robot.png"))
        self.images.append(pygame.image.load("src/monster.png"))
        self.images.append(pygame.image.load("src/door.png"))
        self.images.append(pygame.image.load("src/coin.png"))

    def setup_events(self) -> None:
        self.player_move_event = pygame.USEREVENT + 1

    def update(self, delta: float) -> None:
        self.handle_events()

        # center camera on player
        self.camera.center_on_point(self.player.x_pos, self.player.y_pos)

    def render(self, delta: float) -> None:

        self.window.fill((0, 0, 0))  # clear window with solid color

        self.camera.render_world_tiles(self.window)
        self.camera.render_world_entities(self.window)
    
        self.camera.render_image_entity(self.window, self.player)
        

        pygame.display.flip()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                match (event.key):
                    case pygame.K_UP:
                        if not self.player.is_moving():
                            self.player.move_up = 1
                            self.player.move(self.world)
                            pygame.time.set_timer(PLAYER_MOVE_EVENT, 1000 // self.player.speed)
                        else:
                            self.player.move_up = 1
                    case pygame.K_DOWN:
                        if not self.player.is_moving():
                            self.player.move_down = 1
                            self.player.move(self.world)
                            pygame.time.set_timer(PLAYER_MOVE_EVENT, 1000 // self.player.speed)
                        else:
                            self.player.move_down = 1
                    case pygame.K_LEFT:
                        if not self.player.is_moving():
                            self.player.move_left = 1
                            self.player.move(self.world)
                            pygame.time.set_timer(PLAYER_MOVE_EVENT, 1000 // self.player.speed)
                        else:
                            self.player.move_left = 1
                    case pygame.K_RIGHT:
                        if not self.player.is_moving():
                            self.player.move_right = 1
                            self.player.move(self.world)
                            pygame.time.set_timer(PLAYER_MOVE_EVENT, 1000 // self.player.speed)
                        else:
                            self.player.move_right = 1
                        
            if event.type == pygame.KEYUP:
                match (event.key):
                    case pygame.K_UP:
                        self.player.move_up = 0
                        if not self.player.is_moving():
                            pygame.time.set_timer(PLAYER_MOVE_EVENT, 0)
                    case pygame.K_DOWN:
                        self.player.move_down = 0
                        if not self.player.is_moving():
                            pygame.time.set_timer(PLAYER_MOVE_EVENT, 0)
                    case pygame.K_LEFT:
                        self.player.move_left = 0
                        if not self.player.is_moving():
                            pygame.time.set_timer(PLAYER_MOVE_EVENT, 0)
                    case pygame.K_RIGHT:
                        self.player.move_right = 0
                        if not self.player.is_moving():
                            pygame.time.set_timer(PLAYER_MOVE_EVENT, 0)
                            
            if event.type == PLAYER_MOVE_EVENT:
                self.player.move(self.world)

    def run(self) -> None:
        while True:
            delta = self.clock.tick(FPS)
            self.update(delta)
            self.render(delta)


class World:
    """
    A class representing a tile-based game world, on which to keep track of
    tiles to render and update. Tile types are currently defined using integer
    IDs.
    """

    def __init__(self, tile_grid: list[list[int]]) -> None:
        self._width = len(tile_grid[0])
        self._height = len(tile_grid)
        self._tile_grid = tile_grid
        self._coins: dict[tuple[int,int], ImageEntity] = {}
        self._monsters: dict[tuple[int,int], ImageEntity] = {}

    def get_tile_at_position(self, x: int, y: int) -> Tile:

        # Check if the position is out of bounds. If so, return a bounds tile.
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return Tile.BOUNDS

        return Tile(self._tile_grid[y][x])

    def set_tile_at_position(self, x: int, y: int, tile: Tile) -> None:
        self._tile_grid[y][x] = tile.value
        
    def place_coins(self, coin_image: pygame.Surface) -> None:
        
        i = 0
        while i < COIN_COUNT:
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            
    
            if self.get_tile_at_position(x, y).is_collidable:
                continue
            
            if (x, y) in self._coins.keys():
                continue
            
            if (x, y) in self._monsters.keys():
                continue
            
            coin = ImageEntity(coin_image, x, y)
            
            self.coins[(x, y)] = coin
            i += 1
        print(sorted(self.coins.keys()))
        
    def add_monsters(self, monster_image: pygame.Surface) -> None:
        i = 0
        while i < MONSTER_COUNT:
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            
    
            if self.get_tile_at_position(x, y).is_collidable:
                continue
            
            if (x, y) in self._monsters.keys():
                continue
            
            if (x, y) in self._coins.keys():
                continue
            
            monster = ImageEntity(monster_image, x, y)
            
            self.monsters[(x, y)] = monster
            i += 1

    @property
    def width(self):
        """The width property."""
        return self._width

    @property
    def height(self):
        """The height property."""
        return self._height

    @property
    def coins(self):
        """The coins property."""
        return self._coins
    
    @property
    def monsters(self):
        """The monsters property."""
        return self._monsters

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

    def render_world_tiles(self, surface: pygame.Surface) -> None:
        """
        Renders the camera view to the given surface.
        """
        for x in range(0, self.width):
            for y in range(0, self.height):
                tile = self._world.get_tile_at_position(x + self.pos_x, y + self.pos_y)
                top_x = x * self._tile_size
                top_y = y * self._tile_size
                bototm_x = top_x + self._tile_size
                bototm_y = top_y + self._tile_size
                pygame.draw.rect(
                    surface, tile.color, (top_x, top_y, bototm_x, bototm_y)
                )

    def render_world_entities(self, surface: pygame.Surface) -> None:
        for x in range(0, self.width):
            for y in range(0, self.height):
                for coin in self._world.coins.values():
                    self.render_image_entity(surface, coin)
                for monster in self._world.monsters.values():
                    self.render_image_entity(surface, monster)
                    

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

    def center_on_point(self, x: int, y: int) -> None:
        """
        Centers the camera on the given point.
        """
        self.pos_x = x - self.width // 2
        self.pos_y = y - self.height // 2

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
    A game entity that has an pygame. Surface image object associated with it.
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

class Player(ImageEntity):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int, speed = 4) -> None:
        super().__init__(image, x_pos, y_pos)
        self.move_up = 0
        self.move_down = 0
        self.move_left = 0
        self.move_right = 0
        self.speed = speed # speed in tiles per second
        
    def move(self, world: World):
        new_x_pos = self.x_pos + self.move_right - self.move_left
        new_y_pos = self.y_pos + self.move_down - self.move_up
        
        if not world.get_tile_at_position(new_x_pos, self.y_pos).is_collidable:
            self.x_pos = new_x_pos
            
        if not world.get_tile_at_position(self.x_pos, new_y_pos).is_collidable:
            self.y_pos = new_y_pos
    
    def is_moving(self):
        return bool(self.move_up + self.move_down + self.move_left + self.move_right)

if __name__ == "__main__":
    game = GameApplication()
