import copy
import sys
import os
import cProfile
from queue import Queue, PriorityQueue
import string
import random
import itertools
import time

class Node:
    idCounter = 0
    def __init__(self, snakes = dict(), stars = [], rows = 0, columns = 0, has_eaten = [], parent = None, cost = 0, h = 0):
        Node.idCounter += 1
        self.id = Node.idCounter
        self.snakes = snakes
        self.stars = stars
        self.rows = rows
        self.columns = columns
        self.parent = parent
        self.has_eaten = has_eaten
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def __lt__(self, other):
        '''Metodă-comparator utilizată pentru a adăuga obiectele de tip Node într-un PriorityQueue.'''
        if other.f > self.f:
            return True
        elif other.f == self.f and other.g < self.g:
            return True
        return False

    def __eq__(self, other):
        '''Metodă-comparator utilizată pentru a adăuga obiectele de tip Node într-un PriorityQueue.'''
        if other.f == self.f and other.g == self.g:
            return True
        return False

    def compare_nodes(self, other):
        '''Returnează True dacă informațiile nodurilor sunt identice și False altfel.'''
        return self.snakes == other.snakes and self.stars == other.stars

    def generate_path(self):
        '''Returnează nodurile de la rădăcină la nodul curent.'''
        l = [self]
        node = self
        while node.parent is not None:
            l.insert(0, node.parent)
            node = node.parent
        return l

    def show_path(self):
        '''Metoda utilizată pentru a scrie documentul de output după cerințele date - toate stările prin care s-a ajuns
        de la cea inițială la cea finală, precum și lungimea, costul și durata acestui drum.'''
        alg_time = time.time()
        l = self.generate_path()
        for i in range(len(l)):
            g.write(str(i+1) + ";" + "\n" + repr(l[i]) + "\n" + "\n\n")
        g.write("Lungime drum: " + str(len(l)) + "\n")
        g.write("Cost: " + str(l[-1].g) + "\n")
        g.write("Timp total: " + str(alg_time - start_time))


    def is_in_path(self, new_node):
        '''Returnează True dacă nodul dat ca parametru este un predecesor al celui care apelează metoda și False altfel.
                '''
        current_node = self
        while current_node is not None:
            if current_node.compare_nodes(new_node):
                return True
            current_node = current_node.parent
        return False

    def is_horisontal(self,s):
        '''Returnează True dacă șarpele al cărui indice este primit ca parametru este orizontal și False altfel.'''
        snake = self.snakes[s]
        x = snake[0][0]
        if all(_[0] == x for _ in snake):
            return True
        return False

    def is_vertical(self, s):
        '''Returnează True dacă șarpele al cărui indice este primit ca parametru este vertical și False altfel.'''
        snake = self.snakes[s]
        x = snake[0][1]
        if all(_[1] == x for _ in snake):
            return True
        return False

    def check_collision(self, s, d):
        '''Returnează True dacă mutarea șarpelui al cărui indice este primit ca parametru pe direcția dată ar produce
                vreo coliziune, fie cu el însuși, fie cu ceialți șerpi și False altfel.'''
        head = self.snakes[s][0]
        poz = (head[0] + d[0], head[1] + d[1])
        if poz[0] < 0 or poz[0] >= self.rows:
            return True
        if poz[1] < 0 or poz[1] >= self.columns:
            return True
        for k in self.snakes.keys():
            if poz in self.snakes[k]:
                    return True
        return False

    def move_snake(self, s, d):
        '''Aplică mutarea dată pe șarpe, stabilind costul acesteia, noile coordonate ale șarpelui și modificând lista de
                coordonate a steluțelor dacă s-a întamplat ca șarpele să mănânce una.'''
        cost = 3
        snake = self.snakes[s]
        stars = self.stars
        new_head = (snake[0][0] + d[0], snake[0][1] + d[1])
        if new_head[0] == snake[1][0] or new_head[1] == snake[1][1]:
            cost = 2
        if new_head in stars:
            snake = [new_head] + snake
            stars.remove(new_head)
            self.has_eaten.append((s, new_head))
            cost = 1
        else:
            for i in range(len(snake) - 1, 0, -1):
                snake[i] = snake[i - 1]
            snake[0] = new_head
        self.snakes[s] = snake
        self.stars = stars
        self.g += cost

    def find_tail_index(self, coord):
        '''Returnează indicele șarpelui căruia îi aparține coada ale cărei coordonate sunt primite ca parametru.'''
        snakes = self.snakes
        head = dict()
        tail = dict()
        for k in snakes.keys():
            head[k] = snakes[k][0]
            tail[k] = snakes[k][-1]
        return list(tail.keys())[list(tail.values()).index(coord)]

    def min_star_distance(self, head):
        '''Returnează distanța minimă dintre orice stea de pe tablă și coordonatele capului șarpelui dat.'''
        d = PriorityQueue()
        for s in self.stars:
            md = abs(s[0] - head[0] + s[1] - head[1])
            d.put(md)
        return d.get()

    def __repr__(self):
        '''Permite reprezentarea stării memorate în obiect sub forma dată în cerință.'''
        l = ["." * self.columns] * self.rows
        for i in self.stars:
            l[i[0]] = l[i[0]][:i[1]] + "*" + l[i[0]][i[1] + 1:]
        for i in self.snakes.keys():
            curr = self.snakes[i][0]
            l[curr[0]] = l[curr[0]][:curr[1]] + i + l[curr[0]][curr[1] + 1:]
            for s in range(1, len(self.snakes[i])):
                curr = self.snakes[i][s]
                l[curr[0]] = l[curr[0]][:curr[1]] + i.lower() + l[curr[0]][curr[1] + 1:]
        for i in range(len(self.has_eaten)):
            eat = self.has_eaten[i]
            l.append("Sarpele {} a mancat bobul de pe linia {}, coloana {}.".format(eat[0], eat[1][0], eat[1][1]))
        return ("\n" + "\n".join(l) + "\n")


