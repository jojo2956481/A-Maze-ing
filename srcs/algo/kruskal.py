import random
from collections import deque
from srcs.transform_data.parsing import pars_dict


class maze_Kruskal():
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.maze = []
        self.forty_two = []
        self.lst_grille = []
        for i in range(height):
            ligne = []
            for j in range(width):
                cellule = {'N': False, 'E': False, 'S': False,
                           'W': False, 'zone': 1}
                ligne.append(cellule)
            self.maze.append(ligne)

    def init_grille(self):
        zone_id = 0
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.maze[i][j]['N'] = False
                self.maze[i][j]['E'] = False
                self.maze[i][j]['S'] = False
                self.maze[i][j]['W'] = False
                self.lst_grille.append((i, j))

    def generer(self, seed=0):
        zone_id = 0
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.maze[i][j]['N'] = False
                self.maze[i][j]['E'] = False
                self.maze[i][j]['S'] = False
                self.maze[i][j]['W'] = False
                zone_id += 1
        murs = []

        for i in range(self.height):
            for j in range(self.width):
                if j < self.width - 1:
                    murs.append((i, j, 'E'))
                if i < self.height - 1:
                    murs.append((i, j, 'S'))

        if seed is not None:
            random.seed(seed)
        random.shuffle(murs)
        for (i, j, direction) in murs:
            self.fusionner(i, j, direction)

    def fusionner(self, i: int, j: int, dir: str):
        if not (0 <= i < self.height and 0 <= j < self.width):
            return False
        if (i, j) in self.forty_two:
            return False

        cellule = self.maze[i][j]
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

        if (ni, nj) in self.forty_two:
            return False

        voisin = self.maze[ni][nj]
        zone2 = voisin['zone']

        if zone1 == zone2:
            return False

        cellule[mur_cell] = True
        voisin[mur_voisin] = True

        for x in range(self.height):
            for y in range(self.width):
                if self.maze[x][y]['zone'] == zone2:
                    self.maze[x][y]['zone'] = zone1
        return True

    def place_42(self):
        centre_i = self.height // 2
        centre_j = self.width // 2

        four = [
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1],
        ]

        two = [
            [1, 1, 1],
            [0, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 1],
        ]

        start_i = centre_i - 2
        start_j = centre_j - 4

        for di in range(len(four)):
            for dj in range(len(four[0])):
                if four[di][dj] == 1:
                    i = start_i + di
                    j = start_j + dj
                    if 0 <= i < self.height and 0 <= j < self.width:
                        self.forty_two.append((i, j))
        for di in range(len(two)):
            for dj in range(len(two[0])):
                if two[di][dj] == 1:
                    i = start_i + di
                    j = start_j + dj + 4
                    if 0 <= i < self.height and 0 <= j < self.width:
                        self.forty_two.append((i, j))

    def display(self, print_zones=False):
        from math import floor
        #alias :
        w=self.width;h=self.height;c=self.maze;
        #si on imprime les zones, il faut élargir la taille des couloirs
        if (print_zones):
            len_zone = max([max([len(str(self.maze[i][j]['zone']))
                                for i in range(self.height)])
                            for j in range(laby.width)])+1
        inters = [' ', '╴', '╷', '┐', '╶', '─', '┌', '┬', '╵', '┘',
                  '│', '┤', '└', '┴', '├', '┼']
        t=""
        #la grille des intersections de cases est de taille (N+1)(M+1)
        for i in range(h+1):
            interligne=""
            for j in range(w+1):
                #up, right, bottom, left : les 4 parties de la croix
                # "┼" #False = mur, True = pas mur
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
                # -> mot binaire à 4 bits. 16 cas qu'on a mis dans
                # l'ordre dans la liste inters
                # indice inters
                k=-up*8+right*4+bottom*2+left
                if not print_zones:
                    #espacement horizontal supplémentaire
                    sep= "─" if left else " "
                    t+=sep+inters[k]
                    if j==self.width:t+="\n"
                else:
                    sep= (len_zone+2)*"─" if right else (len_zone+2)*" "
                        # num_zone=self.zones[self.maze[i][j]["zone"]]
                        # if i -1 and num_zone <10  else "*"
                    interligne += ("│" if bottom else " ") + " " * (len_sp_left + 1) + txt_num_zone + " " * (len_sp_right+1)
                    t+=inters[k]+sep
                    if j==self.width:
                        t+="\n" + interligne + "\n"
        print(t)


def config_maze(dictionaire):
    width = int(dictionaire["WIDTH"])
    heigt = int(dictionaire["HEIGHT"])
    if "SEED" in dictionaire:
        seed = int(dictionaire["SEED"])
    else:
        seed = None
    grille = maze_Kruskal(width, heigt)
    grille.init_grille()
    grille.place_42()

    grille.generer(seed)
    grille.display()
    print()


if __name__ == "__main__":
    data = pars_dict()
    if data:
        config_maze(data)
