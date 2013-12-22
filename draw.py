# helper functions for drawing
import pygame
from vector2D import Vec2d

def xfrange(start, stop, step):
    while start < stop:
        yield start
        start += step

def draw_arrow(surf, frompos, topos, width, color):
    perp = (Vec2d(topos) - Vec2d(frompos)).perpendicular_normal() * width
    pygame.draw.polygon(surf, color, (topos, frompos - perp, frompos + perp))


def draw_arrowline(surf, frompos, topos, width, length, offset, color):
    dir = Vec2d(topos) - Vec2d(frompos)
    l = dir.get_length()
    ndir = dir.normalized()
    for lpos in xfrange(offset, l, length):
        draw_arrow(surf, 
                frompos + ndir * lpos, 
                frompos + ndir * (lpos + length),
                width,
                color)


def draw_text(surf, pos, text, size, color):
    font = pygame.font.Font(None, size)
    text = font.render(text, 1, color)
    textpos = text.get_rect(center=pos)
    surf.blit(text, textpos)

def draw_outlined_text(surf, pos, text, size, line_width, line_color, fill_color):
    for xofs in range(-line_width, line_width + 1):
        for yofs in range(-line_width, line_width + 1):
            draw_text(surf, Vec2d(xofs, yofs) + pos, text, size, line_color)
    draw_text(surf, pos, text, size, fill_color)

