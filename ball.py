import pygame
import math

class Ball:
    """
    creates new Ball object with:
    colour: (val, val, cal)
    x: coordinate
    y: coordinate
    x_vel: horizontal velocity
    y_vel: vertical velocity
    gravity: amount of gravity to add each update
    trail: number of trail frames to add
    fading: if trail should fade (True/False)
    efficiency: efficiency of collisions
    friction: friction to be added to velocity each update
    """
    def __init__(self, colour, x, y, x_vel, y_vel, r, gravity, trail, fading, border, efficiency, friction):
        self.colour = colour
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.r = r
        self.gravity = gravity
        self.trail = trail
        self.fading = fading
        self.trail_frames = [] #Not from class call
        self.efficiency = efficiency
        self.friction = friction / 1000
        self.border = border
        self.border_width = int(r / 6)
        self.bounces = 0
        
    def update(self):
        """
        update the balls velocities. Applies friction and gravity and frames if applicable
        """
        self.x += self.x_vel
        self.y += self.y_vel
        
        if abs(self.x_vel) > self.friction:
            if self.x_vel > 0:
                self.x_vel -= self.friction
            else:
                self.x_vel += self.friction
        else:
            self.x_vel = 0

        if abs(self.y_vel) > self.friction:
            if self.y_vel > 0:
                self.y_vel -= self.friction
            else:
                self.y_vel += self.friction
        else:
            self.y_vel = 0

        self.y_vel += self.gravity
        
        if len(self.trail_frames) >= self.trail and self.trail != 0:
            self.trail_frames.pop(0)
        
        if self.trail != 0:
            self.trail_frames.append((self.colour, (int(self.x), int(self.y)), self.r))
        
    def draw(self, screen):
        """_summary_
        draws ball to screen
        """
        if self.fading:
            for i, frame in enumerate(self.trail_frames):
                # Create a semi-transparent surface
                trail_surface = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
                alpha = int(255 * (i + 1) / len(self.trail_frames))  # Gradual transparency
                trail_colour = (*frame[0], alpha)
                pygame.draw.circle(trail_surface, trail_colour, (self.r, self.r), self.r)
                screen.blit(trail_surface, (frame[1][0] - self.r, frame[1][1] - self.r))
            if self.border:
                pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.r + self.border_width)
            pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.r)
        else:
            for frame in self.trail_frames:
                pygame.draw.circle(screen, frame[0], frame[1], frame[2])
            if self.border:
                pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.r + self.border_width)
            pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.r)
    
    def check_collision_with_border(self, screen_width, screen_height):
        x_flag = False
        y_flag = False
        
        if self.x_vel != 0:
            if self.x + self.r >= screen_width:
                self.x = screen_width - self.r 
                self.x_vel *= -self.efficiency
                x_flag = True
            elif self.x - self.r <= 0:
                self.x = self.r
                self.x_vel *= -self.efficiency
                x_flag = True
        
        if self.y_vel != 0:
            if self.y + self.r >= screen_height:
                self.y = screen_height - self.r 
                self.y_vel *= -self.efficiency
                y_flag = True
            elif self.y - self.r <= 0:
                self.y = self.r
                self.y_vel *= -self.efficiency
                y_flag = True
            
        if self.efficiency < 1:
            if y_flag and abs(self.y_vel) > 1:
                if self.y_vel > 0:
                    self.y_vel -= self.friction
                else:
                    self.y_vel += self.friction
            elif y_flag and abs(self.y_vel) < 1:
                self.y_vel = 0

            if x_flag and abs(self.x_vel) > 1:
                if self.x_vel > 0:
                    self.x_vel -= self.friction
                else:
                    self.x_vel += self.friction
            elif x_flag and abs(self.x_vel) < 1:
                self.x_vel = 0
                
        if x_flag or y_flag:
            self.bounces += 1

        return y_flag or x_flag

    def check_collision_with_ball(self, ball, static=False):
        dx = ball.x - self.x
        dy = ball.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Handling zero distance to prevent division by zero
        if distance == 0:
            distance = 1e-6  # A small value to prevent division by zero

        flag = False

        if distance < self.r + ball.r:
            # Calculate the normal vector
            nx = dx / distance
            ny = dy / distance
            
            flag = True
            
            # Calculate the tangent vector
            tx = -ny
            ty = nx
            
            # Dot product tangent
            dpTan1 = self.x_vel * tx + self.y_vel * ty
            dpTan2 = ball.x_vel * tx + ball.y_vel * ty
            
            # Dot product normal
            dpNorm1 = self.x_vel * nx + self.y_vel * ny
            dpNorm2 = ball.x_vel * nx + ball.y_vel * ny
            
            # Conservation of momentum in 1D
            m1 = math.pi * self.r**2
            m2 = math.pi * ball.r**2
            
            new_dpNorm1 = (dpNorm1 * (m1 - m2) + 2 * m2 * dpNorm2) / (m1 + m2)
            new_dpNorm2 = (dpNorm2 * (m2 - m1) + 2 * m1 * dpNorm1) / (m1 + m2)
            
            # Apply efficiency to the normal components
            new_dpNorm1 *= self.efficiency
            new_dpNorm2 *= self.efficiency
            
            # Update velocities
            self.x_vel = tx * dpTan1 + nx * new_dpNorm1
            self.y_vel = ty * dpTan1 + ny * new_dpNorm1
            if not static:
                ball.x_vel = tx * dpTan2 + nx * new_dpNorm2
                ball.y_vel = ty * dpTan2 + ny * new_dpNorm2
            
            # Prevent overlap
            overlap = 0.5 * (self.r + ball.r - distance + 1)  # Adjust to prevent sticking
            self.x -= nx * overlap
            self.y -= ny * overlap
            if not static:
                ball.x += nx * overlap
                ball.y += ny * overlap
            
            self.bounces += 1
            ball.bounces += 1
            
        return flag

    
    def check_collision_with_ring(self, ring):
        """
        Checks for collision with a ring and keeps the ball inside the ring.
        ring: Ring object with properties x (center x-coordinate), y (center y-coordinate), and r (radius).
        """
        dx = self.x - ring.x
        dy = self.y - ring.y
        distance = math.sqrt(dx**2 + dy**2)
        x_flag = False
        y_flag = False
        flag = False
        
        # Check if the ball is outside the ring
        if distance + self.r > ring.r:
            # Normal vector
            nx = dx / distance
            ny = dy / distance
            
            x_flag = True
            y_flag = True
            flag = True
            
            # Reflect the velocity to keep the ball inside
            dpNorm = self.x_vel * nx + self.y_vel * ny
            self.x_vel -= 2 * dpNorm * nx * self.efficiency
            self.y_vel -= 2 * dpNorm * ny * self.efficiency
            
            # Move the ball inside the ring
            overlap = distance + self.r - ring.r
            self.x -= nx * overlap
            self.y -= ny * overlap
            self.bounces += 1
            
        if self.efficiency < 1:
            if y_flag and abs(self.y_vel) > 1:
                if self.y_vel > 0:
                    self.y_vel -= self.friction
                else:
                    self.y_vel += self.friction
            elif y_flag and abs(self.y_vel) < self.friction * 500:
                self.y_vel = 0

            if x_flag and abs(self.x_vel) > 1:
                if self.x_vel > 0:
                    self.x_vel -= self.friction
                else:
                    self.x_vel += self.friction
            elif x_flag and abs(self.x_vel) < self.friction * 500:
                self.x_vel = 0
                
                
        return flag