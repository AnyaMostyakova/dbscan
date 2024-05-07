import pygame
import math

# Инициализация Pygame
pygame.init()

# Создание окна
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("DBSCAN Clustering")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CLUSTER_COLORS = [RED, GREEN, BLUE, YELLOW, (255, 0, 255), (0, 255, 255)]  # Цвета для кластеров

# Список точек
dots = []

# Класс для представления точки
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cluster = None  # Кластер, к которому принадлежит точка (None, если не определен)
        self.flag_color = BLACK  # Цвет "флажка" для точки

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

# Функция для отрисовки точек
def draw_dots():
    for dot in dots:
        color = dot.flag_color if dot.cluster is None else CLUSTER_COLORS[dot.cluster % len(CLUSTER_COLORS)]
        pygame.draw.circle(screen, color, (dot.x, dot.y), 3)

# Функция для вычисления евклидова расстояния между двумя точками
def euclidean_distance(d1, d2):
    return math.sqrt((d1.x - d2.x)**2 + (d1.y - d2.y)**2)

# Функция для поиска всех точек в заданном радиусе eps от точки d
def region_query(d, eps):
    neighbors = []
    for dot in dots:
        if euclidean_distance(d, dot) <= eps:
            neighbors.append(dot)
    return neighbors

# Функция для расширения кластера
def expand_cluster(d, neighbors, cluster_id, eps, min_pts):
    cluster = [d]
    for neighbor in neighbors:
        if neighbor.cluster is None:  # Если точка не принадлежит ни одному кластеру
            neighbor.cluster = cluster_id  # Добавляем ее в текущий кластер
            cluster.append(neighbor)
            neighbor_neighbors = region_query(neighbor, eps)
            if len(neighbor_neighbors) >= min_pts:
                neighbors.extend(neighbor_neighbors)
    return cluster

# Функция для кластеризации точек с помощью DBSCAN
def dbscan(eps, min_pts):
    cluster_id = 0
    for dot in dots:
        if dot.cluster is None:  # Если точка не принадлежит ни одному кластеру
            neighbors = region_query(dot, eps)
            if len(neighbors) >= min_pts:  # Если точка является ядром
                dot.flag_color = GREEN  # Выдаем зеленый "флажок"
                cluster = expand_cluster(dot, neighbors, cluster_id, eps, min_pts)
                for d in cluster:
                    d.cluster = cluster_id
                    d.flag_color = GREEN  # Выдаем зеленый "флажок" всем точкам в кластере
                cluster_id += 1
            else:  # Если точка является шумом
                dot.flag_color = YELLOW  # Выдаем желтый "флажок"
                dot.cluster = -1  # Помечаем ее как шум

# Функция для выдачи "флажков" точкам
def assign_flags():
    for dot in dots:
        if dot.cluster is None:
            dot.flag_color = RED  # Выдаем красный "флажок" неклассифицированным точкам

# Главный цикл
running = True
flagging_mode = False  # Флаг для режима выдачи "флажков"
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Добавление новой точки при нажатии мыши
            x, y = event.pos
            dot = Dot(x, y)
            dots.append(dot)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flagging_mode = True  # Включаем режим выдачи "флажков"

                assign_flags()  # Выдаем "флажки" точкам
                dbscan(20, 3)  # Запускаем алгоритм DBSCAN

    # Очистка экрана
    screen.fill(WHITE)

    # Отрисовка точек
    draw_dots()

    # Обновление экрана
    pygame.display.flip()

    # Выход из режима выдачи "флажков"
    if flagging_mode:
        flagging_mode = False

# Завершение Pygame
pygame.quit()
