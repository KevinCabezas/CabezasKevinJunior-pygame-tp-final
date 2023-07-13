import pygame
from constantes import*
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y,ruta):
		super().__init__()
		self.image = pygame.image.load(ruta)
		# self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.y = y +50
		self.rect.centerx = x +1
		self.speedy = 13

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()