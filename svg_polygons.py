#! /usr/bin/env python

class Canvas:

  width = 0
  height = 0
  canvas = ''
  polygons = []
  circles = []
  boxes = []

  def __init__(self, width=500, height=500):
    self.width = width
    self.height = height

  class Polygon:

    def __init__(self, shape):
      self.shape = shape
      self.border_colour = 'black'
      self.fill_colour = None
      self.opacity = 1.0

    def set_border_colour(self, colour):
      self.border_colour = colour

    def set_fill_colour(self, colour):
      self.fill_colour = colour

    def set_opacity(self, opacity):
      self.opacity = opacity

    def transform(self, x, y):
      new_shape = []
      for vertex in self.shape:
        new_vertex = [vertex[0] + x, vertex[1] + y]
        new_shape.append(new_vertex)
      self.shape = new_shape

  class Circle:

    def __init__(self, position, radius):
      self.position = position
      self.radius = radius
      self.border_colour = 'black'
      self.fill_colour = None
      self.opacity = 1.0

    def set_border_colour(self, colour):
      self.border_colour = colour

    def set_fill_colour(self, colour):
      self.fill_colour = colour

    def set_opacity(self, opacity):
      self.opacity = opacity

    def transform(self, x, y):
      self.position = [self.position[0] + x, self.position[1] + y]

    def scale(self, scale_factor):
      self.radius *= scale_factor

  class Box:

    def __init__(self, position, height, width):
      self.position = position
      self.height = height
      self.width = width

    def transform(self, x, y):
      self.position = [self.position[0] + x, self.position[1] + y]

    def scale(self, scale_factor):
      self.height *= scale_factor
      self.width *= scale_factor

  def add_polygon(self, shape, border_colour=False, fill_colour=False, opacity=False):
    self.polygons.append(self.Polygon(shape))
    if border_colour != False:
      self.polygons[-1].set_border_colour(border_colour)
    if fill_colour != False:
      self.polygons[-1].set_fill_colour(fill_colour)
    if opacity != False:
      self.polygons[-1].set_opacity(opacity)

  def add_circle(self, position, radius, border_colour=False, fill_colour=False, opacity=False):
    self.circles.append(self.Circle(position, radius))
    if border_colour != False:
      self.circles[-1].set_border_colour(border_colour)
    if fill_colour != False:
      self.circles[-1].set_fill_colour(fill_colour)
    if opacity != False:
      self.circles[-1].set_opacity(opacity)

  def add_box(self, position, height, width):
    self.boxes.append(self.Box(position, height, width))

  def write_polygon_to_canvas(self, shape_id):
    shape = self.polygons[shape_id]
    if shape.fill_colour == None:
      fill_colour = "none"
    else:
      fill_colour = shape.fill_colour
    if shape.border_colour == None:
      border_colour = "none"
    else:
      border_colour = shape.border_colour
    opacity = shape.opacity
    canvas = "\n  <g id='shape_%s'>" % shape_id
    points = [(str(vertex[0]) + "," + str(vertex[1])) for vertex in shape.shape]
    canvas += "\n    <polygon points='" + (" ".join(points)) + "' style='fill:%s; stroke:%s; fill-opacity:%s; stroke-opacity:%s; stroke-width:0.5; stroke-linejoin:miter;' />" % (fill_colour, border_colour, opacity, opacity)
    canvas += "\n  </g>\n"
    self.canvas += canvas

  def write_circle_to_canvas(self, shape_id):
    shape = self.circles[shape_id]
    if shape.fill_colour == None:
      fill_colour = "none"
    else:
      fill_colour = shape.fill_colour
    if shape.border_colour == None:
      border_colour = "none"
    else:
      border_colour = shape.border_colour
    opacity = shape.opacity
    position = shape.position
    radius = shape.radius
    canvas = "\n  <g id='shape_%s'>" % shape_id
    canvas += "\n    <circle cx='%s' cy='%s' r='%s' style='stroke:%s; fill:%s; fill-opacity:%s; stroke-opacity:%s;' />" % (position[0], position[1], radius, border_colour, fill_colour, opacity, opacity)
    canvas += "\n  </g>\n"
    self.canvas += canvas

  def write_box_to_canvas(self, shape_id):
    shape = self.boxes[shape_id]
    height = shape.height
    width = shape.width
    vertex1 = shape.position
    vertex2 = [vertex1[0]+width, vertex1[1]]
    vertex3 = [vertex1[0]+width, vertex1[1]+height]
    vertex4 = [vertex1[0], vertex1[1]+height]
    canvas = "\n  <g id='bounding_box_%s'>" % shape_id
    canvas += "\n    <polygon points='%s,%s %s,%s %s,%s, %s,%s' style='fill:none; stroke:gray; stroke-width:1; stroke-dasharray:3 2'/>" % (vertex1[0], vertex1[1], vertex2[0], vertex2[1], vertex3[0], vertex3[1], vertex4[0], vertex4[1])
    canvas += "\n  </g>"
    self.canvas += canvas

  def write_all_polygons(self):
    for shape_id in range(0, len(self.polygons)):
      self.write_polygon_to_canvas(shape_id)

  def write_all_circles(self):
    for shape_id in range(0, len(self.circles)):
      self.write_circle_to_canvas(shape_id)

  def write_all_boxes(self):
    for shape_id in range(0, len(self.boxes)):
      self.write_box_to_canvas(shape_id)

  def write_everything(self):
    self.write_all_polygons()
    self.write_all_circles()
    self.write_all_boxes()

  def save(self, filename='drawing'):
    canvas = self.addHeader()
    canvas += self.addCanvas()
    canvas += self.addFooter()
    f = open(filename + '.svg', 'w')
    f.write(canvas)
    f.close()
    print "File saved as %s.svg" % filename

  def clear(self):
    self.canvas = ''
    self.polygons = []
    self.circles = []
    self.boxes = []

  def addHeader(self):
    return "<svg width='" + str(self.width) + "' height='" + str(self.height) + "' xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:svg='http://www.w3.org/2000/svg' xmlns='http://www.w3.org/2000/svg' version='1.1'>\n"

  def addCanvas(self):
    return self.canvas + "\n"

  def addFooter(self):
    return "</svg>"
