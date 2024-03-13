class PierrotExeception(Exception):
  def __init__(self, error: Exception):
    super().__init__('Pierrot error: ', error)
