import math
import random
import pygame

WIDTH = 960
HEIGHT = 640
FPS = 60

PLAYER_SPEED = 280
BULLET_SPEED = 700
ENEMY_SPEED = 120
ENEMY_FIRE_RATE = 1.8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brawl Stars 3D Prototype")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)


def draw_perspective_floor(surface):
    # Simulate a 3D arena floor with perspective lines.
    colors = [(30, 30, 40), (40, 40, 60)]
    for i in range(20):
        color = colors[i % 2]
        y = HEIGHT * 0.25 + i * ((HEIGHT * 0.75) / 20)
        pygame.draw.rect(surface, color, (0, y, WIDTH, (HEIGHT * 0.75) / 20))
    horizon_y = HEIGHT * 0.25
    for x in range(0, WIDTH + 1, 80):
        pygame.draw.line(surface, (80, 80, 110), (x, HEIGHT), (WIDTH // 2, horizon_y), 1)
    pygame.draw.line(surface, (120, 120, 155), (0, horizon_y), (WIDTH, horizon_y), 3)


class Bullet:
    def __init__(self, x, y, angle, owner):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * BULLET_SPEED
        self.radius = 5
        self.owner = owner
        self.life = 2.2

    def update(self, dt):
        self.pos += self.vel * dt
        self.life -= dt

    def draw(self, surface, camera_offset):
        pos = self.pos - camera_offset
        if 0 <= pos.x <= WIDTH and 0 <= pos.y <= HEIGHT:
            pygame.draw.circle(surface, (255, 220, 80), (int(pos.x), int(pos.y)), self.radius)


class Actor:
    def __init__(self, x, y, color, speed):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.color = color
        self.speed = speed
        self.radius = 24
        self.health = 100
        self.reload = 0

    def is_alive(self):
        return self.health > 0

    def draw(self, surface, camera_offset, angle=0):
        pos = self.pos - camera_offset
        if 0 <= pos.x <= WIDTH and 0 <= pos.y <= HEIGHT:
            size = int(self.radius * (1 + (pos.y - HEIGHT * 0.1) / HEIGHT * 0.1))
            pygame.draw.circle(surface, self.color, (int(pos.x), int(pos.y)), size)
            tip = pygame.Vector2(math.cos(angle), math.sin(angle)) * (size + 10)
            pygame.draw.line(surface, (255, 255, 255), (int(pos.x), int(pos.y)), (int(pos.x + tip.x), int(pos.y + tip.y)), 3)
            pygame.draw.rect(surface, (0, 0, 0), (pos.x - 30, pos.y + size + 8, 60, 8), border_radius=4)
            pygame.draw.rect(surface, (60, 255, 120), (pos.x - 29, pos.y + size + 9, 58 * max(self.health, 0) / 100, 6), border_radius=3)


class Player(Actor):
    def update(self, dt, keys, mouse_pos, bullets):
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.vel = direction * self.speed
        self.pos += self.vel * dt
        self.pos.x = max(80, min(880, self.pos.x))
        self.pos.y = max(120, min(560, self.pos.y))
        self.reload = max(0, self.reload - dt)

        if pygame.mouse.get_pressed()[0] and self.reload == 0:
            aim = pygame.Vector2(mouse_pos) - (self.pos - camera_offset)
            if aim.length_squared() > 0:
                angle = math.atan2(aim.y, aim.x)
                bullets.append(Bullet(self.pos.x, self.pos.y, angle, self))
                self.reload = 0.16

    def draw(self, surface, camera_offset):
        mouse = pygame.mouse.get_pos()
        aim = pygame.Vector2(mouse) - (self.pos - camera_offset)
        angle = math.atan2(aim.y, aim.x)
        super().draw(surface, camera_offset, angle)


class Enemy(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, (220, 100, 100), ENEMY_SPEED)
        self.fire_timer = random.uniform(0.3, ENEMY_FIRE_RATE)

    def update(self, dt, player, bullets):
        direction = player.pos - self.pos
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.pos += direction * self.speed * dt
        self.fire_timer -= dt
        if self.fire_timer <= 0:
            angle = math.atan2(direction.y, direction.x)
            bullets.append(Bullet(self.pos.x, self.pos.y, angle, self))
            self.fire_timer = ENEMY_FIRE_RATE


def draw_hud(surface, player, score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    health_text = font.render(f"Health: {int(player.health)}", True, (255, 255, 255))
    surface.blit(score_text, (14, 14))
    surface.blit(health_text, (14, 42))
    pygame.draw.rect(surface, (60, 60, 70), (14, 70, 200, 18), border_radius=6)
    pygame.draw.rect(surface, (90, 200, 120), (16, 72, 1.96 * max(player.health, 0), 14), border_radius=5)


def spawn_enemy(actors):
    x = random.choice([random.randint(100, 860), random.choice([60, 900])])
    y = random.choice([random.randint(140, 560), random.choice([100, 620])])
    actors.append(Enemy(x, y))


player = Player(WIDTH // 2, HEIGHT // 2 + 40, (80, 180, 240), PLAYER_SPEED)
bullets = []
enemies = [Enemy(160, 160), Enemy(800, 520), Enemy(240, 520)]
score = 0
spawn_timer = 0.0
running = True

while running:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    camera_offset = pygame.Vector2(player.pos.x - WIDTH * 0.5, player.pos.y - HEIGHT * 0.5)
    player.update(dt, keys, pygame.mouse.get_pos(), bullets)

    for enemy in enemies:
        if enemy.is_alive():
            enemy.update(dt, player, bullets)

    for bullet in bullets[:]:
        bullet.update(dt)
        if bullet.life <= 0:
            bullets.remove(bullet)
            continue
        if bullet.owner is not player and (bullet.pos - player.pos).length() < player.radius:
            player.health -= 18
            bullets.remove(bullet)
        for enemy in enemies:
            if enemy.is_alive() and bullet.owner is player and (bullet.pos - enemy.pos).length() < enemy.radius:
                enemy.health -= 40
                bullets.remove(bullet)
                if enemy.health <= 0:
                    score += 55
                break

    enemies = [enemy for enemy in enemies if enemy.is_alive()]
    if player.health <= 0:
        running = False

    spawn_timer += dt
    if spawn_timer >= 2.2:
        spawn_enemy(enemies)
        spawn_timer = 0

    screen.fill((24, 24, 34))
    draw_perspective_floor(screen)
    for _ in range(5):
        pygame.draw.circle(screen, (255, 255, 255), (random.randint(0, WIDTH), random.randint(HEIGHT // 4, HEIGHT)), 2)
    for enemy in enemies:
        enemy.draw(screen, camera_offset, math.atan2(player.pos.y - enemy.pos.y, player.pos.x - enemy.pos.x))
    for bullet in bullets:
        bullet.draw(screen, camera_offset)
    player.draw(screen, camera_offset)
    draw_hud(screen, player, score)

    if player.health <= 0:
        game_over = font.render("GAME OVER - Press ESC to exit", True, (255, 80, 80))
        screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 2 - 20))

    pygame.display.flip()

    if keys[pygame.K_ESCAPE]:
        running = False

pygame.quit()
