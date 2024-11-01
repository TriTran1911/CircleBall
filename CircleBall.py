import random
import pygame
import numpy as np
import math


class Ball:
    def __init__(self, position, velocity):
        self.pos =  np.array(position, dtype=np.float64)
        self.v = np.array(velocity, dtype=np.float64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.is_inside = True

def draw_arc(win, center, radius, start_angle, end_angle):
    p1 = center + (radius * 2) * np.array([math.cos(start_angle), math.sin(start_angle)], dtype=np.float64)
    p2 = center + (radius * 2) * np.array([math.cos(end_angle), math.sin(end_angle)], dtype=np.float64)
    pygame.draw.polygon(win, BLACK, [center, p1, p2], 0)

def is_ball_inside_arc(ball_pos, CIRCLE_CENTER, start_angle, end_angle):
    dx = ball_pos[0] - CIRCLE_CENTER[0]
    dy = ball_pos[1] - CIRCLE_CENTER[1]
    ball_angle = math.atan2(dy, dx)
    start_angle = start_angle % (2 * math.pi)
    end_angle = end_angle % (2 * math.pi)
    if start_angle > end_angle:
        end_angle += 2 * math.pi
    if start_angle <= ball_angle <= end_angle or start_angle <= ball_angle + 2 * math.pi <= end_angle:
        return True

# Initialize the game
pygame.init()
WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Ball")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Circle
CIRCLE_CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=np.float64)
CIRCLE_RADIUS = 150

# Arc 
arc_degrees = 50
start_angle = math.radians(-arc_degrees / 2)
end_angle = math.radians(arc_degrees / 2)

spinning_speed = 0.01

# Physics
GRAVITY = 0.2
ball_velocity = np.array([0, 0], dtype=np.float64)

# Ball
BALL_RADIUS = 5
ball_pos = np.array([WIDTH / 2, HEIGHT / 2 - 120], dtype=np.float64)
balls = [Ball(ball_pos, ball_velocity)]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update the spinning angle
    start_angle += spinning_speed
    end_angle += spinning_speed
    for ball in balls:
        # count balls if the amount of balls is greater than 100 then exit the game
        if len(balls) > 1200:
            running = False
            
        # Add a 2 new balls if the current ball is outside the circle
        if ball.pos[1] > HEIGHT or ball.pos[1] < 0 or ball.pos[0] < 0 or ball.pos[0] > WIDTH:
            balls.remove(ball)
            balls.append(Ball(position = ball_pos, velocity = [random.uniform(-4, 4), random.uniform(-1, 1)]))
            balls.append(Ball(position = ball_pos, velocity = [random.uniform(-4, 4), random.uniform(-1, 1)]))
        
        # Update the ball position
        ball.v[1] += GRAVITY
        ball.pos += ball.v
        
        distance = np.linalg.norm(ball.pos - CIRCLE_CENTER)
        if distance + BALL_RADIUS > CIRCLE_RADIUS:
            # check if the ball status
            if is_ball_inside_arc(ball.pos, CIRCLE_CENTER, start_angle, end_angle):
                ball.is_inside = False
            if ball.is_inside:
                # vector from the circle center to the ball
                d = ball.pos - CIRCLE_CENTER
                
                # check if the ball hits the circle
                d_unit = d / np.linalg.norm(d)
                ball.pos = CIRCLE_CENTER + d_unit * (CIRCLE_RADIUS - BALL_RADIUS)
                
                # tangent vector (t = -r)
                t = np.array([-d[1], d[0]], dtype=np.float64) 
                # projection of the velocity vector on the tangent (b = ((v.t)/(t.t)) * t)
                v_t = (np.dot(ball.v, t)/np.dot(t, t)) * t
                ball.v = 2 * v_t - ball.v
                
                # move the ball to the left (v = rw)
                ball.v += t * spinning_speed
    
    # Clear the screen
    win.fill(BLACK)
    
    # Draw the circle and the ball
    pygame.draw.circle(win, WHITE, CIRCLE_CENTER, CIRCLE_RADIUS, 4)
    draw_arc(win, CIRCLE_CENTER, CIRCLE_RADIUS, start_angle, end_angle)
    for ball in balls:
        pygame.draw.circle(win, ball.color, ball.pos, BALL_RADIUS)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()