class Graph:
    def __init__(self, nodes, start, square_size):
        self.nodes = nodes
        self.number_of_nodes = 1
        self.start = start
        self.square_size = square_size

    def node_index(self, n):
        return self.nodes.index(n)

    def first_heuristic(self, current_node):
        '''Calculează prima euristică admisibilă, detaliată în documentație.'''
        h = 0
        for k in current_node.snakes.keys():
            if len(current_node.snakes[k]) < self.square_size - 1:
                h += current_node.min_star_distance(current_node.snakes[k][0])
        return h

    def second_heuristic(self, current_node):
        '''Calculează a doua euristică admisibilă, detaliată în documentație.'''
        snakes = current_node.snakes
        dif = []
        for k in snakes.keys():
            snake = snakes[k]
            head = snake[0]
            l = 0
            c = 0
            while  l < len(snake) and head[0] == snake[l][0]:
                l += 1
            while c < len(snake) and head[1] == snake[c][1]:
                c += 1
            dif.append(min(len(snake) - l, len(snake) - c))
        return max(dif)

    def calculate_h(self, current_node, heuristic):
        '''Selectează una din cele două euristici disponibile - dacă nu, efectuează calculul euristicii banale.'''
        if heuristic ==1:
            return self.first_heuristic(current_node)
        elif heuristic == 2:
            return self.second_heuristic(current_node)
        else:
            if self.is_final(current_node):
                return 0
            return 1

    def check_length(self, current_node):
        '''Verifică dacă toți șerpii au lungimi valide - dacă sunt mai lungi sau egali cu latura pătratului, starea este
                invalidă.'''
        return all([len(current_node.snakes[k]) <= self.square_size for k in snake_list.keys()])

    def generate_successors(self, current_node):
        '''Funcția de generare a succesorilor nodului dat prin obținerea tuturor combinațiilor de direcții în care
                șerpii se pot duce și verificarea validității acestora.'''
        successor_list = []
        directions = []
        for direction in itertools.product([(0, 1), (0, -1), (1, 0), (-1, 0)], repeat = 4):
            directions.append(direction) #toate combinatiile posibile de
        # directii in care pot sa mearga serpii
        for direction in directions:
            new_node = copy.deepcopy(current_node)
            new_node.has_eaten = []
            if not new_node.check_collision("A", direction[0]):
                new_node.move_snake("A", direction[0])
            else:
                continue
            if not new_node.check_collision("B", direction[1]):
                new_node.move_snake("B", direction[1])
            else:
                continue
            if not new_node.check_collision("C", direction[2]):
                new_node.move_snake("C", direction[2])
            else:
                continue
            if not new_node.check_collision("D", direction[3]):
                new_node.move_snake("D", direction[3])
                if not new_node.is_in_path(current_node) and self.check_length(current_node):
                    new_node.parent = current_node
                    new_node.h = self.calculate_h(new_node, 2)
                    new_node.f = new_node.g + new_node.h
                    successor_list.append(new_node)
                    self.nodes.append(new_node)
                    self.number_of_nodes += 1
            else:
                continue
        return successor_list

    def is_final(self, current_node):
        '''Metoda care verifică dacă nodul curent este într-o stare finală, asigurându-se că au lungimea și orientarea
                corespunzătoare, precum și că formează un pătrat.'''
        snakes = current_node.snakes
        if not all([len(snakes[k]) == self.square_size - 1 for k in snakes.keys()]):
            return False
        head = dict()
        tail = dict()
        for k in snakes.keys():
            head[k] = snakes[k][0]
            tail[k] = snakes[k][-1]
        if current_node.is_horisontal("A"):
            if head["A"][1] - tail["A"][1] > 0:
                coord = (head["A"][0], head["A"][1] + 1)
            else:
                coord = (head["A"][0], head["A"][1] - 1)
            if coord in tail.values() and \
                    current_node.is_vertical(current_node.find_tail_index(coord)):
                if head[current_node.find_tail_index(coord)][0] - \
                        tail[current_node.find_tail_index(coord)][0] > 0:
                    coord = (head[current_node.find_tail_index(coord)][0] + 1,
                             head[current_node.find_tail_index(coord)][1])
                else:
                    coord = (head[current_node.find_tail_index(coord)][0] - 1,
                             head[current_node.find_tail_index(coord)][1])
                if coord in list(tail.values()) and \
                        current_node.is_horisontal(current_node.find_tail_index(coord)):
                    if head[current_node.find_tail_index(coord)][1] - \
                            tail[current_node.find_tail_index(coord)][1] > 0:
                        coord = (head[current_node.find_tail_index(coord)][0],
                                 head[current_node.find_tail_index(coord)][1] + 1)
                    else:
                        coord = (head[current_node.find_tail_index(coord)][0],
                                 head[current_node.find_tail_index(coord)][1] - 1)
                    if coord in tail.values() and \
                            current_node.is_vertical(current_node.find_tail_index(coord)):
                        if head[current_node.find_tail_index(coord)][0] - \
                                tail[current_node.find_tail_index(coord)][0] > 0:
                            coord = (head[current_node.find_tail_index(coord)][0] + 1,
                                     head[current_node.find_tail_index(coord)][1])
                        else:
                            coord = (head[current_node.find_tail_index(coord)][0] - 1,
                                     head[current_node.find_tail_index(coord)][1])
                        if tail["A"] == coord:
                            return True
        elif current_node.is_vertical("A"):
            if head["A"][0] - tail["A"][0] > 0:
                coord = (head["A"][0] + 1, head["A"][1])
            else:
                coord = (head["A"][0] - 1, head["A"][1])
            if coord in tail.values() and \
                    current_node.is_horisontal(current_node.find_tail_index(coord)):
                if head[current_node.find_tail_index(coord)][1] - \
                        tail[current_node.find_tail_index(coord)][1] > 0:
                    coord = (head[current_node.find_tail_index(coord)][0],
                             head[current_node.find_tail_index(coord)][1] + 1)
                else:
                    coord = (head[current_node.find_tail_index(coord)][0],
                             head[current_node.find_tail_index(coord)][1] - 1)
                if coord in tail.values() and \
                        current_node.is_vertical(current_node.find_tail_index(coord)):
                    if head[current_node.find_tail_index(coord)][0] - \
                            tail[current_node.find_tail_index(coord)][0] > 0:
                        coord = (head[current_node.find_tail_index(coord)][0] + 1,
                                 head[current_node.find_tail_index(coord)][1])
                    else:
                        coord = (head[current_node.find_tail_index(coord)][0] - 1,
                                 head[current_node.find_tail_index(coord)][1])
                    if coord in tail.values() and \
                            current_node.is_horisontal(current_node.find_tail_index(coord)):
                        if head[current_node.find_tail_index(coord)][1] - \
                                tail[current_node.find_tail_index(coord)][1] > 0:
                            coord = (head[current_node.find_tail_index(coord)][0],
                                     head[current_node.find_tail_index(coord)][1] + 1)
                        else:
                            coord = (head[current_node.find_tail_index(coord)][0],
                                     head[current_node.find_tail_index(coord)][1] - 1)
                        if tail["A"] == coord:
                            return True
        return False

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)

