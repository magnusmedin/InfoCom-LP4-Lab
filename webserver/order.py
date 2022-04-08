import uuid

class Order:
  def __init__(self, x_dest_osm, y_dest_osm):
    self.coordinates = (x_dest_osm, y_dest_osm)
    self.order_uuid = uuid.uuid1()
    # when an order is placed we should check if there is an available drone, if so set status and drone accordingly
    self.status = "queue" 
    self.drone = None