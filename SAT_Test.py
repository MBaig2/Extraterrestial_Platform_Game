import pygame as pg
from rot_test import *
from settings import *

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))


class Rectangle:
    def __init__(self, x, y, l, w):
        self.x = x
        self.y = y
        self.l = l
        self.w = w


rect1 = pg.Rect(10, 10, 50, 30)
rect2 = pg.Rect(100, 100, 10, 100)
rectangle_dragging = False

w = rect2.width
h = rect2.height
Tx = rect2.left
Ty = rect2.top
x0 = Tx
y0 = Ty
angle = 333.44
points = np.array([[x0, y0, 1], [x0 + w, y0, 1], [x0, y0 + h, 1], [x0 + w, y0 + h, 1]])
rect_coor = getWorldCoord(points, Tx, Ty, angle)
rect_coor_vec = arrayToVector(rect_coor)
rect_center = rect2.centerx

line_coor = [(200, 200), (100, 100)]

collision_font = pg.font.Font(None, 30)
collision_message = "collided!"
collision_render = collision_font.render(collision_message, True, BLACK)
collision_text_rect = collision_render.get_rect()
collision_text_rect.center = (WIDTH - 100, HEIGHT - 100)


# - mainloop -

clock = pg.time.Clock()

running = True

while running:
    screen.fill(LIGHTGREY)
    surf = pg.Surface(rect2.size).convert_alpha()

    # - events -

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rect1.rect.collidepoint(event.pos):
                    rectangle_dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rect1.rect.x - mouse_x
                    offset_y = rect1.rect.y - mouse_y

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_dragging = False

        elif event.type == pg.MOUSEMOTION:
            if rectangle_dragging:
                mouse_x, mouse_y = event.pos
                rect1.rect.x = mouse_x + offset_x
                rect1.rect.y = mouse_y + offset_y

    # - updates (without draws) -
    player_coor = [
        (rect1.rect.left, rect1.rect.top),
        (rect1.rect.right, rect1.rect.top),
        (rect1.rect.left, rect1.rect.bottom),
        (rect1.rect.right, rect1.rect.bottom),
    ]
    collision_ob = SAT_Collision(player_coor, rect_coor_vec)
    collision_chk = collision_ob.collision_dect()
    overlap_val = collision_ob.overlap_val

    if collision_chk:
        screen.blit(collision_render, collision_text_rect)
        # d = vec(rect2.left - rect1.rect.left, rect2.top - rect1.rect.top)
        # s = np.sqrt(d.x * d.x + d.y * d.y)
        # rect1.rect.left -= 10 * d.x / s
        # rect1.rect.top -= 10 * d.y / s

    # empty

    # - draws (without updates) -

    pg.draw.rect(surf, (RED), rect2)

    rotSurf = pg.transform.rotate(surf, angle)

    screen.blit(rotSurf, (Tx, Ty))
    pg.draw.rect(screen, BLUE, rect1)
    # pg.draw.line(screen, RED, line_coor[1], line_coor[0], 3)
    # pg.draw.rect(screen, RED, rect2)
    pg.display.flip()
    rect_center = rect2.center
    rect_coor = getWorldCoord(points, Tx, Ty, angle)

    # - constant game speed / FPS -

    clock.tick(FPS)


# - end -

pg.quit()