def generate_snake(i, j, x):
    '''Funcția utilizată pentru obținerea coordonatelor unui șarpe al cărui indice și coordonate ale capului sunt date
            drept parametru, asigurându-se că se menține în dicționar ordinea coordonatelor de la cap la coadă.'''
    target_coord = (i, j)
    global snake_list
    global lines
    snake_list[x] = [target_coord]
    for k in range(2):
        if target_coord[0] - 1 >= 0 and lines[target_coord[0] - 1][target_coord[1]] == x.lower() and \
                (target_coord[0] - 1, target_coord[1]) not  in snake_list[x]:
            new_target = (target_coord[0] - 1, target_coord[1])
            snake_list[x].append(new_target)
            target_coord = new_target
        elif target_coord[0] + 1 < len(lines) - 1 and lines[target_coord[0] + 1][target_coord[1]] == x.lower() and \
                (target_coord[0] + 1, target_coord[1]) not  in snake_list[x]:
            new_target = (target_coord[0] + 1, target_coord[1])
            snake_list[x].append(new_target)
            target_coord = new_target
        elif target_coord[1] - 1 >= 0 and lines[target_coord[0]][target_coord[1] - 1] == x.lower() and \
                (target_coord[0], target_coord[1] - 1) not in snake_list[x]:
            new_target = (target_coord[0], target_coord[1] - 1)
            snake_list[x].append(new_target)
            target_coord = new_target
        elif target_coord[1] + 1 < len(lines[0]) and lines[target_coord[0]][target_coord[1] + 1] == x.lower() and \
                (target_coord[0], target_coord[1] + 1) not  in snake_list[x]:
            new_target = (target_coord[0], target_coord[1] + 1)
            snake_list[x].append(new_target)
            target_coord = new_target

