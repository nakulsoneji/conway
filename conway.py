import sys, pygame
from pygame import Surface
from pygame.font import Font
from data import *


class Conway:
    def __init__(self, cell_dim: int=10, cell_padding: int=1, dim: list[int]=[1600, 800]):
        pygame.init();
        self.font: Font = pygame.font.SysFont("arial", 16)
        self.alive: int = 0
        self.gen: int = 0
        self.cell_dim: int = cell_dim
        self.cell_padding: int = cell_padding
        self.rows: int = dim[1] // (self.cell_dim + self.cell_padding)
        self.cols: int = dim[0] // (self.cell_dim + self.cell_padding)
        self.tick: int = 1
        dim[0] = dim[0] + self.cell_padding - (dim[0] - (self.cols * (self.cell_dim + self.cell_padding)))
        dim[1] = dim[1] + self.cell_padding - (dim[1] - (self.rows * (self.cell_dim + self.cell_padding)))  
        self.dim: int = dim
        self.cells: Toroidal2DArray[Cell] = Toroidal2DArray(self.rows, self.cols)
        self.surface: Surface = pygame.display.set_mode(self.dim)
        self.surface.fill((0, 0, 0))
    
    def gen_cells(self):
        for i in range(0, self.rows):
            row = []
            for j in range(0, self.cols):          
                cell: Cell = Cell(pygame.Rect(j * self.cell_dim + (j + 1) * self.cell_padding, i * self.cell_dim + (i + 1) * self.cell_padding, self.cell_dim, self.cell_dim))
                row.append(cell);
            self.cells.add_list(row)
            
    def initial_state(self):
        pass
        # self.cells.get_item(30, 30).set_alive(True)
        # self.cells.get_item(29, 30).set_alive(True)
        # self.cells.get_item(29, 31).set_alive(True)
        # self.cells.get_item(29, 32).set_alive(True)
        
        # for i in self.get_neighbors(30, 30):
        #     i.set_alive(True)
    
    def get_neighbors(self, i: int, j: int) -> list[Cell]:
        return [
            self.cells.get_item(i - 1, j),
            self.cells.get_item(i - 1, j + 1),
            self.cells.get_item(i, j + 1),
            self.cells.get_item(i + 1, j + 1),
            self.cells.get_item(i + 1, j),
            self.cells.get_item(i + 1, j - 1),
            self.cells.get_item(i, j - 1),
            self.cells.get_item(i - 1, j - 1),
        ]   
        
    def draw_cells(self, simulate):
        if simulate:
            dead_cells: list[Cell] = []
            alive_cells: list[Cell] = []
            
        self.alive = 0;
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                cell: Cell = self.cells.get_item(i, j)
                pygame.draw.rect(self.surface, cell.color(), cell.rect)
                alive: bool = cell.alive()
                if alive:
                    self.alive += 1
                if simulate:
                    neighbors = self.get_neighbors(i, j)
                    live_neighbors = [n for n in neighbors if n.alive()]
                    if alive and (len(live_neighbors) < 2 or len(live_neighbors) > 3):
                        dead_cells.append(cell)

                    elif not alive and len(live_neighbors) == 3:
                        alive_cells.append(cell)    
        
        if self.alive == 0:
            return
        
        if simulate:
            for c in dead_cells:
                c.set_alive(False)
            for c in alive_cells:
                c.set_alive(True)

            self.gen += 1
    
    def reset(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                self.cells.get_item(i, j).set_alive(False)
        self.gen = 0;
        self.draw_cells()
            
    def text(self) -> Surface:
        return self.font.render(f"Gen: {self.gen} Pop: {self.alive}", True, (0, 0, 0))

    def run(self):
        self.gen_cells()
        self.initial_state()
        play: bool = False;
        count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i in range(0, self.cells.rows):
                        for j in range(0, self.cells.cols):
                            cell: Cell = self.cells.get_item(i, j)
                            rect: Rect = cell.rect
                            if rect.collidepoint(mouse_pos):
                                cell.set_alive(not cell.alive())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.reset()
                        play = False
                    if event.key == pygame.K_w:
                        play = not play
                    if event.key == pygame.K_e and not play:
                        self.draw_cells(True)
                        count += 1
            
            self.surface.fill((195, 195, 195))
            self.draw_cells(play)
            self.surface.blit(self.text(), (15, 15))
            pygame.time.wait(0)
            pygame.display.flip()
            
if __name__ == '__main__':
    app: Conway = Conway()
    app.run()