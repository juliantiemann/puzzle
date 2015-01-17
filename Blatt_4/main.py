#Importsektion
from collections import deque
import time
import heapq

#-------------------------------------------------------------------------------
#------------------------------- Karte einlesen --------------------------------
#-------------------------------------------------------------------------------
f = input("(1)Aufgabe 1, (2)Aufgabe 2 oder (3)Aufgabe 3 oder (4)Portalspass: ") 
if f == "1":
    filename = 'blatt3_environment.txt'
elif f == "2":
    filename = 'env_a.txt'
elif f == "4":
    filename = 'env_b2_big.txt'
else:
    filename = 'env_b2.txt'

data = []
#Datei einlesen und Zeile fuer Zeile in Liste speichern
with open(filename, 'r') as f:
    for line in f:
       data.append(line)

#Eingelesene Datei auf Konsole ausgeben
for n in data:
    print(n.rstrip())
print('-----------------')

#Ließt die Karten ein, erstellt einen Graphen und speichert 
#Startknoten, Endknoten und gibt mögliche Portale zurück 
def parse_map(data):
    possiblePortals = ["0","1","2","3","4","5","6","7","8","9"]
    portals = {}
    nodes = {}
    #alle Felder durchgehen
    for y in range(len(data)):
        for x in range(len(data[y])):
            #Portale ermitteln
            if data[y][x] in possiblePortals:
                if int(data[y][x]) not in portals:
                    portals[int(data[y][x])] = []
                portals[int(data[y][x])].append((x,y))
            #Wenn Feld = s, als Startknoten setzen
            if data[y][x] == 's':
                start = (x,y)
            #Wenn Feld = g, als Zielknoten setzen    
            if data[y][x] == 'g':
                goal = (x,y)
            #Wenn das Feld leer ist zu den Knoten hinzufuegen
            if data[y][x] != 'x': 
                #und alle moeglichen Kanten in ein Set
                edges = set([])
                if x>0 and data[y][x-1] != "x":
                    edges.add((x-1, y))
                if x<(len(data[y]) - 1) and data[y][x+1] != "x":
                    edges.add((x+1, y))
                if y>0 and data[y-1][x] != "x":
                    edges.add((x, y-1))
                if y<(len(data) - 1) and data[y+1][x] != "x":
                    edges.add((x, y+1))
                nodes[(x,y)] = edges
    return nodes, start, goal, portals

#Portale im Graphen anwenden
def usePortals(portals, nodes):
    for portal in portals:
        adj1 = nodes[portals[portal][0]]
        adj2 = nodes[portals[portal][1]]
        nodes[portals[portal][0]] = adj2
        nodes[portals[portal][1]] = adj1
    return nodes
            
nodes, start, goal, portals = parse_map(data)

print('-----------------------')
print("##### Startknoten #####")
print('-----------------------')
print(start)
print('-----------------------')
print("###### Zielknoten #####")
print('-----------------------')
print(goal)


#-------------------------------------------------------------------------------
#------------------------------- Suchstrategien --------------------------------
#-------------------------------------------------------------------------------


#breadth first search
def bfs(graph, start, goal):
    global anzElemente
    anzElemente = 0
    #Set mit allen Knoten, die schon besucht wurden
    visited = set([start])
    #Queue mit allen zu betrachtenden Knoten + die Pfade bis zu diesen Knoten
    queue = deque([(start, [start])])
    anzElemente += 1
    while queue:
        #erster Knoten in Queue + Pfad 
        (currentnode, path) = queue.pop()
        visited.add(currentnode)
        #Fuer jeden zum aktuellen Knoten adjazente Knoten, bis auf die,
        #die schon besucht wurden
        for adjnode in graph[currentnode] - set(visited):
            #Wenn der adjazente Knoten = Zielknoten den Pfad zurueckgeben
            if adjnode == goal:
                return path + [adjnode] #bricht ab beim ersten Pfad den er findet
            #sonst Knoten und potenziellen Pfad in Queue und
            #zu den besuchten hinzufuegen 
            else:
                queue.appendleft((adjnode, path + [adjnode]))
                anzElemente += 1