def read_file():
    '''Funcția de parsare și validare a fișierului de input care introduce coordonatele șerpilor în dicționarul aferent
                indicelui său și cele ale steluțelor în lista dedicată. Această funcție returnează True dacă fișierul este
                valid și False altfel.'''
    permitted_characters = "AaBbCcDd.*\n"
    global coords
    global lines
    lines = f.readlines()
    count_a = ("").join(lines).count("a")
    count_A = ("").join(lines).count("A")
    count_b = ("").join(lines).count("b")
    count_B = ("").join(lines).count("B")
    count_c = ("").join(lines).count("c")
    count_C = ("").join(lines).count("C")
    count_d = ("").join(lines).count("d")
    count_D = ("").join(lines).count("D")
    if count_D != 1 or count_C != 1 or count_B != 1 or count_A != 1:
        return False
    if count_d != 2 or count_c != 2 or count_b != 2 or count_a != 2:
        return False
    columns = len(lines[0])
    rows = len(lines) - 1 # nu este necesar sa adaugam 1 -> o linie in plus de la dimensiunea patratului final
    for i in range(rows):
        for j in range(columns):
            if lines[i][j] == '*':
                coords.append((i, j))
            elif lines[i][j] == 'A':
                generate_snake(i, j, 'A')
            elif lines[i][j] == 'B':
                generate_snake(i, j, 'B')
            elif lines[i][j] == 'C':
                generate_snake(i, j, 'C')
            elif lines[i][j] == 'D':
                generate_snake(i, j, 'D')
            elif lines[i][j] not in permitted_characters:
                return False
    global square_size
    square_size = int(''.join(_ for _ in lines[-1] if _.isdigit()))
    # scoate intregul din ultima linie de forma L = [int]
    return True


