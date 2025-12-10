from __future__ import annotations
import pygame as py

class Vector2:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def get_line_eq(self, other:Vector2) -> tuple[float, float]:
        if (other.x - self.x) != 0:
            m = (other.y - self.y) / (other.x - self.x)
            b = self.y - (m * self.x)
            return m, b
        else: return 0, 0 # temporary

def create_grid(surface, width: int, height: int) -> None:
    # for 16:9 displays for now
    for x in range(0, width + 1, width // 16):
        py.draw.line(surface, "white", (x, 0), (x, height))
    for y in range(0, height + 1, height // 9):
        py.draw.line(surface, "white", (0, y), (width, y))

def player_to_mouse(surface, player_pos:Vector2, mouse_pos:Vector2) -> None:
    py.draw.line(surface, "white", (player_pos.x, player_pos.y), (mouse_pos.x, mouse_pos.y))

def draw_intersection_points(surface, m:float, b:float, 
                             width:int, height:int,
                             player_pos:Vector2, mouse_pos:Vector2) -> None:
    # there is probably a better way to do this
    if mouse_pos.x > player_pos.x and mouse_pos.y > player_pos.y:
        for x in range(0, mouse_pos.x, width // 16):
            if x <= player_pos.x:
                continue
            py.draw.circle(surface, "red", (x, m * x + b), 10)
        for y in range(0, mouse_pos.y, height // 9):
            if y <= player_pos.y:
                continue
            py.draw.circle(surface, "red", ((y - b) / m, y), 10)
    elif mouse_pos.x < player_pos.x and mouse_pos.y > player_pos.y:
        for x in range(width, mouse_pos.x, -(width // 16)):
            if x >= player_pos.x:
                continue
            py.draw.circle(surface, "red", (x, m * x + b), 10)
        for y in range(0, mouse_pos.y, height // 9):
            if y <= player_pos.y:
                continue
            py.draw.circle(surface, "red", ((y - b) / m, y), 10)
    elif mouse_pos.x > player_pos.x and mouse_pos.y < player_pos.y:
        for x in range(0, mouse_pos.x, width // 16):
            if x <= player_pos.x:
                continue
            py.draw.circle(surface, "red", (x, m * x + b), 10)
        for y in range(height, mouse_pos.y, -(height // 9)):
            if y >= player_pos.y:
                continue
            py.draw.circle(surface, "red", ((y - b) / m, y), 10)
    elif mouse_pos.x < player_pos.x and mouse_pos.y < player_pos.y:
        for x in range(width, mouse_pos.x, -(width // 16)):
            if x >= player_pos.x:
                continue
            py.draw.circle(surface, "red", (x, m * x + b), 10)
        for y in range(height, mouse_pos.y, -(height // 9)):
            if y >= player_pos.y:
                continue
            py.draw.circle(surface, "red", ((y - b) / m, y), 10)


def main():
    width = 1280
    height = 720

    player_pos = Vector2(width // 2, height // 2)

    py.init()
    surface = py.display.set_mode((width, height))
    clock = py.time.Clock()

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT: running = False

        surface.fill("black")
        create_grid(surface, width, height)

        player = py.draw.circle(surface, "blue", (player_pos.x, player_pos.y), 10)
        mouse_posx, mouse_posy = py.mouse.get_pos()
        mouse_pos = Vector2(mouse_posx, mouse_posy)

        player_to_mouse(surface, player_pos, mouse_pos) 
        m, b = player_pos.get_line_eq(mouse_pos)

        draw_intersection_points(surface, m, b, width, height, player_pos, mouse_pos)

        py.display.flip()
        clock.tick(60)
        
    py.quit()

if __name__ == "__main__":
    main()
