import pygame

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
    tiles to render and update.
    """

    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        
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
