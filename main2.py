from menu import Menu
import pygame
pygame.init()
MENU_PRINCIPAL = "menu_principal"
JUGAR = "jugar"
OPCIONES = "opciones"
# Agrega más estados según las pantallas de tu juego
def main():
    ejecutando = True
    estado_actual = True
    while ejecutando:
        if MENU_PRINCIPAL:
            menu = Menu()
            menu.menu_inicio()
        # elif estado_actual == JUGAR:
        #     jugar()
        # elif estado_actual == OPCIONES:
        #     opciones()
        # Agrega más condicionales según tus estados de juego

        # Actualiza la pantalla y realiza otras operaciones necesarias
main()