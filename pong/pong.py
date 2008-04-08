import sys, pygame
pygame.init()

pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1, 0.0)

p1score = 0
p2score = 0

first = True

size = width, height = 640, 480
speed = [4, 4]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png").convert()
p1 = pygame.image.load("paddle.png").convert()
p2 = pygame.image.load("paddle.png").convert()

ballrect = ball.get_rect(center=(320,240))
p1rect = p1.get_rect(center=(10,240))
p2rect = p2.get_rect(center=(630,240))

p1mov = [0,0]
p2mov = [0,0]

# Create a font
font1 = pygame.font.Font(None, 64)
text1 = font1.render(str(p1score), True, (255,255, 255))
font2 = pygame.font.Font(None, 64)
text2 = font2.render(str(p2score), True, (255,255, 255))

# Create a rectangle
textRect1 = text1.get_rect()
textRect1.topleft = [0,0]
textRect2 = text2.get_rect()
textRect2.topright = [width,0]

pygame.key.set_repeat(10, 4)

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				sys.exit()
			if event.key == pygame.K_DOWN:
				p2mov = [0,4]
			if event.key == pygame.K_UP:
				p2mov = [0,-4]
			if event.key == pygame.K_s:
				p1mov = [0,4]
			if event.key == pygame.K_w:
				p1mov = [0,-4]
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
				p2mov = [0,0]
			if event.key == pygame.K_s or event.key == pygame.K_w:
				p1mov = [0,0]

	ballrect = ballrect.move(speed)

	if p2rect.top < 0 and p2mov == [0,-4]:
		p2mov = [0,0]
	elif p2rect.bottom > height and p2mov == [0,4]:
		p2mov = [0,0]

	if p1rect.top < 0 and p1mov == [0,-4]:
		p1mov = [0,0]
	elif p1rect.bottom > height and p1mov == [0,4]:
		p1mov = [0,0]

	p2rect = p2rect.move(p2mov)
	p1rect = p1rect.move(p1mov)

	# ball collisions
	if ballrect.colliderect(p1rect) or ballrect.colliderect(p2rect):
		speed[0] = -speed[0]
	if ballrect.top < 0 or ballrect.bottom > height:
		speed[1] = -speed[1]

	# gg
	if ballrect.right > width:
		p1score += 1
		text1 = font1.render(str(p1score), True, (255,255, 255))
		textRect1 = text1.get_rect()
		textRect1.topleft = [0,0]
		speed[0] = -speed[0]

		pygame.time.wait(1000)
		ballrect = ball.get_rect(center=(320,240))
		p1rect = p1.get_rect(center=(10,240))
		p2rect = p2.get_rect(center=(630,240))

		first = True
	if ballrect.left < 0:
		p2score += 1
		text2 = font2.render(str(p2score), True, (255,255, 255))
		textRect2 = text2.get_rect()
		textRect2.topright = [width,0]
		speed[0] = -speed[0]

		pygame.time.wait(1000)
		ballrect = ball.get_rect(center=(320,240))
		p1rect = p1.get_rect(center=(10,240))
		p2rect = p2.get_rect(center=(630,240))

		first = True

	screen.fill(black)

	screen.blit(ball, ballrect)
	screen.blit(p1, p1rect)
	screen.blit(p2, p2rect)
	screen.blit(text1, textRect1)
	screen.blit(text2, textRect2)

	pygame.display.flip()

	if first:
		pygame.time.wait(500)
		first = False
