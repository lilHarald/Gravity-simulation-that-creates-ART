import pygame
import math
import random
import copy
import path
from path import Path


WORLD_WIDTH = 1000
WORLD_HEIGHT = 1000
G = 0.03                        # Gravity constant
NUMBER_OF_BODIES = 150
AVERAGE_DENSITY = 300
AVERAGE_RADIUS = 4
TIME_SPEED = 40                 # Frames/ticks per second
START_SPEED = True              # If set to False, all bodies will start standing still
MERGE_WHEN_COLLIDE = True       # Whether the celestial bodies should merge when colliding with each other or not

pygame.font.init()
font = pygame.font.SysFont('Arial', 20, True, False)
BG_COLOR = (0, 0, 0)
win = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))


class Body:
    def __init__(self, density, radius, pos, color):
        self.density = density
        self.radius = radius
        self.pos = pos
        self.color = color
        self.direction = [0, 0]
        self.current_force = [0, 0]
        self.mass = density * radius ** 2 * math.pi
        self.path = Path(color)

    def draw(self):
        pygame.draw.circle(win, self.color, self.pos, self.radius)

    def update(self):
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        if self.path.ticks_to_update == path.TICKS_TO_UPDATE:
            self.path.path.append(copy.copy(self.pos))
            self.path.ticks_to_update = 0
        self.current_force = [0, 0]
        self.path.ticks_to_update += 1

bodies = []
selected_body = None


