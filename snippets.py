#draw_grid(self.surf, (0,0,250), FIELDSIZE.x, FIELDSIZE.y, GRIDWIDTH)
def draw_grid(surf, color, xdist, ydist, width):
    # draw vertical lines
    xmax, ymax = surf.get_size()
    for x in range(0, xmax, xdist):
        pygame.draw.line(surf, color, (x, 0), (x, ymax), width) 
    # draw horizontal lines
    for y in range(0, ymax, ydist):
        pygame.draw.line(surf, color, (0, y), (xmax, y), width) 

