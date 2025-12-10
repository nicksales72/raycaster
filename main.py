import pygame as py

def create_grid(surface, width: int, height: int) -> None:
    # for 16:9 displays for now
    for i in range(0, width + 1, width // 16):
        py.draw.line(surface, "white", (i, 0), (i, 720))
    for j in range(0, height + 1, height // 9):
        py.draw.line(surface, "white", (0, j), (1280, j))

def player_to_mouse(surface, player_posx, player_posy, mouse_posx, mouse_posy):
    py.draw.line(surface, "white", (player_posx, player_posy), (mouse_posx, mouse_posy))

def get_line_eq(player_posx, player_posy, mouse_posx, mouse_posy):
    if (mouse_posx - player_posx) != 0:
        m = (mouse_posy - player_posy) / (mouse_posx - player_posx)
        b = player_posy - (m * player_posx)
        print(f"y = {m:.2f}x + {b:.2f}")
        return m, b

def draw_intersection_points(surface, m, b, player_posx, player_posy, mouse_posx, mouse_posy, width, height):
    # there is probably a better way to do this
    if mouse_posx > player_posx and mouse_posy > player_posy:
        for x in range(0, mouse_posx, width // 16):
            if x <= player_posx:
                continue
            py.draw.circle(surface, "red", (x, m * x + b), 10)
        for y in range(0, mouse_posy, height // 9):
            if y <= player_posy:
                continue
            py.draw.circle(surface, "red", ((y - b) / m, y), 10)
    elif mouse_posx < player_posx and mouse_posy > player_posy:
        for x in range(width, mouse_posx, -(width // 16)):
            if x >= player_posx:
                continue
            py.draw.circle(surface, "red", (x, m * x + b), 10)
        for y in range(0, mouse_posy, height // 9):
            if y <= player_posy:
                continue
            py.draw.circle(surface, "red", ((y - b) / m, y), 10)
    elif mouse_posx > player_posx and mouse_posy < player_posy:
        for x in range(0, mouse_posx, width // 16):
            if x <= player_posx:
                continue
            py.draw.circle(surface, "red", (x, m * x + b), 10)
        for y in range(height, mouse_posy, -(height // 9)):
            if y >= player_posy:
                continue
            py.draw.circle(surface, "red", ((y - b) / m, y), 10)
    elif mouse_posx < player_posx and mouse_posy < player_posy:
        for x in range(width, mouse_posx, -(width // 16)):
            if x >= player_posx:
                continue
            py.draw.circle(surface, "red", (x, m * x + b), 10)
        for y in range(height, mouse_posy, -(height // 9)):
            if y >= player_posy:
                continue
            py.draw.circle(surface, "red", ((y - b) / m, y), 10)


def main():
    width = 1280
    height = 720

    player_posx = width // 2
    player_posy = height // 2

    py.init()
    surface = py.display.set_mode((width, height))
    clock = py.time.Clock()

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT: running = False

        surface.fill("black")
        create_grid(surface, width, height)

        player = py.draw.circle(surface, "blue", (player_posx, player_posy), 10)
        mouse_posx, mouse_posy = py.mouse.get_pos()

        player_to_mouse(surface, player_posx, player_posy, mouse_posx, mouse_posy) 
        m, b = get_line_eq(player_posx, player_posy, mouse_posx, mouse_posy)

        draw_intersection_points(surface, m, b, player_posx, player_posy, mouse_posx, mouse_posy, width, height)

        py.display.flip()
        clock.tick(60)
        
    py.quit()

if __name__ == "__main__":
    main()
