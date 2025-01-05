import pygame
import random
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tree Planting Game")
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BLUE = (135, 206, 250)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
clock = pygame.time.Clock()
FPS = 60
player_size = 20
player_color = (0, 0, 255)
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
trees = []
tree_types = {
    "oak": {"growth_rate": 1, "max_radius": 30, "color": GREEN},
    "pine": {"growth_rate": 2, "max_radius": 25, "color": (0, 100, 0)},
    "baobab": {"growth_rate": 0.5, "max_radius": 40, "color": (85, 107, 47)},
}
water_drops = []
WATER_DROP_RADIUS = 10
WATER_DROP_SPAWN_TIME = 5 * FPS
water_timer = 0
machines = []
MACHINE_SIZE = 40
MACHINE_SPEED = 1
MACHINE_SPAWN_TIME = 20 * FPS
machine_timer = 0
font = pygame.font.SysFont("Arial", 20)
running = True
score = 0
water_level = 100
def draw_player():
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))
def plant_tree(x, y, tree_type):
    trees.append({"x": x, "y": y, "radius": 5, "type": tree_type, "time_planted": pygame.time.get_ticks()})
def grow_trees():
    current_time = pygame.time.get_ticks()
    for tree in trees:
        if water_level > 0:
            elapsed_time = current_time - tree["time_planted"]
            growth_rate = tree_types[tree["type"]]["growth_rate"]
            if elapsed_time >= 1000 / growth_rate:
                tree["radius"] += 1
                tree["time_planted"] = current_time
                if tree["radius"] > tree_types[tree["type"]]["max_radius"]:
                    tree["radius"] = tree_types[tree["type"]]["max_radius"]

def draw_trees():
    for tree in trees:
        tree_color = tree_types[tree["type"]]["color"]
        pygame.draw.circle(screen, BROWN, (tree["x"], tree["y"]), tree["radius"])
        pygame.draw.circle(screen, tree_color, (tree["x"], tree["y"] - tree["radius"] // 2), tree["radius"] // 2)

def spawn_water_drops():
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    water_drops.append({"x": x, "y": y})
def draw_water_drops():
    for drop in water_drops:
        pygame.draw.circle(screen, CYAN, (drop["x"], drop["y"]), WATER_DROP_RADIUS)
      
def spawn_machine():
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    machines.append({"x": x, "y": y, "dx": random.choice([-MACHINE_SPEED, MACHINE_SPEED]), "dy": random.choice([-MACHINE_SPEED, MACHINE_SPEED])})

def draw_machines():
    for machine in machines:
        pygame.draw.rect(screen, RED, (machine["x"], machine["y"], MACHINE_SIZE, MACHINE_SIZE))

def move_machines():
    for machine in machines:
        machine["x"] += machine["dx"]
        machine["y"] += machine["dy"]
        if machine["x"] <= 0 or machine["x"] >= SCREEN_WIDTH - MACHINE_SIZE:
            machine["dx"] *= -1
        if machine["y"] <= 0 or machine["y"] >= SCREEN_HEIGHT - MACHINE_SIZE:
            machine["dy"] *= -1

def check_collisions():
    global water_level, score
    for drop in water_drops[:]:
        if pygame.Rect(player_pos[0], player_pos[1], player_size, player_size).colliderect(
            pygame.Rect(drop["x"] - WATER_DROP_RADIUS, drop["y"] - WATER_DROP_RADIUS, WATER_DROP_RADIUS * 2, WATER_DROP_RADIUS * 2)):
            water_drops.remove(drop)
            water_level += 20
            if water_level > 100:
                water_level = 100

    for machine in machines:
        for tree in trees[:]:
            distance = ((machine["x"] + MACHINE_SIZE // 2 - tree["x"]) ** 2 + (machine["y"] + MACHINE_SIZE // 2 - tree["y"]) ** 2) ** 0.5
            if distance < tree["radius"] + MACHINE_SIZE // 2:
                trees.remove(tree)
                score -= 5

def destroy_machines():
    global score
    for machine in machines[:]:
        if pygame.Rect(player_pos[0], player_pos[1], player_size, player_size).colliderect(
            pygame.Rect(machine["x"], machine["y"], MACHINE_SIZE, MACHINE_SIZE)):
            machines.remove(machine)
            score += 20

while running:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tree_type = random.choice(list(tree_types.keys()))
                plant_tree(player_pos[0] + player_size // 2, player_pos[1] + player_size // 2, tree_type)
                score += 10
            if event.key == pygame.K_k:
                destroy_machines()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size:
        player_pos[1] += player_speed
    water_timer += 1
    if water_timer >= WATER_DROP_SPAWN_TIME:
        spawn_water_drops()
        water_timer = 0
    machine_timer += 1
    if machine_timer >= MACHINE_SPAWN_TIME:
        spawn_machine()
        machine_timer = 0
    if machine_timer % 100 == 0:
        MACHINE_SPAWN_TIME = max(10 * FPS, MACHINE_SPAWN_TIME - 1)
    water_level -= 0.1
    if water_level < 0:
        water_level = 0

    move_machines()
    grow_trees()
    draw_player()
    draw_trees()
    draw_water_drops()
    draw_machines()
    check_collisions()
    score_text = font.render(f"Score: {score}", True, WHITE)
    water_text = font.render(f"Water Level: {int(water_level)}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(water_text, (10, 40))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
