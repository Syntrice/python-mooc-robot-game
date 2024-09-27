import pygame
import random

GAME_TITLE = "Robot Game"
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60


class GameApplication:
    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.run()

    def update(self) -> None:
        self.handle_events()

    def render(self) -> None:
        pass

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
                tile_grid[i].append(0 if random.random() < 0.5 else 1)
        return tile_grid
        
        
    @property
    def width(self):
        """The width property."""
        return self._width
        
    @property
    def height(self):
        """The height property."""
        return self._height



if __name__ == "__main__":
    game = GameApplication()
