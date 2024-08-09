from pygame import Rect
from typing import TypeVar

T = TypeVar("T")

class Cell:
    alive_color = (0, 0, 0)
    dead_color = (255, 255, 255)
    
    def __init__(self, rect: Rect):
        self.__alive: bool = False
        self.__color: tuple[int, int, int] = Cell.dead_color
        self.rect = rect
        
    def color(self) -> tuple[int, int, int]:
        return self.__color

    def alive(self) -> bool:
        return self.__alive
    
    def set_alive(self, status: bool):
        if status:
            self.__alive = True
            self.__color = Cell.alive_color
        else:
            self.__alive = False
            self.__color = Cell.dead_color

class Toroidal2DArray:
    def __init__(self, rows: int, cols: int):
        self.__array: list[list[T]] = []
        self.rows = rows
        self.cols = cols
    
    def add_list(self, arr: list[T]):
        if (len(self.__array) < self.rows and len(arr) == self.cols):
            self.__array.append(arr)
        else:
            print("array has reached size limit or array is not equal to cols")
    
    def get_item(self, i: int, j: int) -> T:
        return self.__array[i % self.rows][j % self.cols]
