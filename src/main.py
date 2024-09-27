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
        
if __name__ == "__main__":
    game = GameApplication()