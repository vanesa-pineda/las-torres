import pygame
import time

# Inicializar pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Tamaño de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Torres de Hanói")

# Tamaño de los discos y las torres
DISK_WIDTH = 80
DISK_HEIGHT = 20
TOWER_WIDTH = 20
TOWER_HEIGHT = 300

# Fuentes
font = pygame.font.SysFont('Arial', 30)

# Torrecillas y discos
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.disks = []

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x - TOWER_WIDTH // 2, self.y, TOWER_WIDTH, TOWER_HEIGHT))
        for i, disk in enumerate(self.disks):
            disk.draw(self.x, self.y + (len(self.disks) - i - 1) * DISK_HEIGHT)

    def add_disk(self, disk):
        self.disks.append(disk)

    def remove_disk(self):
        return self.disks.pop()

class Disk:
    def __init__(self, size, color):
        self.size = size
        self.color = color

    def draw(self, x, y):
        pygame.draw.rect(screen, self.color, (x - self.size // 2, y, self.size, DISK_HEIGHT))

# Colores para los discos
disk_colors = [RED, GREEN, BLUE, ORANGE, YELLOW]

# Función para mover el disco
def move_disk(from_tower, to_tower):
    if from_tower.disks:
        disk = from_tower.remove_disk()
        to_tower.add_disk(disk)

# Función para verificar si el juego ha terminado
def check_win(towers):
    return len(towers[2].disks) == len(disk_colors)

# Inicialización del juego
towers = [Tower(200, 100), Tower(400, 100), Tower(600, 100)]
disks = [Disk(DISK_WIDTH * (i + 1), disk_colors[i]) for i in range(len(disk_colors))]
for disk in reversed(disks):
    towers[0].add_disk(disk)

# Variables para el control del juego
selected_disk = None
moves = 0
running = True

# Bucle principal del juego
while running:
    screen.fill(WHITE)

    # Dibujar las torres y los discos
    for tower in towers:
        tower.draw()

    # Contar movimientos
    move_text = font.render(f'Movimientos: {moves}', True, BLACK)
    screen.blit(move_text, (10, 10))

    # Comprobar si el jugador ha ganado
    if check_win(towers):
        win_text = font.render('¡Has ganado!', True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(2)
        running = False

    # Manejar eventos de usuario
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for tower in towers:
                if tower.x - TOWER_WIDTH // 2 <= mouse_x <= tower.x + TOWER_WIDTH // 2 and tower.y <= mouse_y <= tower.y + TOWER_HEIGHT:
                    if selected_disk:
                        # Si ya hay un disco seleccionado, intenta moverlo
                        if tower == selected_disk[1]:
                            continue
                        move_disk(selected_disk[1], tower)
                        moves += 1
                        selected_disk = None
                    elif tower.disks:
                        # Selecciona el disco superior
                        selected_disk = (tower.disks[-1], tower)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
