import subprocess
import sys

try:
    # Vérifie si numpy est installé
    import numpy as np
except ImportError:
    try:
        # Tente d'installer numpy
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    except subprocess.CalledProcessError as e:
        print("Error occurred while installing numpy:", e)


try:
    # Vérifie si pygame est installé
    import pygame
except ImportError:
    try:
        # Tente d'installer pygame
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    except subprocess.CalledProcessError as e:
        print("Error occurred while installing pygame:", e)


try:
    # Vérifie si pymunk est installé
    import pymunk
except ImportError:
    try:
        # Tente d'installer pymunk
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymunk"])
    except subprocess.CalledProcessError as e:
        print("Error occurred while installing pymunk:", e)

import numpy as np
import pygame
import pymunk

pygame.init()
rng = np.random.default_rng()

# Constantes
SIZE = WIDTH, HEIGHT = np.array([570, 770])
PAD = (24, 160)
A = (PAD[0], PAD[1])
B = (PAD[0], HEIGHT - PAD[0])
C = (WIDTH - PAD[0], HEIGHT - PAD[0])
D = (WIDTH - PAD[0], PAD[1])
BG_COLOR = (250, 240, 148)
W_COLOR = (205, 133, 63)
FPS = 100
RADII = [17, 25, 32, 38, 50, 63, 75, 87, 100, 115, 135]
THICKNESS = 14
DENSITY = 0.001
ELASTICITY = 0.22  # Plus le nombre est grand, plus ça rebondit
IMPULSE = 10000
GRAVITY = 1200
DAMPING = 0.5
NEXT_DELAY = FPS
BIAS = 0.00001
POINTS = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66]
shape_to_particle = dict()
COLORS = [
    (245, 0, 0),
    (250, 100, 100),
    (150, 20, 250),
    (250, 210, 10),
    (250, 150, 0),
    (245, 0, 0),
    (250, 250, 100),
    (255, 180, 180),
    (255, 255, 0),
    (100, 235, 10),
    (0, 185, 0),
]
ROOF_HEIGHT = 20
R_COLOR=(205, 153, 63)


class Particle:
    def __init__(self, pos, n, space, mapper):
        self.n = n % 11
        self.radius = RADII[self.n]
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = tuple(pos)
        self.shape = pymunk.Circle(body=self.body, radius=self.radius)
        self.shape.density = DENSITY
        self.shape.elasticity = ELASTICITY
        self.shape.collision_type = 1
        self.shape.friction = 0.2
        self.has_collided = False
        mapper[self.shape] = self
        space.add(self.body, self.shape)
        self.alive = True

    def draw(self, screen):
        if self.alive:
            c1 = np.array(COLORS[self.n])
            c2 = (c1 * 0.8).astype(int)

                # Dessiner le cercle du visage avec ombrage
            if self.n >= 4:
                pygame.draw.circle(screen, (100, 100, 100), (int(self.body.position[0] + self.radius * 0.05),
                                                            int(self.body.position[1] + self.radius * 0.05)),
                                   int(self.radius * 1))  # Ombrage
                pygame.draw.circle(screen, tuple(c2), self.body.position, self.radius)
                pygame.draw.circle(screen, tuple(c1), self.body.position, self.radius * 0.9)

            else:
                pygame.draw.circle(screen, (100, 100, 100), (int(self.body.position[0] + self.radius * 0.08),
                                                            int(self.body.position[1] + self.radius * 0.08)),
                                   int(self.radius * 1))  # Ombrage
                pygame.draw.circle(screen, tuple(c2), self.body.position, self.radius)
                pygame.draw.circle(screen, tuple(c1), self.body.position, self.radius * 0.9)

            # Calculer les positions des yeux et de la bouche
            eye_radius = int(self.radius * 0.15)
            eye_offset = int(self.radius * 0.2)
            mouth_radius = int(self.radius * 0.25)
            eye1_pos = (self.body.position[0] - eye_offset, self.body.position[1] - eye_offset)
            eye2_pos = (self.body.position[0] + eye_offset, self.body.position[1] - eye_offset)
            mouth_pos = (self.body.position[0], self.body.position[1] + int(self.radius * 0.2))

            # Dessiner les yeux
            eye_radius = int(self.radius * 0.15)
            eye_offset = int(self.radius * 0.2)
            eye1_pos = (self.body.position[0] - eye_offset, self.body.position[1] - eye_offset)
            eye2_pos = (self.body.position[0] + eye_offset, self.body.position[1] - eye_offset)
            pygame.draw.circle(screen, (0, 0, 0), eye1_pos, eye_radius)
            pygame.draw.circle(screen, (0, 0, 0), eye2_pos, eye_radius)

            # Dessiner la bouche (sourire)
            if self.n != 4:  # Ne dessine pas la bouche pour la boule orange (indice 4)
                pygame.draw.arc(screen, (0, 0, 0), (self.body.position[0] - self.radius * 0.5,
                                                   self.body.position[1] - self.radius * 0.3,
                                                   self.radius, self.radius * 0.6), np.pi, 2 * np.pi, int(self.radius * 4))
            else:
                # Dessiner une bouche spéciale pour la boule orange
                pygame.draw.arc(screen, (0, 0, 0), (self.body.position[0] - self.radius * 0.5,
                                                   self.body.position[1] - self.radius * 0.2,
                                                   self.radius, self.radius * 0.4), 0, np.pi, int(self.radius * 0.15))
                
    def get_texture_color(self):
        # Générer une couleur procédurale basée sur le type de fruit (n)
        color_intensity = 150 + self.n * 20
        return color_intensity, color_intensity, color_intensity
    
    def kill(self, space):
        space.remove(self.body, self.shape)
        self.alive = False
        print(f"Particle {id(self)} killed")

    @property
    def pos(self):
        return np.array(self.body.position)


