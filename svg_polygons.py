#! /usr/bin/env python

class Canvas:

  width = 0
  height = 0
  canvas = ''
  shape_count = 0

  def __init__(self, width=500, height=500):
    self.width = width
    self.height = height

  def polygon(self, shape, border_colour='black', fill_colour=None, opacity=1.0):
    if fill_colour == None:
      fill_colour = "none"
    if border_colour == None:
      border_colour = "none"
    canvas = "\n  <g id='shape%s'>" % self.shape_count
    points = [(str(vertex[0]) + "," + str(vertex[1])) for vertex in shape]
    canvas += "\n    <polygon points='" + (" ".join(points)) + "' style='fill:%s; stroke:%s; fill-opacity:%s; stroke-opacity:%s; stroke-width:3; stroke-linejoin:miter;' />" % (fill_colour, border_colour, opacity, opacity)
    canvas += "\n  </g>\n"
    self.canvas += canvas
    self.shape_count += 1

  def circle(self, position, radius=1, border_colour='black', fill_colour=None, opacity=1.0):
    canvas = "\n  <g id='shape%s'>" % self.shape_count
    canvas += "\n    <circle cx='%s' cy='%s' r='%s' style='stroke:%s; fill:%s; fill-opacity:%s; stroke-opacity:%s;' />" % (position[0], position[1], radius, border_colour, fill_colour, opacity, opacity)
    canvas += "\n  </g>\n"
    self.canvas += canvas
    self.shape_count += 1

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
    self.shape_count = 0

  def addHeader(self):
    return "<svg xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:svg='http://www.w3.org/2000/svg' xmlns='http://www.w3.org/2000/svg' version='1.1' width='" + str(self.width) + "' height='" + str(self.height) + "'>\n"

  def addCanvas(self):
    return self.canvas + "\n"

  def addFooter(self):
    return "</svg>"
