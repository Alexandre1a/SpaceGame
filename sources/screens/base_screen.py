class Screen:
  """
  The base class for all screens in the game
  """
  def onEnter(self): pass
  def handle_event(self, event): pass
  def update(self, dt): pass
  def render(self, surface): pass
