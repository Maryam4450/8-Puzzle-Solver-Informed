import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def enqueue(self, x):
        heapq.heappush(self.elements, (x.f, x))  

    def dequeue(self):
        return heapq.heappop(self.elements)[1]  
    
    def is_empty(self):
        return len(self.elements) == 0

class Node:
    def __init__(self, state, goal, parent=None, g=0):
        self.state = state
        self.parent = parent
        self.goal = goal
        self.g = g  
        self.h = self.heuristic_manhattan()  # Manhattan distance
        #self.h = self.heuristic() #hamming (out of place tile)
        self.f = self.g + self.h  

    def __lt__(self, other):
        return self.f < other.f  
    
    def heuristic_manhattan(self):  
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
    
    def heuristic(self):#hamming (out of place tiles)
        dis = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0 and self.state[i][j] != self.goal[i][j]:
                    dis += 1
        return dis
    
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
                child_node = Node(child_state, self.goal, parent=node, g=node.g + 1)  
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
    
    # ================== A* algorithm ===================
    def solve_puzzle_astar(self):  
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
        """ Backtrack and return solution path """
        path = []
        while node:
            path.insert(0, node)
            node = node.parent
        return path

goal = [[1,2,3], [4,5,6], [7,8,0]]
ps = PuzzleSolver([[4, 7, 8], [3, 6, 5], [1, 2, 0]], goal)
solution = ps.solve_puzzle_astar()


print("============================================")
if solution:
    i = 1
    for state in solution:
        print(f"Step {i}")
        i += 1
        for row in state.state:
            print(row)
        print()
else:
    print("No solution found.")

