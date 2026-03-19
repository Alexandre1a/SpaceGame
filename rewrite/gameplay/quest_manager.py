import random
from gameplay.quests.delivery import DeliveryQuest
from gameplay.quest import Quest
from entities.planet import Planet
import pygame

class QuestManager:

    def __init__(self, game):
      """
        Has access to the whole game context
      """
      self.game = game
      self.questList = []
      self.loadQuests()
      self.currentQuest = self.questList[0]

    def getActiveQuest(self):
      return self.currentQuest.objective

    def loadQuests(self):
      self.data = self.game.getSaveData()

      if self.data is None:
        for i in range(len(self.game.gameScreen.planets)):
          quest = DeliveryQuest("Deliver", self.game.gameScreen.planets[i], self.game, 10, random.choice(self.game.gameScreen.planets), i)
          self.questList.append(quest)
        print("[QuestManager] Generated ", len(self.questList), "quests with destination", [q.destination.name for q in self.questList], "\nand source ", [q.giver.name for q in self.questList]," and id ", [p.id for p in self.questList])
      else: pass

    def checkPlanetIsGiver(self, planet):
      for i in range(len(self.questList)):
        if planet.name == self.questList[i].giver.name:
          return True
        else:
          pass
      return False

    def checkPlanetIsTarget(self, planet):
      for i in self.questList:
        if planet.name == self.currentQuest.destination.name:
          return True
        else:
          pass
      return False

    def acceptQuest(self, planet):
      print("[QuestManager] Attempting to accept quest...")
      # Need to verfy is quest is avaliable
      # Planet is used to get questID (source is unique)
      for i in range(len(self.questList)):
        if planet.name == self.questList[i].giver.name:
          id = i
        else:
          pass
      if self.questList[id].completed != True:
        self.currentQuest = self.questList[id]
      else:
        planet.buttons[0].setDisabled(True)
        # Quest is unavailable (completed)


    def completeQuest(self, planet):
      print("[QuestManager] Attempting to complete quest...")
      for i in range(len(self.questList)):
        if planet.name == self.questList[i].giver.name:
          id = i
        else:
          pass
      if id is None:
        print("[QuestManager] ", planet.name, " has no quest !")

      if planet.name == self.questList[id].destination.name:
        if not self.questList[id].completed:
          self.questList[id].completed = True
          print("[QuestManager] Completed ", self.questList[id].objective)
          self.game.phtonos.add(self.game, self.questList[id].reward)
          planet.buttons[1].setDisabled(True)
          self.currentQuest = Quest("None", Planet(pygame.Vector2(0,0), 0, (0,0,0)), self.game, 0, 5948372)  # Dummy Quest
        else:
          planet.buttons[1].setDisabled(True)
      print("[QuestManager] Current global quest states:\n", [q.destination.name for q in self.questList], '\n', [q.giver.name for q in self.questList], '\n', [p.id for p in self.questList], '\n', [p.completed for p in self.questList])
