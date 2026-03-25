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
    self.currentQuest = None

  def getActiveQuest(self):
    if self.currentQuest is None:
      return "No active quest"
    return self.currentQuest.objective

  def getActiveQuestPos(self):
    """
    Returns the pygame Vector of the target position
    """
    if self.currentQuest is None:
      return None
    return self.currentQuest.destination.pos

  def loadQuests(self):
    self.data = self.game.getSaveData()

    if self.data is None:
      for i in range(len(self.game.gameScreen.planets)):
        quest = DeliveryQuest("Deliver", self.game.gameScreen.planets[i], self.game, 10, random.choice(self.game.gameScreen.planets), i)
        self.questList.append(quest)
      print("[QuestManager] Generated ", len(self.questList), "quests with destination", [q.destination.name for q in self.questList], "\nand source ", [q.giver.name for q in self.questList]," and id ", [p.id for p in self.questList])
    else:
      for quest in self.questList:
        if quest.id in self.data["questStates"]:
          quest.completed = self.data["questStates"][quest.id]

      currentId = self.data.get("currentQuestId")

      if currentId is None:
        self.currentQuest = next( (q for q in self.questList if q.id == currentId), None)

  def checkPlanetIsGiver(self, planet):
    for i in range(len(self.questList)):
      if planet.name == self.questList[i].giver.name:
        if self.questList[i].completed:
          return False
        return True
      else:
        pass
    return False

  def checkPlanetIsTarget(self, planet):
    if self.currentQuest is None:
      return False
    return planet.name == self.currentQuest.destination.name


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
      planet.buttons[0].setDisabled(True)
    else:
      planet.buttons[0].setDisabled(True)
      # Quest is unavailable (completed)


  def completeQuest(self, planet):
    print("[QuestManager] Attempting to complete quest...")
    if planet.name == self.currentQuest.destination.name:
      if not self.currentQuest.completed:
        self.currentQuest.completed = True
        print("[QuestManager] Completed ", self.currentQuest.objective)
        self.game.phtonos.add(self.game, self.currentQuest.reward)
        planet.buttons[1].setDisabled(True)
        self.currentQuest = None
      else:
        planet.buttons[1].setDisabled(True)
    print("[QuestManager] Current global quest states:\n", [q.destination.name for q in self.questList], '\n', [q.giver.name for q in self.questList], '\n', [p.id for p in self.questList], '\n', [p.completed for p in self.questList])

  def toDict(self):
    return {
      "questStates" : {q.id: q.completed for q in self.questList},
      "currentQuestId": self.currentQuest.id if self.currentQuest else None,
    }
