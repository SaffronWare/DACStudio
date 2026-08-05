import pygame

pygame.init()
clock = pygame.time.Clock()


class Application:
    def __init__(self):
        self.FPS = 60
        self.dt = 1/self.FPS
        self.def_dims = (1000, 1000)
        self.window = None

    def start(self):
        self.window = pygame.display.set_mode((1000,1000))
        
        while True:
            self.window.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            pygame.display.flip()
            clock.tick(self.FPS)

        
def main():
    app = Application()
    app.start()


if __name__ == '__main__':
    main()