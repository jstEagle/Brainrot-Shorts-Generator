import pygame
import pygame.gfxdraw
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

    # Class-level scratch surface for fading trail rendering
    _trail_scratch = None
    _trail_scratch_size = 0

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

    def update(self, dt=1.0):
        """
        update the balls velocities. Applies friction and gravity and frames if applicable.
        dt: time scale factor (1.0 = normal, <1 = slow-mo)
        """
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt

        if abs(self.x_vel) > self.friction:
            if self.x_vel > 0:
                self.x_vel -= self.friction * dt
            else:
                self.x_vel += self.friction * dt
        else:
            self.x_vel = 0

        if abs(self.y_vel) > self.friction:
            if self.y_vel > 0:
                self.y_vel -= self.friction * dt
            else:
                self.y_vel += self.friction * dt
        else:
            self.y_vel = 0

        self.y_vel += self.gravity * dt

        if len(self.trail_frames) >= self.trail and self.trail != 0:
            self.trail_frames.pop(0)

        if self.trail != 0:
            self.trail_frames.append((self.colour, (int(self.x), int(self.y)), self.r))

    def _draw_aa_circle(self, surface, color, pos, radius):
        """Draw an anti-aliased filled circle using gfxdraw."""
        x, y = int(pos[0]), int(pos[1])
        r = int(radius)
        if r < 1:
            r = 1
        try:
            pygame.gfxdraw.aacircle(surface, x, y, r, color)
            pygame.gfxdraw.filled_circle(surface, x, y, r, color)
        except (ValueError, OverflowError):
            pygame.draw.circle(surface, color, (x, y), r)

    @classmethod
    def _get_trail_scratch(cls, needed_size):
        """Get or grow a class-level scratch surface for trail rendering."""
        if cls._trail_scratch is None or needed_size > cls._trail_scratch_size:
            cls._trail_scratch_size = needed_size
            cls._trail_scratch = pygame.Surface((needed_size, needed_size), pygame.SRCALPHA)
            cls._trail_scratch.fill((0, 0, 0, 0))
        return cls._trail_scratch

    def draw(self, screen, glow=False, glow_color=None):
        """
        draws ball to screen with anti-aliased circles.
        glow: if True, draw a glow effect behind the ball.
        glow_color: color for the glow (defaults to ball colour).
        """
        # Draw glow effect if enabled
        if glow:
            from effects import draw_glow
            color = glow_color if glow_color else self.colour
            draw_glow(screen, color, (int(self.x), int(self.y)), int(self.r))

        if self.fading:
            num_trail = len(self.trail_frames)
            for i, frame in enumerate(self.trail_frames):
                trail_r = int(frame[2])
                if trail_r < 1:
                    trail_r = 1
                size = trail_r * 2
                scratch = Ball._get_trail_scratch(size)
                scratch.fill((0, 0, 0, 0), (0, 0, size, size))
                alpha = int(255 * (i + 1) / num_trail)
                trail_colour = (*frame[0], alpha)
                pygame.draw.circle(scratch, trail_colour, (trail_r, trail_r), trail_r)
                screen.blit(scratch, (frame[1][0] - trail_r, frame[1][1] - trail_r), (0, 0, size, size))
            if self.border:
                self._draw_aa_circle(screen, (0, 0, 0), (self.x, self.y), self.r + self.border_width)
            self._draw_aa_circle(screen, self.colour, (self.x, self.y), self.r)
        else:
            for frame in self.trail_frames:
                self._draw_aa_circle(screen, frame[0], frame[1], frame[2])
            if self.border:
                self._draw_aa_circle(screen, (0, 0, 0), (self.x, self.y), self.r + self.border_width)
            self._draw_aa_circle(screen, self.colour, (self.x, self.y), self.r)

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

        # Squared-distance early-out
        combined_r = self.r + ball.r
        dist_sq = dx * dx + dy * dy
        if dist_sq >= combined_r * combined_r:
            return False

        distance = math.sqrt(dist_sq)

        # Handling zero distance to prevent division by zero
        if distance == 0:
            distance = 1e-6  # A small value to prevent division by zero

        # Calculate the normal vector
        nx = dx / distance
        ny = dy / distance

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

        return True


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

    def apply_gravity_towards(self, target_x, target_y, strength=1.0):
        """
        Apply gravitational acceleration towards a target point (1/r^2 law).
        Used for orbital mechanics (gravity well simulation).
        """
        dx = target_x - self.x
        dy = target_y - self.y
        dist_sq = dx * dx + dy * dy
        dist = math.sqrt(dist_sq)
        if dist < 5:
            return  # prevent extreme forces at very close range
        force = strength / dist_sq
        # Cap force to prevent explosion
        force = min(force, 2.0)
        self.x_vel += force * dx / dist
        self.y_vel += force * dy / dist
