from gameplay.quest import Quest

class DeliveryQuest(Quest):
  """
  A simple delivery quest,
  go from point A to B
  objective: The type of mission
  giver: The source of the quest
  receiver: The entity that need to accomplish the quest
  reward: The reward for completing the quest, in credits
  destination: The
  """
  def __init__(
    self,
    objective,
    giver,
    receiver,
    reward,
    destination,
    id
  ):
    super().__init__(objective, giver, receiver, reward, id)

    self.source      = giver # The giver is the source
    self.destination = destination
    self.objective += " to " + str(destination.name)
