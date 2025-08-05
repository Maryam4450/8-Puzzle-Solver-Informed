import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def enqueue(self, x):
        heapq.heappush(self.elements, x)

    def dequeue(self):
        return heapq.heappop(self.elements)
    
    def is_empty(self):
        return len(self.elements) == 0

class Node:
    def __init__(self, state, goal,parent=None):
        self.state = state
        self.parent = parent
        self.goal=goal
        self.h = self.heuristic() #use in hamming(out of place tiles)
        #self.h = self.heuristic_manhattan() 

    def __lt__ (self, other):
        return self.h < other.h
    
    def heuristic(self):#hamming (out of place tiles)
        dis = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0 and self.state[i][j] != self.goal[i][j]:
                    dis += 1
        return dis
    
    def heuristic_manhattan(self): #manhattan distance
        dis = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:  
                    value = self.state[i][j]
                    for x in range(3):
                        for y in range(3):
                            if self.goal[x][y] == value:
                                dis += abs(i - x) + abs(j - y)
                                break
        return dis
    
    def __str__ (self):
        s=""
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                s+=f"{self.state[i][j]} "
            s+="\n"
        return s

class PuzzleSolver:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
    
    def find_space(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)

    def find_moves(self, pos):
        x, y = pos
        return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    
    def find_children(self, node):
        children = []
        space = self.find_space(node.state)
        moves = self.find_moves(space)

        for move in moves:
            if self.is_valid(move[0], move[1]):  
                child_state = self.play_move(node, move, space)
                child_node = Node(child_state, self.goal, parent=node)  
                child_node.h = child_node.heuristic()  #this is used in case of hamming(out of place tiles)
                #child_node.h = child_node.heuristic_manhattan()  
                children.append(child_node)
        return children
    
    def is_valid(self, x, y):
        return 0 <= x < 3 and 0 <= y < 3
    
    def play_move(self, state, move, space):
        x_space, y_space = space
        x_move, y_move = move
        copy_state = [row[:] for row in state.state]
        copy_state[x_space][y_space], copy_state[x_move][y_move] = copy_state[x_move][y_move], copy_state[x_space][y_space] 
        return copy_state
    
    #using best first search====================================
    def solve_puzzle_bfs(self): 
        pq = PriorityQueue()
        start_node = Node(self.start, self.goal)
        pq.enqueue(start_node)
        visited = set()
        
        while not pq.is_empty():
            current = pq.dequeue()
            if current.state == self.goal:
                return self.print_solution(current)
            visited.add(str(current.state))
            for child in self.find_children(current):
                if str(child.state) not in visited:
                    pq.enqueue(child)
        return []
    
    def print_solution(self, node):        
        path = []
        while node:
            path.insert(0, node)
            node = node.parent
        print("\nSolution Path:")
        return path
       

goal = [[1,2,3], [4,5,6], [7,8,0]]
ps = PuzzleSolver([[4, 7, 8], [3, 6, 5], [1, 2, 0]], goal)
#ps = PuzzleSolver([[1, 2, 3], [0, 4, 6], [7, 5, 8]], goal)
solution = ps.solve_puzzle_bfs()
print("============================================")
if solution:
    i=1
    for state in solution:
        print(f"step {i}")
        i=i+1
        for row in state.state:
            print(row)
        print()
        
else:
    print("No solution found.")
