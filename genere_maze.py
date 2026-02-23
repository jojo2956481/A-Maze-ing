
import random
from collections import deque
from parsing import pars_dict

# j'ai implementé l'algorithm de Kruskal pour generer le maze
# j'ai implémnter l'algotithm de BFS (Breadth-First Search) pour le solver
# la fonction display est generé par ia juste pour avoir un rendu

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
        for i in range(height):
            ligne = []
            for j in range(width):
                cellule = {'N': False, 'E': False, 'S': False, 'W': False, 'zone':1}
                ligne.append(cellule)
            self.cells.append(ligne)

    def display(self, print_zones=False):
        from math import floor
        #alias :
        w=self.width;h=self.height;c=self.cells;
        #si on imprime les zones, il faut élargir la taille des couloirs
        if(print_zones):
            len_zone=max([ max([ len(str(self.cells[i][j]['zone'])) for i in range(self.height) ]) for j in range(laby.width) ])+1
        inters=[' ','╴','╷', '┐','╶','─','┌','┬','╵','┘','│','┤','└','┴','├','┼']
        t=""
        #la grille des intersections de cases est de taille (N+1)(M+1)
        for i in range(h+1):
            interligne=""
            for j in range(w+1):
                #up, right, bottom, left : les 4 parties de la croix "┼" #False = mur, True = pas mur
                #Coins et bords:
                up=False if i==0 else None
                left=False if j==0 else None
                right=False if j==w else None
                bottom=False if i==h else None
                if j==w:
                    if up==None:up=not c[i-1][j-1]['E']
                    if bottom==None:bottom=not c[i][j-1]['E']
                if i==h:
                    bottom=False
                    if right==None:right=not c[i-1][j]['S']
                    if left==None:left=not c[i-1][j-1]['S']
                #intérieur :
                if up==None:up=not c[i-1][j]['W']
                if right==None:right=not c[i][j]['N']
                if bottom==None:bottom=not c[i][j]['W']
                if left==None:left=not c[i][j-1]['N']
                #-> mot binaire à 4 bits. 16 cas qu'on a mis dans l'ordre dans la liste inters
                #indice inters
                k=-up*8+right*4+bottom*2+left
                if not print_zones:
                    #espacement horizontal supplémentaire
                    sep= "─" if left else " "
                    t+=sep+inters[k]
                    if j==self.width:t+="\n"
                else:
                    sep= (len_zone+2)*"─" if right else (len_zone+2)*" "
                        #num_zone=self.zones[self.cells[i][j]["zone"]] if i -1 and num_zone <10  else "*"
                    interligne+=("│" if bottom else " ")+" "*(len_sp_left+1)+txt_num_zone+" "*(len_sp_right+1)
                    t+=inters[k]+sep
                    if j==self.width:
                        t+="\n" + interligne + "\n"
        print(t)

    def fusionner(self, i, j, dir):
        if not (0 <= i < self.height and 0 <= j < self.width):
            return False
        cellule = self.cells[i][j]
        zone1 = int(cellule['zone'])

        ni = nj = None
        mur_cell = mur_voisin = None

        if dir == 'N':
            ni, nj = i - 1, j
            mur_cell = 'N'
            mur_voisin = 'S'
        elif dir == 'S':
            ni, nj = i + 1, j
            mur_cell = 'S'
            mur_voisin = 'N'
        elif dir == 'E':
            ni, nj = i, j + 1
            mur_cell = 'E'
            mur_voisin = 'W'
        elif dir == 'W':
            ni, nj = i, j - 1
            mur_cell = 'W'
            mur_voisin = 'E'
        else:
            return False
        if not (0 <= ni < self.height and 0 <= nj < self.width):
            return False
        
        voisin = self.cells[ni][nj]
        zone2 = voisin['zone']

        if zone1 == zone2:
            return False
        cellule[mur_cell] = True
        voisin[mur_voisin] = True

        for x in range(self.height):
            for y in range(self.width):
                if self.cells[x][y]['zone'] == zone2:
                    self.cells[x][y]['zone'] = zone1
        return True

    def generer(self):
        zone_id = 0
        for i in range(self.height):
            for j in range(self.width):
                self.cells[i][j]['zone'] = zone_id
                self.cells[i][j]['N'] = False
                self.cells[i][j]['E'] = False
                self.cells[i][j]['S'] = False
                self.cells[i][j]['W'] = False
                zone_id += 1
        murs = []

        for i in range(self.height):
            for j in range(self.width):
                if j < self.width - 1:
                    murs.append((i, j, 'E'))
                if i < self.height - 1:
                    murs.append((i, j, 'S'))
        random.shuffle(murs)
        for (i, j, direction) in murs:
            self.fusionner(i, j, direction)

    def solver(self, entry, exit):
        e_x, e_y = map(int, entry.split(","))
        o_x, o_y = map(int, exit.split(","))

        start = (e_y, e_x)
        goal = (o_y, o_x)

        queue = deque([start])
        visited = set()
        parents = {}

        visited.add(start)

        while queue:
            current = queue.popleft()

            if current == goal:
                break
            i, j = current
            cell = self.cells[i][j]
            directions = [
                ('N', (-1, 0)),
                ('S', (1, 0)),
                ('E', (0, 1)),
                ('W', (0, -1))
            ]
            for direction, (di, dj) in directions:
                if cell[direction]:
                    ni, nj = i + di, j + dj
                    neighbor = (ni, nj)
                    if 0 <= ni < self.height and 0 <= nj < self.width:
                        neighbor = (ni, nj)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        parents[neighbor] = (current, direction)
                        queue.append(neighbor)
        path = []
        lst = ""
        current = goal
        while current != start:
            parent, direction = parents[current]
            path.append((current, direction))
            current = parent
        path.append((start, None))
        path.reverse()
        for cell, direction in path:
            if direction is not None:
                lst += direction
        return lst


def config_maze(dictionaire):
    width = int(dictionaire["WIDTH"])
    heigt = int(dictionaire["HEIGHT"])
    entry = dictionaire["ENTRY"]
    exit = dictionaire["EXIT"]
    grille = Maze(width, heigt)
    grille.generer()
    grille.display()
    print(entry)
    print(exit)
    path = grille.solver(entry, exit)
    print(path)


if __name__ == "__main__":
    data = pars_dict()
    if data:
        config_maze(data)