# ====================================== BFS DFS =========================================


def breadth_first(gr, number_of_solutions=1):
    total_nodes = 0
    max_nodes = 0
    q = Queue()
    q.put(gr.start)
    while not q.empty():
        if q.qsize() > max_nodes:
            max_nodes = q.qsize()
        alg_time = time.time()
        if alg_time - start_time > timeout:
            return
        nodCurent = q.get()
        if gr.is_final(nodCurent):
            nodCurent.show_path()
            g.write("\nNumărul total de noduri calculate: " + str(total_nodes))
            g.write("Numărul maxim de noduri în memorie: " + str(max_nodes) + "\n")
            g.write("\n\n------------------------------------------------------\n")
            number_of_solutions -= 1
            if number_of_solutions == 0:
                return
        successor_list = gr.generate_successors(nodCurent)
        total_nodes += len(successor_list)
        for s in successor_list:
            q.put(s)


def depth_first(gr, number_of_solutions=1):
    df(gr.start, number_of_solutions)


def df(current_node, number_of_solutions):
    total_nodes = 0
    alg_time = time.time()
    if alg_time - start_time > timeout:
        return
    if number_of_solutions <= 0:
        return number_of_solutions
    if gr.is_final(current_node):
        current_node.show_path()
        g.write("\nNumărul total de noduri calculate: " + str(total_nodes))
        g.write("\n\n------------------------------------------------------")
        number_of_solutions -= 1
        if number_of_solutions == 0:
            return number_of_solutions
    successor_list = gr.generate_successors(current_node)
    total_nodes += len(successor_list)
    for sc in successor_list:
        number_of_solutions = df(sc, number_of_solutions)
    return number_of_solutions


def idf(current_node, depth, number_of_solutions):
    total_nodes = 0
    alg_time = time.time()
    if alg_time - start_time > timeout:
        return
    if depth == 1 and gr.is_final(current_node):
        current_node.show_path()
        g.write("\nNumărul total de noduri calculate: " + str(total_nodes))
        g.write("\n\n------------------------------------------------------")
        number_of_solutions -= 1
        if number_of_solutions == 0:
            return number_of_solutions
    if depth > 1:
        successor_list = gr.generate_successors(current_node)
        total_nodes += len(successor_list)
        for sc in successor_list:
            if number_of_solutions != 0:
                number_of_solutions = idf(sc, depth - 1, number_of_solutions)
    return number_of_solutions


def iterative_depth_first(gr, number_of_solutions=1):
    for i in range(100):
        if number_of_solutions == 0:
            return
        number_of_solutions = idf(gr.start, i, number_of_solutions)

# ====================================== A* =========================================


