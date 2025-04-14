import pygame
import random

# 初期設定
pygame.init()
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("テトリス")
clock = pygame.time.Clock()

# カラー設定
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]

# テトリスの形
shapes = [
    [[1, 1, 1], [0, 1, 0]],  # T字
    [[1, 1], [1, 1]],        # 正方形
    [[1, 1, 1, 1]]           # I字
]

# ボード設定
board = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]

# ブロッククラス
class Block:
    def __init__(self):
        self.shape = random.choice(shapes)
        self.color = random.randint(1, len(colors) - 1)
        self.x = WIDTH // BLOCK_SIZE // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def collision(self, dx, dy):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.x + x + dx, self.y + y + dy
                    if nx < 0 or nx >= WIDTH // BLOCK_SIZE or ny >= HEIGHT // BLOCK_SIZE or board[ny][nx]:
                        return True
        return False

    def place(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    board[self.y + y][self.x + x] = self.color

# ライン消去
def clear_lines():
    global board
    board = [row for row in board if any(cell == 0 for cell in row)]
    while len(board) < HEIGHT // BLOCK_SIZE:
        board.insert(0, [0] * (WIDTH // BLOCK_SIZE))

# ゲームループ
running = True
block = Block()
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        # ゲームオーバー判定
        if event.type == pygame.QUIT:
            running = False
        # キー入力判定
        if event.type == pygame.KEYDOWN:
            # 左キー(移動)
            if event.key == pygame.K_LEFT and not block.collision(-1, 0):
                block.x -= 1
            # 右キー(移動)
            if event.key == pygame.K_RIGHT and not block.collision(1, 0):
                block.x += 1
            # 下キー(下降)
            if event.key == pygame.K_DOWN and not block.collision(0, 1):
                block.y += 1
            # 上キー(回転)
            if event.key == pygame.K_UP:
                block.rotate()

    # 自動でブロックを落下
    if not block.collision(0, 1):
        block.y += 1
    else:
        block.place()
        clear_lines()
        block = Block()
        # 新しいブロックが置けない場合ゲームオーバー
        if block.collision(0, 0):
            running = False

    # ボード描画
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            pygame.draw.rect(screen, colors[cell], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # ブロック描画
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, colors[block.color], ((block.x + x) * BLOCK_SIZE, (block.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
