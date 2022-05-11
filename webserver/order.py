import uuid

class Order:
  def __init__(self, coords):
    self.coordinatesFrom = coords['from']
    self.coordinatesTo = coords['to']
    self.order_uuid = uuid.uuid4()
    # when an order is placed we should check if there is an available drone, if so set status and drone accordingly
    self.status = "queue" 
    self.drone = None