def a_star(gr, number_of_solutions):
    total_nodes = 0
    c = PriorityQueue()
    c.put(gr.start)
    while not c.empty():
        alg_time = time.time()
        if alg_time - start_time > timeout:
            return
        current_node = c.get()
        print(current_node)
        if gr.is_final(current_node):
            current_node.show_path()
            g.write("\nNumărul total de noduri calculate: " + str(total_nodes) + "\n")
            g.write("\n\n------------------------------------------------------")
            number_of_solutions -= 1
            if number_of_solutions == 0:
                return
        successor_list = gr.generate_successors(current_node)
        total_nodes += len(successor_list)
        for s in successor_list:
            c.put(s)


def create_path(gr, current_node, limit, number_of_solutions):
    if current_node.f > limit:
        return number_of_solutions, current_node.f
    if gr.is_final(current_node) and current_node.f == limit:
        current_node.show_path()
        g.write("Limita: " + str(limit) + "\n")
        g.write("\n----------------\n")
        number_of_solutions -= 1
        if number_of_solutions == 0:
            return 0, "gata"
    successor_list = gr.generate_successors(current_node)
    minim = float('inf')
    for s in successor_list:
        number_of_solutions, res = create_path(gr, s, limit, number_of_solutions)
        if res == "gata":
            return 0, "gata"
        if res < minim:
            minim = res
    return number_of_solutions, minim


def ida_star(gr, number_of_solutions):
    start_node = gr.start
    limit = start_node.f
    while True:
        number_of_solutions, res = create_path(gr, start_node, limit, number_of_solutions)
        if res == "gata":
            break
        if res == float('inf'):
            break
        limit = res


def a_star_optim(gr):
    l_open = PriorityQueue()
    l_open.put(gr.start)
    l_closed = dict()
    close = False
    while not l_open.empty():
        current_node = l_open.get()
        l_closed[current_node.id] = current_node
        if gr.is_final(current_node):
            current_node.show_path()
            return
        successor_list = gr.generate_successors(current_node)
        while not l_open.empty():
            current_node = l_open.get()
            gasitC = False
            for current_node in list(l_open):
                if s.id == current_node.id:
                    gasitC = True
                    if s.f >= current_node.f:
                        successor_list.remove(s)
                    else:
                        l_open.get()
                    break
            if not gasitC:
                for current_node in l_closed.keys():
                    if s.id == current_node.id:
                        if s.f >= current_node.f:
                            successor_list.remove(s)
                            close = False
                        else:
                            del l_closed[current_node]
                            close = True
                        break



##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

start_time = time.time()
input_folder = os.fsdecode(sys.argv[1])
for input_file in os.listdir(input_folder):
    input_filename = os.fsdecode(input_file)
    if os.path.isfile(input_filename) and input_filename.endswith(".txt") and "output" not in input_filename:
        f = open(os.path.join(input_folder, input_file), "r")
        output_folder = os.fsdecode(sys.argv[2])
        output_filename = os.path.join(output_folder, input_file[:-4] + "_output.txt")
        g = open(output_filename, "w", encoding = "utf-8")
        lines = [[]]
        coords = []
        snake_list = dict()
        square_size = 0
        if read_file():
            init = Node(snake_list, coords, len(lines) - 1, len(lines[0]) - 1)
            if 4 * square_size - 16 > len(coords):
                g.write("Acest fișier input nu are nicio soluție.")
                break
        else:
            g.write("Acest fișier input nu este formatat corect.")
            break
        nodes = [init]
        start = init
        gr = Graph(nodes, start, square_size)
        solutions = int(sys.argv[3])
        timeout = int(sys.argv[4])
        # breadth_first(gr)
        # depth_first(gr, solutions)
        # iterative_depth_first(gr, solutions)
        a_star(gr, solutions)
        # a_star_optim(gr)
        # ida_star(gr, solutions)
        alg_time = time.time()
        if alg_time - start_time > timeout:
            g.write("TIMEOUT")


##################################################