class PreParticle:
    def __init__(self, x, n):
        self.n = n % 11
        self.radius = RADII[self.n]
        self.x = x
        
        print(f"PreParticle {id(self)} created")

    def draw(self, screen):
        c1 = np.array(COLORS[self.n])
        c2 = (c1 * 0.8).astype(int)
        pygame.draw.circle(screen, tuple(c2), (self.x, PAD[1] // 2), self.radius)
        pygame.draw.circle(screen, tuple(c1), (self.x, PAD[1] // 2), self.radius * 0.9)

        # Dessiner les yeux
        eye_radius = int(self.radius * 0.15)
        eye_offset = int(self.radius * 0.2)
        eye1_pos = (self.x - eye_offset, PAD[1] // 2 - eye_offset)
        eye2_pos = (self.x + eye_offset, PAD[1] // 2 - eye_offset)
        pygame.draw.circle(screen, (0, 0, 0), eye1_pos, eye_radius)
        pygame.draw.circle(screen, (0, 0, 0), eye2_pos, eye_radius)

        if self.n != 4:  # Ne dessine pas la bouche pour la boule orange (indice 4)
            pygame.draw.arc(screen, (0, 0, 0), (self.x - self.radius * 0.5,
                                               PAD[1] // 2 - self.radius * 0.3,
                                               self.radius, self.radius * 0.6), np.pi, 2 * np.pi, int(self.radius * 4))
        else :
            pygame.draw.arc(screen, (0, 0, 0), (self.x - self.radius * 0.5,
                                               PAD[1] // 2 - self.radius * 0.2,
                                               self.radius, self.radius * 0.4), 0, np.pi, int(self.radius * 0.15))

    def set_x(self, x):
        lim = PAD[0] + self.radius + THICKNESS // 2
        self.x = np.clip(x, lim, WIDTH - lim)

    def release(self, space, mapper):
        return Particle((self.x, PAD[1] // 2), self.n, space, mapper)


class Wall:
    thickness = THICKNESS

    def __init__(self, a, b, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, a, b, self.thickness // 2)
        self.shape.friction = 10
        space.add(self.body, self.shape)
        print(f"wall {self.shape.friction=}")

    def draw(self, screen):
        pygame.draw.line(screen, W_COLOR, self.shape.a, self.shape.b, self.thickness)

def resolve_collision(p1, p2, space, particles, mapper):
    if p1.n == p2.n:
        distance = np.linalg.norm(p1.pos - p2.pos)
        if distance < 2 * p1.radius:
            p1.kill(space)
            p2.kill(space)
            pn = Particle(np.mean([p1.pos, p2.pos], axis=0), p1.n+1, space, mapper)
            for p in particles:
                if p.alive:
                    vector = p.pos - pn.pos
                    distance = np.linalg.norm(vector)
                    if distance < pn.radius + p.radius:
                        impulse = IMPULSE * vector / (distance ** 2)
                        p.body.apply_impulse_at_local_point(tuple(impulse))
                        print(f"{impulse=} was applied to {id(p)}")
            return pn
    return None

class Roof:
    thickness = THICKNESS

    def __init__(self, a, b, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, a, b, self.thickness // 2)
        self.shape.friction = 10
        self.shape.sensor = True  # Définir le toit comme capteur
        space.add(self.body, self.shape)
        print(f"roof {self.shape.friction=}")

    def draw(self, screen):
        pygame.draw.line(screen, R_COLOR, self.shape.a, self.shape.b, self.thickness)


# Créé la page pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PySuika")
clock = pygame.time.Clock()
pygame.font.init()
scorefont = pygame.font.SysFont("monospace", 32)
overfont = pygame.font.SysFont("monospace", 72)

space = pymunk.Space()
space.gravity = (0, GRAVITY)
space.damping = DAMPING
space.collision_bias = BIAS
print(f"{space.damping=}")
print(f"{space.collision_bias=}")
print(f"{space.collision_slop=}")

# Murs
pad = 20
left = Wall((PAD[0], PAD[1] - ROOF_HEIGHT), B, space)
bottom = Wall(B, C, space)
right = Wall(C, (WIDTH - PAD[0], PAD[1] - ROOF_HEIGHT), space)
walls = [left, bottom, right]
roof = Roof((PAD[0], PAD[1] - ROOF_HEIGHT), (WIDTH - PAD[0], PAD[1] - ROOF_HEIGHT), space)

# Dessiner les murs
for w in walls:
    w.draw(screen)

# Liste pour stocker les fruits
wait_for_next = 0
next_particle = PreParticle(WIDTH//2, rng.integers(0, 5))
particles = []

# Collisions
handler = space.add_collision_handler(1, 1)


def collide(arbiter, space, data):
    sh1, sh2 = arbiter.shapes
    _mapper = data["mapper"]
    pa1 = _mapper[sh1]
    pa2 = _mapper[sh2]
    cond = bool(pa1.n != pa2.n)
    pa1.has_collided = cond
    pa2.has_collided = cond
    if not cond:
        new_particle = resolve_collision(pa1, pa2, space, data["particles"], _mapper)
        data["particles"].append(new_particle)
        data["score"] += POINTS[pa1.n]
    return cond


handler.begin = collide
handler.data["mapper"] = shape_to_particle
handler.data["particles"] = particles
handler.data["score"] = 0

# Boucle principale du jeu
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                particles.append(next_particle.release(space, shape_to_particle))
                wait_for_next = NEXT_DELAY
            elif event.key in [pygame.K_q, pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and wait_for_next == 0:
            particles.append(next_particle.release(space, shape_to_particle))
            wait_for_next = NEXT_DELAY

    next_particle.set_x(pygame.mouse.get_pos()[0])

    if wait_for_next > 1:
        wait_for_next -= 1
    elif wait_for_next == 1:
        next_particle = PreParticle(next_particle.x, rng.integers(0,5))
        wait_for_next -= 1

    # Dessine le fond et les particules
    screen.fill(BG_COLOR)
    if wait_for_next == 0:
        next_particle.draw(screen)
    for w in walls:
        w.draw(screen)
    roof.draw(screen)
    for p in particles:
        p.draw(screen)
        if p.pos[1] < PAD[1] and p.has_collided:
            label = overfont.render("Game Over!", 1, (0, 0, 0))
            screen.blit(label, PAD)
            game_over = True
    label = scorefont.render(f"Score: {handler.data['score']}", 1, (0, 0, 0))
    screen.blit(label, (10, 10))

    space.step(1/FPS)
    pygame.display.update()
    clock.tick(FPS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_q, pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()