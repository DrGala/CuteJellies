
import pygame
import random


SCREEN_SIZE = (640, 480)

YELLOW = 0
GREEN = 1
RED = 2
BLUE = 3
PURPLE = 4
GREY = 5



                

class ResourceManager:
    def __init__(self):
        images = []
        images.append( self.load_image("png/yellow.png") )
        images.append( self.load_image("png/green.png") )
        images.append( self.load_image("png/red.png") )
        images.append( self.load_image("png/blue.png") )
        images.append( self.load_image("png/purple.png") )
        images.append( self.load_image("png/grey.png") )
        self.images = images
        
    def load_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, (32, 32))

    def get_surface(self, which):
        return self.images[which]




class Jelly(pygame.sprite.Sprite):
    def __init__(self, position, surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.center = position


class Jelly_Yellow(pygame.sprite.Sprite):
    def __init__(self, position, RM):
        Jelly.__init__(self, position, RM.get_surface(YELLOW))

    def update(self):
        pass

class Jelly_Green(pygame.sprite.Sprite):
    def __init__(self, position, RM):
        Jelly.__init__(self, position, RM.get_surface(GREEN))

    def update(self):
        pass

class Jelly_Red(pygame.sprite.Sprite):
    def __init__(self, position, RM):
        Jelly.__init__(self, position, RM.get_surface(RED))

    def update(self):
        pass

class Jelly_Blue(pygame.sprite.Sprite):
    def __init__(self, position, RM):
        Jelly.__init__(self, position, RM.get_surface(BLUE))

    def update(self):
        pass

class Jelly_Purple(pygame.sprite.Sprite):
    def __init__(self, position, RM):
        Jelly.__init__(self, position, RM.get_surface(PURPLE))

    def update(self):
        pass

class Jelly_Grey(pygame.sprite.Sprite):
    def __init__(self, position, RM):
        Jelly.__init__(self, position, RM.get_surface(GREY))

    def update(self):
        pass


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.val = -1

    def fill(self):
        if self.val != -1:
            return
        self.val = random.randrange(0, 6)
    
class Board:
    def __init__(self, RM):
        self.RM = RM
        self.cells = [ [ Cell(0,0), Cell(0,1), Cell(0,2), Cell(0,3), Cell(0,4) ],
                       [ Cell(1,0), Cell(1,1), Cell(1,2), Cell(1,3), Cell(1,4) ],
                       [ Cell(2,0), Cell(2,1), Cell(2,2), Cell(2,3), Cell(2,4) ],
                       [ Cell(3,0), Cell(3,1), Cell(3,2), Cell(3,3), Cell(3,4) ],
                       [ Cell(4,0), Cell(4,1), Cell(4,2), Cell(4,3), Cell(4,4) ],
                       [ Cell(5,0), Cell(5,1), Cell(5,2), Cell(5,3), Cell(5,4) ],
                       [ Cell(6,0), Cell(6,1), Cell(6,2), Cell(6,3), Cell(6,4) ],
                       [ Cell(7,0), Cell(7,1), Cell(7,2), Cell(7,3), Cell(7,4) ]
                       ]

        self.fill_all()
        self.create_game_sprites()


    def fill_all(self):
        for row in self.cells:
            for cell in row:
                cell.fill()

    def create_sprite(self, cell):
        pos = (100 + cell.col * 40, 100 + cell.row * 40)
        if cell.val == YELLOW:
            return Jelly_Yellow( pos, self.RM )
        elif cell.val == GREEN:
            return Jelly_Green( pos, self.RM )
        elif cell.val == RED:
            return Jelly_Red( pos, self.RM )
        elif cell.val == BLUE:
            return Jelly_Blue( pos, self.RM )
        elif cell.val == PURPLE:
            return Jelly_Purple( pos, self.RM )
        else:
            return Jelly_Grey( pos, self.RM ) 
        
    def create_game_sprites(self):
        self.sprites = pygame.sprite.Group()

        for row in self.cells:
            for cell in row:
                self.sprites.add( self.create_sprite(cell) )
        
    def draw(self, surface):
        self.sprites.draw(surface)

    def update(self):
        pass


class Selector:

    
    def __init__(self):
        self.radius = 15
        self.incr = -0.3
        self.positions = []

    def draw(self, screen):
        count = len(self.positions)
        if count == 0:
            return
        elif count == 1:
            pos = self.positions[0]
            pygame.draw.circle(screen, (255,255,255), pos, int(self.radius), 2)
        else:
            pos = pos = self.positions[0]
            pygame.draw.circle(screen, (255,255,255), pos, int(self.radius), 2)
            pos = pos = self.positions[1]
            pygame.draw.circle(screen, (255,255,255), pos, int(self.radius), 2)
        
    def update(self):
        self.radius += self.incr
        if self.radius < 4 or self.radius > 15:
            self.incr *= -1

    def mouse_down(self, row_col):
        pos = (100 + row_col[1] * 40, 100 + row_col[0] * 40)
        self.positions = [ pos, pos ]

    def mouse_move(self, row_col):
        if len(self.positions) == 2:
            pos = (100 + row_col[1] * 40, 100 + row_col[0] * 40)
            self.positions[1] = pos

    def mouse_up(self, row_col):
        self.positions = []
    
class Game:

    RUNNING = 0
    GAME_OVER = 1
    
    def __init__(self, SCREEN_SIZE, caption):
        self.screen = self.init_game_window(SCREEN_SIZE, caption)
        self.RM = ResourceManager()
        self.backdrop = pygame.image.load('png/BG.png')
        self.board = Board(self.RM)
        self.selector = Selector()
        self.state = self.RUNNING
        
    def is_game_over(self):
        return self.state == self.GAME_OVER
    
    def init_game_window(self, screen_size, caption):
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(caption)
        return screen

    def render(self):
        self.screen.blit(self.backdrop,(0,0))
        self.board.draw(self.screen)
        self.selector.draw(self.screen)
        
        pygame.display.update()
        pygame.time.delay(2)
        
    def terminate(self):
        pygame.quit()

    def handle_events(self):
        for ourevent in pygame.event.get():
            # print(ourevent)

            if ourevent.type == pygame.KEYUP:
                if ourevent.key == pygame.K_ESCAPE:
                    self.state = self.GAME_OVER

            if ourevent.type == pygame.MOUSEBUTTONDOWN and ourevent.button == 1:
                self.selector.mouse_down( (0,0) )

            if ourevent.type == pygame.MOUSEMOTION:
                self.selector.mouse_move( (0,1) )

            if ourevent.type == pygame.MOUSEBUTTONUP and ourevent.button == 1:
                self.selector.mouse_up( (0,1) )
                
            
    def update(self):
        self.board.update()
        self.selector.update()


        
def main(args):
    game = Game(SCREEN_SIZE, "python pong")        
    while not game.is_game_over():
        game.render()
        game.handle_events()
        game.update()
    game.terminate()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
