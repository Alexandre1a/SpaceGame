import random
from gameplay.quests.delivery import DeliveryQuest

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
        print("[QuestManager] Generated ", len(self.questList), "quests with destination", [q.destination.name for q in self.questList], "\nand source ", [q.giver.name for q in self.questList])
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
        # Quest is unavailable (completed)
        pass

    def completeQuest(self, planet):
      for i in range(len(self.questList)):
        if planet.name == self.questList[i].giver.name:
          id = i
        else:
          pass

      if planet.name == self.questList[id].destination.name:
        self.questList[id].completed = True
        print("[QuestManager] Completed ", self.questList[id].objective)
        self.game.phtonos.add(self.game, self.questList[id].reward)
