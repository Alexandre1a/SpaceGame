class Quest:
  """
    A quest should have:
      - A reward
      - A giver
      - An objective
  """
  def __init__(
    self,
    objective,
    giver,
    receiver,
    reward,
    id
  ):
    """
      Sets a little bit of context for a quest
      All operations are done by the manager
    """
    self.objective = str(objective) + " from " + str(giver.name) + " for " + str(reward)
    self.giver     = giver
    self.receiver  = receiver
    self.reward    = reward
    self.id        = id
    self.completed = False

  def toDict(self):
    return {
        "id": self.id,
        "completed": self.completed,
        "reward": self.reward,
        "giver": self.giver.name,
        "receiver": None,
    }

  @classmethod
  def fromDict(cls, data, planets):
    pass
