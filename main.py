# Importieren der Pygame-Bibliothek
import pygame

# initialisieren von pygame
pygame.init()

# genutzte Farbe
ORANGE  = ( 255, 140, 0)
RED     = ( 255, 0, 0)
GREEN   = ( 0, 255, 0)
BLACK = ( 0, 0, 0)
WHITE   = ( 255, 255, 255)

# Fenster öffnen
pygame.display.set_mode((640, 480))

# Titel für Fensterkopf
pygame.display.set_caption("Game Jam")

# solange die Variable True ist, soll das Spiel laufen
active = True

# Schleife Hauptprogramm
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False