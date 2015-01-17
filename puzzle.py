import math
import copy
import heapq

class puzzle:
    def __init__(self):
        self.visited = 0

        #self.steine = [[1,8,7], [3,"b",5], [4,6,2]]
        self.steine = [[2,9,6,8], [4, "b", 5, 14], [15, 1, 10, 3], [12, 7, 13, 11]]
        #self.steine = [[1,2,3,4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, "b", 15]]
        #self.steine = [[1,2,3], [4,5,6], [7,8,"b"]]

        self.size = len(self.steine)

        self.ziele = {}
        for x in range((self.size * self.size) -1):
            self.ziele[x + 1] = x % self.size, x / self.size
        self.ziele["b"] = self.size - 1, self.size - 1

    def loesen(self):
        #hier kommt der A*
        #self.explored = []
        self.a_star()
        #root = Node(self, None, 0, None)
        #print self.ida_star(root)

    def a_star(self):
        visited = 0
        prioritaetenQueue = []
        heapq.heappush(prioritaetenQueue, (0, Node(self, None, 0, None)))
        inQueue = []
        while prioritaetenQueue:
            visited += 1
            #print visited
            kosten,node = heapq.heappop(prioritaetenQueue)
            if node.puzzle.heuristik() == 0:
                bew = []
                while node.parent:
                    bew.append(node.bew)
                    node = node.parent
                bew.reverse()

                print "Noetige Schritte:", len(bew)
                print "besucht =", visited
                print ", ".join(str(mv) for mv in bew)

                return "Gefunden"
            else:
                for child in node.children():
                    if child not in inQueue:
                        heapq.heappush(prioritaetenQueue, (child.restkosten, child))
                        inQueue.append(child)



# ------------------ IDA* ANFANG --------------------
    def ida_star(self, root):
        bound = root.puzzle.heuristik()

        while True:
            #print "neue Runde mit ", bound
            t = self.search(root, 0, bound)
            if t == "Gefunden":
                return "Gefunden"
            if t == float("inf"):
                return FALSE
            bound = t

    def search(self, node, g, bound):
        self.visited += 1
        #print g, bound, node.puzzle.heuristik()
        f = g + node.puzzle.heuristik()
        if f > bound:
            return f
        if node.puzzle.heuristik() == 0:

            bew = []
            while node.parent:
                bew.append(node.bew)
                node = node.parent
            bew.reverse()

            print "Noetige Schritte:", len(bew)
            print ", ".join(str(mv) for mv in bew)

            return "Gefunden"

        min = float("inf")

        for child in node.children():
            t = self.search(child, child.kosten, bound)
            if t == "Gefunden":
                return "Gefunden"
            if t < min:
                min = t
        return min

# ------------------ IDA* ENDE --------------------

    def heuristik(self):
        #die Bewertungen, wie nah das Puzzle am Zielzustand dran ist
        h = 0
        for y, reihe in enumerate(self.steine):
            for x, stein in enumerate(reihe):
                h += math.fabs(x - self.ziele[stein][0]) + math.fabs(y - self.ziele[stein][1])
        return int(h)

    def moveBlank(self, pos):
        #tauscht den blanken Stein mit dem an der angegebenen Position
        x,y = pos
        bx, by = self.getBlank()
        if (math.fabs(bx-x) == 1) ^ (math.fabs(by-y) == 1):
            self.steine[by][bx] = self.steine[y][x]
            self.steine[y][x] = "b"


    def getBlank(self):
        #gibt die aktuellen Koordinaten des blanken Steins zurueck
        for y, reihe in enumerate(self.steine):
            for x, stein in enumerate(reihe):
                if stein == "b":
                    return x,y

    def getNewBlanks(self):
        #gibt die moeglichen neuen Koordinaten des blanken Steines zurueck
        x,y = self.getBlank()
        bewegungen = []
        if x < self.size - 1: bewegungen.append((x + 1, y))
        if x > 0: bewegungen.append((x - 1, y))
        if y < self.size - 1: bewegungen.append((x, y + 1))
        if y > 0: bewegungen.append((x, y - 1))
        return bewegungen

    def printPuzzle(self):
        print self.steine



class Node:
    def __init__(self, puzzle, bew, kosten, parent):
        self.puzzle = puzzle
        self.bew = bew
        self.kosten = kosten
        self.parent = parent
        self.restkosten = kosten + self.puzzle.heuristik()

    def children(self):
        #gibt alle moeglichen Kinder eines Knotens zurueck
        children = []
        for newBlank in self.puzzle.getNewBlanks():
            #Das aktuelle Puzzle kopieren, die moeglichen Aenderungen anwenden und
            #zu den Kindern eines Knoten hinzufuegen
            puzzle = copy.deepcopy(self.puzzle)
            puzzle.moveBlank(newBlank)
            children.append(Node(puzzle, newBlank, self.kosten + 1, self))
        return children

    def __eq__(self, target):
        if isinstance(target, Node):
            return self.puzzle.steine == target.puzzle.steine
        else:
            return target == self


    def __hash__(self):
        return hash((self.kosten, self.parent))



p = puzzle()
p.printPuzzle()
#print p.getNewBlanks()
#p.moveBlank((2,1))
#p.printPuzzle()
p.loesen()
#print p.heuristik()
