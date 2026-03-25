from gameplay.quest import Quest

class DeliveryQuest(Quest):
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