for i in range(NUMBER_OF_BODIES):
    bodies.append(Body(random.randint(int(AVERAGE_DENSITY / 2), AVERAGE_DENSITY * 2) / 100, random.randint(AVERAGE_RADIUS // 2, AVERAGE_RADIUS * 2), [random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT)], (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))))
    if START_SPEED:
        bodies[-1].direction = [random.randint(-10, 10) / 10, random.randint(-10, 10) / 10]
        print(bodies[-1].direction)


def draw():
    win.fill(BG_COLOR)
    for b in bodies:
        b.draw()
    if selected_body is not None:
        selected_body.path.draw(win)
        pygame.draw.line(win, (255, 255, 255), selected_body.pos, (selected_body.pos[0] + selected_body.direction[0] * 50, selected_body.pos[1] + selected_body.direction[1] * 50), 3)
        pygame.draw.line(win, (255, 100, 100), selected_body.pos, (selected_body.pos[0] + selected_body.current_force[0] * 10, selected_body.pos[1] + selected_body.current_force[1] * 10), 2)
        win.blit(font.render("Mass: " + str(round(selected_body.mass, 2)), True, (255, 255, 255)), (10, 10))
        win.blit(font.render("Density: " + str(round(selected_body.density, 2)), True, (255, 255, 255)), (10, 40))
        win.blit(font.render("Radius: " + str(round(selected_body.radius, 2)), True, (255, 255, 255)), (10, 70))


    pygame.display.update()

def update_bodies():
    for b in bodies:
        b.update()

def gravity():
    global selected_body
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            if j >= len(bodies):
                continue
            distance_x = bodies[i].pos[0] - bodies[j].pos[0]
            distance_y = bodies[i].pos[1] - bodies[j].pos[1]
            distance_squared = distance_x ** 2 + distance_y ** 2

            if distance_squared == 0:
                continue

            if distance_squared < bodies[i].radius ** 2 + bodies[j].radius ** 2:
                if MERGE_WHEN_COLLIDE:
                    bodies[i].pos[0] = (bodies[i].radius * bodies[i].pos[0] + bodies[j].radius * bodies[j].pos[0]) / (bodies[i].radius + bodies[j].radius)
                    bodies[i].direction[0] = (bodies[i].direction[0] * bodies[i].mass + bodies[j].direction[0] * bodies[j].mass) / (bodies[j].mass + bodies[i].mass)
                    bodies[i].direction[1] = (bodies[i].direction[1] * bodies[i].mass + bodies[j].direction[1] * bodies[j].mass) / (bodies[j].mass + bodies[i].mass)
                    bodies[i].radius = math.sqrt(bodies[i].radius * bodies[i].radius + bodies[j].radius * bodies[j].radius)
                    color = [0, 0, 0]
                    color[0] = (bodies[i].color[0] * bodies[i].radius + bodies[j].color[0] * bodies[j].radius) / (bodies[i].radius + bodies[j].radius)
                    color[1] = (bodies[i].color[1] * bodies[i].radius + bodies[j].color[1] * bodies[j].radius) / (bodies[i].radius + bodies[j].radius)
                    color[2] = (bodies[i].color[2] * bodies[i].radius + bodies[j].color[2] * bodies[j].radius) / (bodies[i].radius + bodies[j].radius)
                    bodies[i].color = tuple(color)
                    bodies[i].mass += bodies[j].mass
                    bodies[i].density = bodies[i].mass / (bodies[i].radius ** 2 * math.pi)
                    bodies[i].path.other_paths.append(bodies[j].path)
                    if selected_body == bodies[j]:
                        selected_body = bodies[i]
                    bodies.pop(j)
                else:
                    if bodies[i].pos[0] > bodies[j].pos[0]:
                        bodies[i].pos[0] += abs(distance_x / 2)
                        bodies[j].pos[0] -= abs(distance_x / 2)
                    else:
                        bodies[i].pos[0] -= abs(distance_x / 2)
                        bodies[j].pos[0] += abs(distance_x / 2)
                    if bodies[i].pos[1] > bodies[j].pos[1]:
                        bodies[i].pos[1] += abs(distance_y / 2)
                        bodies[j].pos[1] -= abs(distance_y / 2)
                    else:
                        bodies[i].pos[1] -= abs(distance_y / 2)
                        bodies[j].pos[1] += abs(distance_y / 2)
                continue
            force = G * (bodies[i].mass * bodies[j].mass) / distance_squared
            if distance_x == -distance_y:
                x_part = .5
                y_part = .5
            else:
                x_part = abs(distance_x/(abs(distance_x) + abs(distance_y)))
                y_part = abs(distance_y/(abs(distance_x) + abs(distance_y)))

            if x_part > 40:
                print(x_part)
                print(distance_x/(distance_x + distance_y), distance_x, distance_y)
            # bodies[i].direction[0] += x_part * force / bodies[i].mass
            # bodies[j].direction[0] -= x_part * force / bodies[j].mass
            # bodies[i].direction[1] += y_part * force / bodies[i].mass
            # bodies[j].direction[1] -= y_part * force / bodies[j].mass
            if bodies[i].pos[0] < bodies[j].pos[0]:
                bodies[i].direction[0] += x_part * force / bodies[i].mass
                bodies[j].direction[0] -= x_part * force / bodies[j].mass
                bodies[i].current_force[0] += x_part * force
                bodies[j].current_force[0] -= x_part * force
            else:
                bodies[i].direction[0] -= x_part * force / bodies[i].mass
                bodies[j].direction[0] += x_part * force / bodies[j].mass
                bodies[i].current_force[0] -= x_part * force
                bodies[j].current_force[0] += x_part * force

            if bodies[i].pos[1] < bodies[j].pos[1]:
                bodies[i].direction[1] += y_part * force / bodies[i].mass
                bodies[j].direction[1] -= y_part * force / bodies[j].mass
                bodies[i].current_force[1] += y_part * force
                bodies[j].current_force[1] -= y_part * force
            else:
                bodies[i].direction[1] -= y_part * force / bodies[i].mass
                bodies[j].direction[1] += y_part * force / bodies[j].mass
                bodies[i].current_force[1] -= y_part * force
                bodies[j].current_force[1] += y_part * force



clock = pygame.time.Clock()
run = True
while run:
    clock.tick(TIME_SPEED)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            selected_body = None
            mx, my = pygame.mouse.get_pos()
            for b in bodies:
                if (mx - b.pos[0]) ** 2 + (my - b.pos[1]) ** 2 <= b.radius ** 2:
                    selected_body = b
                    break

    update_bodies()
    gravity()
    draw()
