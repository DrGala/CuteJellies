
import pygame
import random


SCREEN_SIZE = (640, 480)

CELL_SIZE = 40
ROW_OFFSET = 100
COL_OFFSET = 100
    
YELLOW = 0
GREEN = 1
RED = 2
BLUE = 3
PURPLE = 4
GREY = 5


SWITCH_JELLIES = pygame.USEREVENT + 1
SWAP_COMPLETED = pygame.USEREVENT + 2
CHECK_FALLING = pygame.USEREVENT + 3


def rowcol_2_screenxy(row, col):
    x = int(CELL_SIZE/2 + COL_OFFSET + col * CELL_SIZE)
    y = int(CELL_SIZE/2 + ROW_OFFSET + row * CELL_SIZE)
    return (x, y)

def screenxy_2_rowcol(x, y):
    row = int((y-ROW_OFFSET) / CELL_SIZE)
    col = int((x-COL_OFFSET) / CELL_SIZE)
    return (row, col)
                    

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

    RM = None
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.jelly = None

    def create_sprite(self):
        pos = rowcol_2_screenxy(self.row, self.col)
        val = random.randrange(0, 6)
        if val == YELLOW:
            self.jelly =  Jelly_Yellow( pos, self.RM )
        elif val == GREEN:
            self.jelly =  Jelly_Green( pos, self.RM )
        elif val == RED:
            self.jelly =  Jelly_Red( pos, self.RM )
        elif val == BLUE:
            self.jelly =  Jelly_Blue( pos, self.RM )
        elif val == PURPLE:
            self.jelly =  Jelly_Purple( pos, self.RM )
        else:
            self.jelly =  Jelly_Grey( pos, self.RM )

    def is_updated(self):
        cell_center = rowcol_2_screenxy(self.row, self.col)
        jelly_center = self.jelly.rect.center
        return cell_center[0] == jelly_center[0] and cell_center[1] == jelly_center[1]
    
    def update(self):
        if self.jelly is None:
            return
        
        cell_center = rowcol_2_screenxy(self.row, self.col)
        jelly_center = self.jelly.rect.center
        dx = 0
        dy = 0
        if (jelly_center[0] < cell_center[0]):
            dx = 1
        if (jelly_center[0] > cell_center[0]):
            dx = -1
        if (jelly_center[1] < cell_center[1]):
            dy = 1
        if (jelly_center[1] > cell_center[1]):
            dy = -1
        self.jelly.rect.move_ip(dx,dy)
        
    
class Board:

    def __init__(self, RM):
        self.RM = RM
        Cell.RM = RM
        self.cells = [ [ Cell(0,0), Cell(0,1), Cell(0,2), Cell(0,3), Cell(0,4) ],
                       [ Cell(1,0), Cell(1,1), Cell(1,2), Cell(1,3), Cell(1,4) ],
                       [ Cell(2,0), Cell(2,1), Cell(2,2), Cell(2,3), Cell(2,4) ],
                       [ Cell(3,0), Cell(3,1), Cell(3,2), Cell(3,3), Cell(3,4) ],
                       [ Cell(4,0), Cell(4,1), Cell(4,2), Cell(4,3), Cell(4,4) ],
                       [ Cell(5,0), Cell(5,1), Cell(5,2), Cell(5,3), Cell(5,4) ],
                       [ Cell(6,0), Cell(6,1), Cell(6,2), Cell(6,3), Cell(6,4) ],
                       [ Cell(7,0), Cell(7,1), Cell(7,2), Cell(7,3), Cell(7,4) ]
                       ]

        self.gather_game_sprites()
        self.swapping = ()

   
    def gather_game_sprites(self):
        self.sprites = pygame.sprite.Group()

        for row in self.cells:
            for cell in row:
                cell.create_sprite()
                self.sprites.add( cell.jelly )
        
    def draw(self, surface):
        self.sprites.draw(surface)

    def update(self):
        for row in self.cells:
            for cell in row:
                cell.update()
        if len(self.swapping) > 0:
            swap_completed = True
            for cell in self.swapping:
                if not cell.is_updated():
                    swap_completed = False
            if swap_completed:
                pygame.event.post( pygame.event.Event( SWAP_COMPLETED, swapped=self.swapping ) )
                self.swapping = ()
                    
            

    def swap(self, start, end):
        cell_a = self.cells[start[0]][start[1]]
        cell_b = self.cells[end[0]][end[1]]
        self.swapping = (cell_a, cell_b)
        cell_a.jelly, cell_b.jelly = cell_b.jelly, cell_a.jelly

    def pop_cells(self, swapped):
        cell_a = swapped[0]
        cell_b = swapped[1]
        if type(cell_a.jelly) != type(cell_b.jelly):
            return self.pop(cell_a) + self.pop(cell_b)
        else:
            return self.pop(cell_a)
                    
    def same(self, dx, dy, cell, popped):
        row = cell.row + dx
        col = cell.col + dy
        other_cell = self.cells[row][col]
        while row in range(0,7) and col in range(0,4) and type(cell.jelly) == type(other_cell.jelly):
            popped.append(other_cell)
            row += dx
            col += dy
            other_cell = self.cells[row][col]

        
    def pop(self, cell):
        popped = []

        if cell.row > 0:
            self.same(-1,0,cell,popped)

        if cell.row < 7:
            self.same(1,0,cell,popped)

        if cell.col > 0:
            self.same(0,-1,cell,popped)

        if cell.col < 4:
            self.same(0,1,cell,popped)

        if len(popped) > 0:
            popped.append(cell)

        count = len(popped)

        if count > 0:
            print('Killing', count, ' jellies')
            for cell in popped:
                cell.jelly.kill()
                cell.jelly = None

        pygame.event.post( pygame.event.Event(CHECK_FALLING) )
        
        return count

    def fall(self):

        print ('Falling jellies')

        falling_cells = []
        
        row_count = len(self.cells)
        col_count = len(self.cells[0])

        moved_jellies = False
        created_jellies = False
        
        for row in range(row_count-1, 0, -1):
            for col in range(0, col_count):
                cell = self.cells[row][col]
                above_cell = self.cells[row-1][col]
                if cell.jelly is None and above_cell.jelly is not None:
                    cell.jelly = above_cell.jelly
                    above_cell.jelly = None
                    moved_jellies = True
                    falling_cells.append(cell)

        if not moved_jellies:
            for col in range(0, col_count):
                cell = self.cells[0][col]
                if cell.jelly is None:
                    cell.create_sprite()
                    self.sprites.add( cell.jelly )
                    created_jellies = True
                    
        return falling_cells
        

                            

        
