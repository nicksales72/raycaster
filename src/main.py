from __future__ import annotations
import pygame as py

class Vector2:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def get_line_eq(self, other:Vector2) -> tuple[float, float]:
        if (other.x - self.x) != 0: # division by 0
            m = (other.y - self.y) / (other.x - self.x)
            b = self.y - (m * self.x)
            return m, b
        else: return 0, 0 

class MiniMap:
    def __init__(self, width:int, height:int):
        self.width = width 
        self.height = height
        self.surface = None
        self.clock = None

    def create_surface(self) -> None:
        py.init()
        self.surface = py.display.set_mode((self.width, self.height))
        self.clock = py.time.Clock()

    def create_grid(self) -> None:
        for x in range(0, self.width + 1, self.width // 16):
            py.draw.line(self.surface, "white", (x, 0), (x, self.height))
        for y in range(0, self.height + 1, self.height // 9):
            py.draw.line(self.surface, "white", (0, y), (self.width, y))

    def player_to_mouse(self, player_pos:Vector2, mouse_pos:Vector2) -> None:
        py.draw.line(self.surface, "white", (player_pos.x, player_pos.y), (mouse_pos.x, mouse_pos.y))

    def draw_intersection_points(self, m:float, b:float, player_pos:Vector2, mouse_pos:Vector2) -> None:
        step_x = self.width // 16
        step_y = self.height // 9 

        dx = mouse_pos.x - player_pos.x
        dy = mouse_pos.y - player_pos.y

        step_x *= 1 if dx > 0 else -1
        step_y *= 1 if dy > 0 else -1

        if dx > 0:
            for x in range(0, mouse_pos.x, step_x):
                if x <= player_pos.x:
                    continue
                y = m * x + b
                py.draw.circle(self.surface, "red", (x, y), 10)
        else:
            for x in range(self.width, mouse_pos.x, step_x):
                if x >= player_pos.x:
                    continue
                y = m * x + b
                py.draw.circle(self.surface, "red", (x, y), 10)

        if dy > 0:
            for y in range(0, mouse_pos.y, step_y):
                if y <= player_pos.y:
                    continue
                x = (y - b) / m
                py.draw.circle(self.surface, "red", (x, y), 10)
        else:
            for y in range(self.height, mouse_pos.y, step_y):
                if y >= player_pos.y:
                    continue
                x = (y - b) / m
                py.draw.circle(self.surface, "red", (x, y), 10)

    def surface_loop(self, player_pos:Vector2) -> None:
        running = True
        while running:
            for event in py.event.get():
                if event.type == py.QUIT: running = False

            self.surface.fill("black")
            self.create_grid()

            player = py.draw.circle(self.surface, "blue", (player_pos.x, player_pos.y), 10)
            mouse_posx, mouse_posy = py.mouse.get_pos()
            mouse_pos = Vector2(mouse_posx, mouse_posy)

            self.player_to_mouse(player_pos, mouse_pos) 
            m, b = player_pos.get_line_eq(mouse_pos)

            self.draw_intersection_points(m, b, player_pos, mouse_pos)

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
