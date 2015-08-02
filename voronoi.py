#############################################################
# Adapted from: https://gist.github.com/neothemachine/8803860
#############################################################

from __future__ import division
import numpy as np
from collections import defaultdict
from scipy.spatial import Delaunay, KDTree
import Polygon # http://www.j-raedler.de/projects/polygon/

def voronoi(P):
  delauny = Delaunay(P)
  triangles = delauny.points[delauny.vertices]
  circum_centers = np.array([triangle_csc(tri) for tri in triangles])
  long_lines_endpoints = []
  lineIndices = []
  for i, triangle in enumerate(triangles):
    circum_center = circum_centers[i]
    for j, neighbor in enumerate(delauny.neighbors[i]):
      if neighbor != -1:
        lineIndices.append((i, neighbor))
      else:     
        ps = triangle[(j+1)%3] - triangle[(j-1)%3]
        ps = np.array((ps[1], -ps[0]))
        middle = (triangle[(j+1)%3] + triangle[(j-1)%3]) * 0.5
        di = middle - triangle[j]
        ps /= np.linalg.norm(ps)
        di /= np.linalg.norm(di)
        if np.dot(di, ps) < 0.0:
          ps *= -1000.0
        else:
          ps *= 1000.0
        long_lines_endpoints.append(circum_center + ps)                
        lineIndices.append((i, len(circum_centers) + len(long_lines_endpoints)-1))
  vertices = np.vstack((circum_centers, long_lines_endpoints))
  lineIndicesSorted = np.sort(lineIndices) # make (1,2) and (2,1) both (1,2)
  lineIndicesTupled = [tuple(row) for row in lineIndicesSorted]
  lineIndicesUnique = sorted(set(lineIndicesTupled))
  return vertices, lineIndicesUnique
 
def triangle_csc(pts):
  rows, cols = pts.shape
  A = np.bmat([[2 * np.dot(pts, pts.T), np.ones((rows, 1))], [np.ones((1, rows)), np.zeros((1, 1))]])
  b = np.hstack((np.sum(pts * pts, axis=1), np.ones((1))))
  x = np.linalg.solve(A,b)
  bary_coords = x[:-1]
  return np.sum(pts * np.tile(bary_coords.reshape((pts.shape[0], 1)), (1, pts.shape[1])), axis=0)
 
def voronoi_cell_lines(points, vertices, lineIndices):
  kd = KDTree(points)
  cells = defaultdict(list)
  for i1,i2 in lineIndices:
    v1,v2 = vertices[i1], vertices[i2]
    mid = (v1+v2)/2
    _, (p1Idx,p2Idx) = kd.query(mid, 2)
    cells[p1Idx].append((i1,i2))
    cells[p2Idx].append((i1,i2))
  return cells
 
def voronoi_polygons(cells):
  for pIdx,lineIndices_ in cells.items():
    dangling_lines = []
    for i1,i2 in lineIndices_:
      connections = list(filter(lambda i12_: (i1,i2) != (i12_[0],i12_[1]) and (i1==i12_[0] or i1==i12_[1] or i2==i12_[0] or i2==i12_[1]), lineIndices_))
      assert 1 <= len(connections) <= 2
      if len(connections) == 1:
        dangling_lines.append((i1,i2))
    assert len(dangling_lines) in [0,2]
    if len(dangling_lines) == 2:
      (i11,i12), (i21,i22) = dangling_lines
      connected = list(filter(lambda i12_: (i12_[0],i12_[1]) != (i11,i12) and (i12_[0] == i11 or i12_[1] == i11), lineIndices_))
      i11Unconnected = len(connected) == 0
      connected = list(filter(lambda i12_: (i12_[0],i12_[1]) != (i21,i22) and (i12_[0] == i21 or i12_[1] == i21), lineIndices_))
      i21Unconnected = len(connected) == 0
      startIdx = i11 if i11Unconnected else i12
      endIdx = i21 if i21Unconnected else i22
      cells[pIdx].append((startIdx, endIdx))
  polys = dict()
  for pIdx,lineIndices_ in cells.items():
    directedGraph = lineIndices_ + [(i2,i1) for (i1,i2) in lineIndices_]
    directedGraphMap = defaultdict(list)
    for (i1,i2) in directedGraph:
      directedGraphMap[i1].append(i2)
    orderedEdges = []
    currentEdge = directedGraph[0]
    while len(orderedEdges) < len(lineIndices_):
      i1 = currentEdge[1]
      i2 = directedGraphMap[i1][0] if directedGraphMap[i1][0] != currentEdge[0] else directedGraphMap[i1][1]
      nextEdge = (i1, i2)
      orderedEdges.append(nextEdge)
      currentEdge = nextEdge
    polys[pIdx] = [i1 for (i1,i2) in orderedEdges]
  return polys

# Takes the intersection of the polygon and bounding box, such that polygons
# that lie partially out of the bounding box will be clipped
def clip_to_bounding_box(poly, bounding_box):
  p = Polygon.Polygon(poly)
  b = Polygon.Polygon(bounding_box)
  return list(p & b)[0]

def polygons(points, bounding_box):
  vertices, lineIndices = voronoi(points)
  cells = voronoi_cell_lines(points, vertices, lineIndices)
  polys = voronoi_polygons(cells)
  polylist = []
  for i in range(len(points)):
    poly = vertices[np.asarray(polys[i])]
    clipped_poly = clip_to_bounding_box(poly, bounding_box)
    polylist.append(clipped_poly)
  return polylist