class Selector:

    def __init__(self):
        self.radius = 15
        self.incr = -0.3
        self.rows_cols = ()
        self.positions = ()
        
    def draw(self, screen):
        count = len(self.positions)
        if count == 0:
            return
        elif count == 2:
            pygame.draw.circle(screen, (255,255,255), self.positions[0], int(self.radius), 2)
            pygame.draw.circle(screen, (255,255,0), self.positions[1], int(self.radius), 2)
        
    def update(self):
        self.radius += self.incr
        if self.radius < 4 or self.radius > 15:
            self.incr *= -1

    def mouse_down(self, row_col):
        if len(self.positions) == 0:
            self.rows_cols = ( row_col, row_col )
            pos = rowcol_2_screenxy(row_col[0], row_col[1])
            self.positions = ( pos, pos )

    def mouse_move(self, row_col):
        if len(self.positions) != 2:
            return

        start_row_col = self.rows_cols[0]
        
        d0 = abs(start_row_col[0] - row_col[0])
        d1 = abs(start_row_col[1] - row_col[1])
        if d0 < 2 and d1 < 2:
            if  (d0==0 or d1==0):
                end_row_col = self.rows_cols[1]
                self.rows_cols = (start_row_col, row_col)
                pos = rowcol_2_screenxy(row_col[0], row_col[1])
                self.positions = (self.positions[0], pos)
            else:
                self.rows_cols = (start_row_col, start_row_col)
                self.positions = (self.positions[0], self.positions[0])
                

    def mouse_up(self, row_col):
        if len(self.rows_cols) == 2:
            rc1 = self.rows_cols[0]
            rc2 = self.rows_cols[1]
            if rc1[0] != rc2[0] or rc1[1] != rc2[1]:
                pygame.event.post( pygame.event.Event(SWITCH_JELLIES, start=rc1, end=rc2) )
        self.rows_cols = ()
        self.positions = ()
    
class Game:

    RUNNING = 0
    GAME_OVER = 1
    WAIT_SWITCH = 2
    WAIT_UNDO_SWITCH = 3
    FALLING = 4
    
    def __init__(self, SCREEN_SIZE, caption):
        self.screen = self.init_game_window(SCREEN_SIZE, caption)
        self.RM = ResourceManager()
        self.backdrop = pygame.image.load('png/BG.png')
        self.board = Board(self.RM)
        self.selector = Selector()
        self.state = self.RUNNING
        self.falling_cells = []
        
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

            if ourevent.type == CHECK_FALLING:
                self.falling_cells = self.board.fall()
                if len(self.falling_cells) > 0:
                    self.state == self.FALLING

            if self.state == self.FALLING:
                if not self.board.fall():
                    print('Back to Running')
                    self.state = self.RUNNING

            if self.state == self.WAIT_UNDO_SWITCH:
                if ourevent.type == SWAP_COMPLETED:
                    self.state = self.RUNNING
                    
            if self.state == self.WAIT_SWITCH:
                if ourevent.type == SWAP_COMPLETED:
                    if self.board.pop_cells(ourevent.swapped) > 0:
                        self.state = self.FALLING
                    else:
                        self.state = self.WAIT_UNDO_SWITCH
                        rowcol_1 = (ourevent.swapped[0].row, ourevent.swapped[0].col)
                        rowcol_2 = (ourevent.swapped[1].row, ourevent.swapped[1].col)
                        self.board.swap(rowcol_1, rowcol_2)
                        
                    
            if self.state == self.RUNNING:
                if ourevent.type == pygame.MOUSEBUTTONDOWN and ourevent.button == 1:
                    self.selector.mouse_down( screenxy_2_rowcol( ourevent.pos[0], ourevent.pos[1] ) )

                if ourevent.type == pygame.MOUSEMOTION:
                    self.selector.mouse_move( screenxy_2_rowcol( ourevent.pos[0], ourevent.pos[1] ) )

                if ourevent.type == pygame.MOUSEBUTTONUP and ourevent.button == 1:
                    self.selector.mouse_up( screenxy_2_rowcol( ourevent.pos[0], ourevent.pos[1] ) )

                if ourevent.type == SWITCH_JELLIES:
                    print('SWITCH JELLIES!', ourevent.start, ourevent.end)
                    self.state = self.WAIT_SWITCH
                    self.board.swap(ourevent.start, ourevent.end)
            
    def update(self):
        self.board.update()
        self.selector.update()

        if self.state == self.FALLING:
            falling_done = True
            for cell in self.falling_cells:
                if not cell.is_updated():
                    falling_done = False

            pygame.event.post( pygame.event.Event(CHECK_FALLING) )
            
    
        
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
