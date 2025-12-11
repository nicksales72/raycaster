from __future__ import annotations
from dataclasses import dataclass 
import pygame as py

@dataclass
class Vector2:
    x:float
    y:float

class MiniMap:
    def __init__(self, width:int, height:int):
        self.width = width 
        self.height = height
        self.surface = None
        self.clock = None
        self.grid_surface = None 

        self.grid_x_step = width // 16 
        self.grid_y_step = height // 9

    def create_surface(self) -> None:
        py.init()
        self.surface = py.display.set_mode((self.width, self.height))
        self.clock = py.time.Clock()
        self._create_grid_surface()

    def _create_grid_surface(self) -> None:
        surf = py.Surface((self.width, self.height))
        surf.fill("black")

        for x in range(0, self.width + 1, self.grid_x_step):
            py.draw.line(surf, "white", (x, 0), (x, self.height))
        for y in range(0, self.height + 1, self.grid_y_step):
            py.draw.line(surf, "white", (0, y), (self.width, y))

        self.grid_surface = surf

    def compute_intersections(self, A:Vector2, B:Vector2): 
        Ax, Ay = A.x, A.y
        Bx, By = B.x, B.y

        dx = Bx - Ax
        dy = By - Ay

        results = []
        for k in range(0, self.width + 1, self.grid_x_step):
            if dx != 0:
                t = (k - Ax) / dx
                if 0 <= t <= 1: 
                    y = Ay + t * dy
                    results.append((k, y))

        for k in range(0, self.width + 1, self.grid_y_step):
            if dy != 0:
                t = (k - Ay) / dy
                if 0 <= t <= 1: 
                    x = Ax + t * dx
                    results.append((x, k))

        return results

    def surface_loop(self, player_pos:Vector2) -> None:
        running = True
        while running:
            for event in py.event.get():
                if event.type == py.QUIT: running = False

            self.surface.blit(self.grid_surface, (0, 0)) # draws grid as surface onto the surface

            mx, my = py.mouse.get_pos()
            mouse_pos = Vector2(mx, my)

            py.draw.line(self.surface, "white", (player_pos.x, player_pos.y), (mouse_pos.x, mouse_pos.y))

            pts = self.compute_intersections(player_pos, mouse_pos)
            for x, y in pts:
                py.draw.circle(self.surface, "red", (int(x), int(y)), 6)

            py.draw.circle(self.surface, "blue", (int(player_pos.x), int(player_pos.y)), 10)

            py.display.flip()
            self.clock.tick(60)
            
        py.quit()

def main():
    width = 1280
    height = 720

    player_pos = Vector2(width // 2, height // 2)

    minimap = MiniMap(width, height)
    minimap.create_surface()
    minimap.surface_loop(player_pos)

if __name__ == "__main__":
    main()
