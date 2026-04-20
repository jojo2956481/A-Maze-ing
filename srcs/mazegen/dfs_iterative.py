import random
# from srcs.transform_data.parsing import pars_dict
# from .solver import solver_bfs, solver_all_path


class DfsMaze():
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

    def generate_maze(self, seed=None) -> None:
        self.init_grille()
        if seed is not None:
            random.seed(seed)

        i, j = self.start()
        self.dfs_recursive(i, j)

    def execute_dfs(self, seed=None):
        if seed is not None:
            random.seed(seed)

        i, j = self.start()
        self.dfs_recursive(i, j)

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

    def start(self):
        while True:
            i, j = random.choice(self.lst_grille)
            if (i, j) not in self.forty_two:
                self.maze[i][j]["zone"] = 1
                return i, j

    def find_voisin(self, direction, i, j):

        ni, nj = None, None
        mur_cell, mur_voisin = None, None
        if direction == 'N':
            ni, nj = i - 1, j
            mur_cell = 'N'
            mur_voisin = 'S'
        elif direction == 'S':
            ni, nj = i + 1, j
            mur_cell = 'S'
            mur_voisin = 'N'
        elif direction == 'E':
            ni, nj = i, j + 1
            mur_cell = 'E'
            mur_voisin = 'W'
        elif direction == 'W':
            ni, nj = i, j - 1
            mur_cell = 'W'
            mur_voisin = 'E'

        return ni, nj, mur_cell, mur_voisin

    def dfs_recursive(self, i, j):
        stack = [(i, j)]
        self.maze[i][j]["zone"] = 1

        while stack:
            i, j = stack[-1]

            directions = ['N', 'E', 'S', 'W']
            random.shuffle(directions)

            moved = False
            for direction in directions:
                ni, nj, mur_cell, mur_voisin = self.find_voisin(direction,
                                                                i, j)

                if not (0 <= ni < self.height and 0 <= nj < self.width):
                    continue
                if (ni, nj) in self.forty_two:
                    continue
                if self.maze[ni][nj]["zone"] == 0:
                    self.maze[i][j][mur_cell] = True
                    self.maze[ni][nj][mur_voisin] = True
                    self.maze[ni][nj]["zone"] = 1

                    stack.append((ni, nj))
                    moved = True
                    break

            if not moved:
                stack.pop()

    def place_42(self):
        centre_i = self.height // 2
        centre_j = self.width // 2 + 1 if self.width % 2 == 1 else self.width // 2

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

    # def display(self, print_zones=False):
    #     from math import floor
    #     #alias :
    #     w=self.width;h=self.height;c=self.maze;
    #     #si on imprime les zones, il faut élargir la taille des couloirs
    #     if (print_zones):
    #         len_zone = max([max([len(str(self.maze[i][j]['zone']))
    #                             for i in range(self.height)])
    #                         for j in range(laby.width)])+1
    #     inters = [' ', '╴', '╷', '┐', '╶', '─', '┌', '┬', '╵', '┘',
    #               '│', '┤', '└', '┴', '├', '┼']
    #     t=""
    #     #la grille des intersections de cases est de taille (N+1)(M+1)
    #     for i in range(h+1):
    #         interligne=""
    #         for j in range(w+1):
    #             #up, right, bottom, left : les 4 parties de la croix
    #             # "┼" #False = mur, True = pas mur
    #             #Coins et bords:
    #             up=False if i==0 else None
    #             left=False if j==0 else None
    #             right=False if j==w else None
    #             bottom=False if i==h else None
    #             if j==w:
    #                 if up==None:up=not c[i-1][j-1]['E']
    #                 if bottom==None:bottom=not c[i][j-1]['E']
    #             if i==h:
    #                 bottom=False
    #                 if right==None:right=not c[i-1][j]['S']
    #                 if left==None:left=not c[i-1][j-1]['S']
    #             #intérieur :
    #             if up==None:up=not c[i-1][j]['W']
    #             if right==None:right=not c[i][j]['N']
    #             if bottom==None:bottom=not c[i][j]['W']
    #             if left==None:left=not c[i][j-1]['N']
    #             # -> mot binaire à 4 bits. 16 cas qu'on a mis dans
    #             # l'ordre dans la liste inters
    #             # indice inters
    #             k=-up*8+right*4+bottom*2+left
    #             if not print_zones:
    #                 #espacement horizontal supplémentaire
    #                 sep= "─" if left else " "
    #                 t+=sep+inters[k]
    #                 if j==self.width:t+="\n"
    #             else:
    #                 sep= (len_zone+2)*"─" if right else (len_zone+2)*" "
    #                     # num_zone=self.zones[self.maze[i][j]["zone"]]
    #                     # if i -1 and num_zone <10  else "*"
    #                 interligne += ("│" if bottom else " ") + " " * (len_sp_left + 1) + txt_num_zone + " " * (len_sp_right+1)
    #                 t+=inters[k]+sep
    #                 if j==self.width:
    #                     t+="\n" + interligne + "\n"
    #     print(t)

    def imperfect_maze(self):
        mur = 0
        for ligne in self.maze:
            for cell in ligne:
                for value in cell.values():
                    if value is False:
                        mur += 1
        mur = mur // 2
        mur = mur - (self.height + self.width)
        mur = mur - 55
        result = int(mur * 0.5)
        directions = {
            'N': (-1, 0, 'S'),
            'S': (1, 0, 'N'),
            'E': (0, 1, 'W'),
            'W': (0, -1, 'E')
        }
        for _ in range(result):
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)

            dir_name = random.choice(list(directions.keys()))
            di, dj, opposite = directions[dir_name]

            ni, nj = i + di, j + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                if not self.maze[i][j][dir_name]:
                    if self.maze[i][j]["zone"] != 0:
                        if self.maze[ni][nj]["zone"] != 0:
                            if sum(1 for v in self.maze[i][j].values()
                                   if not v) >= 1:
                                if sum(1 for v in self.maze[ni][nj].values()
                                       if not v) >= 1:

                                    self.maze[i][j][dir_name] = True
                                    self.maze[ni][nj][opposite] = True


# def config_maze(dictionaire):
#     # print(dictionaire)
#     width = int(dictionaire["WIDTH"])
#     heigt = int(dictionaire["HEIGHT"])
#     entry = dictionaire["ENTRY"]
#     exit = dictionaire["EXIT"]
#     if "SEED" in dictionaire:
#         seed = int(dictionaire["SEED"])
#     else:
#         seed = None
#     grille = dfs(width, heigt)
#     grille.init_grille()
#     grille.place_42()
#     grille.execute_dfs(seed)
#     grille.display()
#     print(solver_bfs(entry, exit, grille))
#     # print(solver_all_path(entry, exit, grille))
#     grille.imperfect_maze()
#     grille.display()
#     print(solver_all_path(entry, exit, grille))


# if __name__ == "__main__":
#     data = pars_dict()
#     if data:
#         config_maze(data)
