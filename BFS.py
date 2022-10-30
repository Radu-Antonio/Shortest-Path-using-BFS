import pygame, sys, queue

pygame.init()
pygame.display.set_caption('BFS')
SCREEN_SIZE, SQUARE_SIZE = 800, 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (52, 52, 52)
GREEN = (44, 157, 23)
RED = (230, 25, 25)

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
grid = [[0] * (SCREEN_SIZE // SQUARE_SIZE) for _ in range(SCREEN_SIZE // SQUARE_SIZE)]
prev = [[0] * (SCREEN_SIZE // SQUARE_SIZE) for _ in range(SCREEN_SIZE // SQUARE_SIZE)]
q = queue.Queue()
stage = 0
target = (-1, -1)
fpsclock = pygame.time.Clock()

def draw(x, y, color):
	pygame.draw.rect(screen, color, (x * SQUARE_SIZE + 1, y * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

def main():
	global stage, target
	screen.fill(WHITE)
	size = len(grid)
	for i in range(size):
		for j in range(size):
			pygame.draw.rect(screen, GRAY, (j * SQUARE_SIZE + 1, i * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if pygame.mouse.get_pressed()[0] and stage == 0:
				x, y = pygame.mouse.get_pos()
				x //= SQUARE_SIZE
				y //= SQUARE_SIZE
				grid[x][y] = -1
				draw(x, y, BLACK)

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and stage == 0:
				stage += 1
			
			if event.type == pygame.MOUSEBUTTONUP and stage == 2:
				x, y = pygame.mouse.get_pos()
				x //= SQUARE_SIZE
				y //= SQUARE_SIZE
				draw(x, y, GREEN)
				stage += 1
				target = (x, y)

			if event.type == pygame.MOUSEBUTTONUP and stage == 1:
				x, y = pygame.mouse.get_pos()
				x //= SQUARE_SIZE
				y //= SQUARE_SIZE
				grid[x][y] = 1
				q.put((x, y))
				prev[x][y] = (-1, -1)
				draw(x, y, GREEN)
				stage += 1

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and stage == 3:
				stage += 1
				done = False

				while not q.empty() and not done:
					currX, currY = q.get()
					for x, y in [(1,0), (0,1), (-1,0), (0,-1)]:
						a = currX + x
						b = currY + y

						if (a, b) == target:
							prev[a][b] = (currX, currY)
							done = True
							break

						if 0 <= a < len(grid) and 0 <= b < len(grid) and grid[a][b] == 0:
							grid[a][b] = 1
							prev[a][b] = (currX, currY)
							q.put((a, b)) 
							draw(a, b, RED)

					fpsclock.tick(60)
					pygame.display.update()

				if prev[target[0]][target[1]]:
					back = target
					while back != (-1, -1):
						draw(back[0], back[1], GREEN)
						back = prev[back[0]][back[1]]

		fpsclock.tick(60)
		pygame.display.update()

if __name__ == "__main__":
	main()