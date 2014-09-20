#!/usr/bin/python

import Queue

bestDist = 1000000
bestNeighbour = None
priQ, k = None, 0

def dist(p1, p2):
  s = 0
  for i in xrange(len(p1)):
    s += abs(p1[i] - p2[i]) ** 2

  return s ** 0.5

class KDTree:
  def __init__(self, point, dimIndex):
    self.point = point
    self.dimIndex = dimIndex
    self.right, self.left = None, None

  def insert(self, point):
    if point[self.dimIndex] < self.point[self.dimIndex]:
      if self.left == None:
        self.left = KDTree(point, (self.dimIndex + 1) % len(point))
      else:
        self.left.insert(point)
    else:
      if self.right == None:
        self.right = KDTree(point, (self.dimIndex + 1) % len(point))
      else:
        self.right.insert(point)

  def findNearest(self, point):
    global bestDist, bestNeighbour
    global priQ, k

    priQ.put((-dist(point, self.point), self.point))
    if priQ.qsize() > k:
      priQ.get()

    # if dist(point, self.point) < bestDist:
    #   bestDist = dist(point, self.point)
    #   bestNeighbour = self.point

    other = None
    if point[self.dimIndex] < self.point[self.dimIndex]:
      if self.left != None:
        self.left.findNearest(point)
        other = self.right
    else:
      if self.right != None:
        self.right.findNearest(point)
        other = self.right

    if (abs(self.point[self.dimIndex] - point[self.dimIndex]) < -priQ.queue[-1][0] or \
      priQ.qsize() != k) and other != None:
      other.findNearest(point)

def main():
  p = [[1, 2], [3, 4], [5, 4], [6, 3], [6, 4]]
  global priQ, k
  priQ = Queue.PriorityQueue()
  k = 2

  kd = KDTree(p[0], 0)
  for pp in p[1:]:
    kd.insert(pp)

  kd.findNearest([6, 5])

  # print "%s %d" % (bestNeighbour, bestDist)
  print map(lambda x: (x[0] * -1, x[1]), priQ.queue)

if __name__ == "__main__":
  main()