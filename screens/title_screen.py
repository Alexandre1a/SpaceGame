import pygame
from screens.base_screen import Screen
from ui.button import Button
from ressources.ressources import getMusicPath


class TitleScreen(Screen):
    def __init__(self, game, width, height, font, titleFont):
        self._game = game
        self._font = font
        self._fontTitle = titleFont

        centerX = width // 2
        startY = height // 2 - 100

        self._buttons = [
            Button(
                "Jouer",
                (centerX, startY),
                game.displayStartOptions,
                font,
            ),
            Button(
                "Sélection Vaisseau",
                (centerX, startY + 60),
                game.displayShipSelection,
                font,
            ),
            Button(
                "Paramètres",
                (centerX, startY + 120),
                game.displaySettingsScreen,
                font,
            ),
            Button(
                "Quitter",
                (centerX, startY + 180),
                game.quit,
                font,
            ),
        ]

    def onEnter(self):
      pygame.mixer.music.stop()
      pygame.mixer.music.load(getMusicPath("menu.wav"))
      pygame.mixer.music.play(-1)

    def handleEvent(self, event):
        for button in self._buttons:
            button.handleEvent(event)

    def update(self, dt):
      # Static screen
      pass

    def render(self, surface):
      surface.fill((5, 5, 20))

      titleText = self._fontTitle.render("SPACE GAME", True, (100, 200, 255))
      titleRect = titleText.get_rect(center=(surface.get_width() // 2, 80))
      surface.blit(titleText, titleRect)

      money = self._game.getMoney()
      moneyText = self._font.render(
          f"Crédits disponibles : {money:,} ¢",
          True,
          (255, 215, 0),
      )
      moneyRect = moneyText.get_rect(center=(surface.get_width() // 2, 150))

      bgRect = moneyRect.inflate(20, 10)
      bgSurface = pygame.Surface(bgRect.size, pygame.SRCALPHA)
      bgSurface.fill((255, 255, 0, 128))
      surface.blit(bgSurface, bgRect)
      surface.blit(moneyText, moneyRect)

      selectedShip = self._game.getSelectedShip()
      if selectedShip:
          shipName = selectedShip.getName()
          shipInfoText = f"Vaisseau : {shipName}"
      else:
          shipInfoText = "Aucun vaisseau sélectionné"

      shipText = self._font.render(shipInfoText, True, (150, 150, 255))
      shipRect = shipText.get_rect(center=(surface.get_width() // 2, 200))
      surface.blit(shipText, shipRect)

      for button in self._buttons:
          button.render(surface)

      versionText = self._font.render("v1.2.4", True, (80, 80, 80))
      versionRect = versionText.get_rect(
          bottomright=(surface.get_width() - 10, surface.get_height() - 10)
      )
      surface.blit(versionText, versionRect)