#depth first search
def dfs(graph, start, goal):
    global anzElemente
    anzElemente = 0
    #Set mit allen Knoten, die schon besucht wurden
    visited = set([start])
    #Stack mit allen zu betrachtenden Knoten + die Pfade bis zu diesen Knoten
    stack = [(start, [start])]
    anzElemente += 1
    while stack:
        (currentnode, path) = stack.pop()
        visited.add(currentnode)
        for adjnode in graph[currentnode] - set(visited):# - set(path):
            if adjnode == goal:
                return path + [adjnode] #alle Pfade die in Frage kommen zurueck
            else:
                stack.append((adjnode, path + [adjnode]))
                anzElemente += 1

def AStern(graph, start, goal, portalDic):
    
    def euklDistanz(a,b):
        return (((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2))    
    
    #Es wird nicht nur die direkte euklidische Distanz zum Ziel berechnet, sondern
    #auch die euklidische Distanz über die einzelnen Portale. Der geringste Abstand wird zurückgegeben.
    def distanz(a, b, portalDic):
        dists = []
        for node in portalDic:
            dists.append(euklDistanz(a,node) + euklDistanz(portalDic[node],b))
        dists.append(euklDistanz(a,b))
        return min(dists)
    
    # globale Zählervariable für Anzahl Elemente in Queue
    global anzElemente
    anzElemente = 0
    
    #Set mit allen Knoten, die schon besucht wurden
    visited = set([start])
    #Set mit Knote, die bereits in Queue sind
    inQueue = set([])
    # Benutzung eines Heaps zur Priorisierung der Queue
    # (Kosten, Tripel aus Knotentupel und Pfad zum Knoten)
    prioritaetenQueue = []
    heapq.heappush(prioritaetenQueue, (0, start,[start]))
    anzElemente = 1
    while prioritaetenQueue:
        kosten,currentnode,path = heapq.heappop(prioritaetenQueue)
        visited.add(currentnode)
        for adjnode in graph[currentnode] - set(visited):
            # ist Knoten ein Zielknoten?
            if adjnode == goal:
                return path + [adjnode] 
            else:
                # prüfen, ob der Knoten bereits in der Queue ist, wenn ja, brauch ernicht mehr
                # hinzugefügt werden, da der kostengünstigste Weg zu diesem Knoten bereits gefunden wurde
                if adjnode not in inQueue:
                    # berechne Kosten fuer Knoten bis zum Zielknoten & fuege Knoten Heap hinzu
                    kostenKnoten = distanz(adjnode, goal, portalDic) + len(path)
                    heapq.heappush(prioritaetenQueue, (kostenKnoten, adjnode, path + [adjnode])) 
                    anzElemente += 1
                    inQueue.add(adjnode)
	           

	
#-------------------------------------------------------------------------------
#---------------------------------- Ausgabe ------------------------------------
#-------------------------------------------------------------------------------

type = input("(1)BFS oder (2)DFS oder (3)A* ?: ")
useportals = input("Portale benutzen (1)Ja oder (2)Nein?: ")

begin = time.clock()
if useportals == "1":
    nodes = usePortals(portals,nodes);
if type == "1":
    paths = list([bfs(nodes, start, goal)])
elif type == "2":
    paths = list([dfs(nodes, start, goal)])
elif type == "3":
    if useportals == "1":
        #Map mit Portalen, um schneller Ein- und Austiegspunkt zu finden
        portalDic = {}
        for portal in portals:
            for portal in portals:
                portalDic[portals[portal][0]] = portals[portal][1]
                portalDic[portals[portal][1]] = portals[portal][0]
        paths = list([AStern(nodes, start, goal, portalDic)])
    else:
        paths = list([AStern(nodes, start, goal, {})])  
end = time.clock()
    
print("\nMoegliche Pfade---------------------------------------------------------------\n")
#print paths

print("Es wurden", anzElemente, "Elemente der Queue hinzugefügt.")
print("Benötigte Zeit", end-begin)

if len(paths) != 0:
    i = 0
    for path in paths:
        if path is None:
            print("Kein Pfad zum Ziel gefunden") 
        else:
            i = i + 1
            print("\n", i,". Pfad - Länge", len(path), "\n")
            print(path)

            #Karte zeilenweise durchgehen und alle Knoten im gefundenen Pfad
            #durch "." ersetzen
            for y in range(len(data)):
                string = ""
                for x in range(len(data[y])):
                    if (x,y) in path and (x,y) != start and (x,y) != goal and data[y][x] not in ["0","1","2","3","4","5","6","7","8","9"]:
                        string += "."
                    else:
                        string += data[y][x]  
                print(string.rstrip())        
else:
    print("Kein Pfad zum Ziel gefunden")
