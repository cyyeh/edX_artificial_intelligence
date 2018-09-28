from queue import Queue, LifoQueue
import time
import resource
import sys
import math
from heapq import heappush, heappop

class PriorityQueue:
    def __init__(self):
        self.queue = []
        self._index = 0

    def empty(self):
        return len(self.queue) == 0

    def put(self, priority, value):
        heappush(self.queue, (priority, self._index, value))
        self._index += 1
    
    def get(self):
        return heappop(self.queue)[-1]

class PuzzleState(object):
    """docstring for PuzzleState"""
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")
        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self, reverse=True):
        """expand the node"""
        if len(self.children) == 0:
            if reverse:  
                # add child nodes in order of RLDU    
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
            else:
                # add child nodes in order of UDLR
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
        return self.children

# Function that Writes to output.txt
### Students need to change the method to have the corresponding parameters
def writeOutput(sm, result, time_mem_statistics):
    f = open('output.txt', mode='w')
    final_state = result["state"]
    path_to_goal = [final_state.action]
    cost_of_path = final_state.cost
    nodes_expanded = result["nodes_expanded"]

    parent_state = final_state.parent
    while parent_state:
        if parent_state.parent:
            path_to_goal.append(parent_state.action)
        parent_state = parent_state.parent

    path_to_goal.reverse()
    search_depth = len(path_to_goal)
    
    f.write("path_to_goal: " + str(path_to_goal) + "\n")
    f.write("cost_of_path: " + str(cost_of_path) +  "\n")
    f.write("nodes_expanded: " + str(nodes_expanded) + "\n")
    f.write("search_depth: " + str(search_depth) + "\n")
    if sm == "bfs":
        f.write("max_search_depth: " + str(search_depth + 1) + "\n")
    elif sm == "dfs":
        f.write("max_search_depth: " + str(search_depth) + "\n")
    elif sm == "ast":
        f.write("max_search_depth: " + str(search_depth) +  "\n")
    f.write("running_time: " + str(time_mem_statistics[0]) + "\n")
    f.write("max_ram_usage: " + str(time_mem_statistics[1]) + "\n")

    f.close()

def bfs_search(initial_state):
    """BFS search"""
    frontier = Queue() # queue
    frontier.put(initial_state) # enqueue
    frontier_and_explored = {} # frontier and explored states
    frontier_and_explored[tuple(initial_state.config)] = True
    nodes_expanded = 0

    while not frontier.empty():
        state = frontier.get() # dequeue

        if test_goal(state):
            final_states = {
                "state": state,
                "nodes_expanded": nodes_expanded
            }
            return True, final_states
        
        state.expand(reverse=False)
        nodes_expanded += 1
        for neighbor in state.children:
            if not tuple(neighbor.config) in frontier_and_explored:
                frontier.put(neighbor) # enqueue
                frontier_and_explored[tuple(neighbor.config)] = True


    return False, None

def dfs_search(initial_state):
    """DFS search"""
    frontier = LifoQueue() # stack
    frontier.put(initial_state) # push
    frontier_and_explored = {} # frontier and explored states
    frontier_and_explored[tuple(initial_state.config)] = True
    nodes_expanded = 0

    while not frontier.empty():
        state = frontier.get() # pop
        
        if test_goal(state):
            final_states = {
                "state": state,
                "nodes_expanded": nodes_expanded
            }
            return True, final_states
        
        state.expand()
        nodes_expanded += 1
        for neighbor in state.children:
            if not tuple(neighbor.config) in frontier_and_explored:
                frontier.put(neighbor) # push
                frontier_and_explored[tuple(neighbor.config)] = True

    return False, None

def A_star_search(initial_state):
    """A * search"""
    frontier = PriorityQueue() # priority queue
    frontier.put(calculate_total_cost(initial_state), initial_state)
    frontier_dict = {}
    explored_dict = {}
    frontier_dict[tuple(initial_state.config)] = True
    nodes_expanded = 0

    while not frontier.empty():
        state = frontier.get()
        #del frontier_dict[tuple(state.config)]
        explored_dict[tuple(state.config)] = True

        if test_goal(state):
            final_states = {
                "state": state,
                "nodes_expanded": nodes_expanded
            }
            return True, final_states
        
        state.expand()
        nodes_expanded += 1
        for neighbor in state.children:
            if not tuple(neighbor.config) in frontier_dict and \
            not tuple(neighbor.config) in explored_dict:
                frontier.put(calculate_total_cost(neighbor), neighbor)
                frontier_dict[tuple(neighbor.config)] = True
            elif tuple(neighbor.config) in frontier_dict:
                frontier.put(calculate_total_cost(neighbor), neighbor)

    return False, None

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    return state.cost + calculate_heuristic_cost(state)

def calculate_heuristic_cost(state):
    heuristic_cost = 0
    for idx, tile in enumerate(state.config):
        if tile != 0:
            heuristic_cost += calculate_manhattan_dist(idx, tile, state.n)
    return heuristic_cost

def calculate_manhattan_dist(idx, value, n):
    """calculatet the manhattan distance of a tile"""
    target_map = {
        '1': (0, 1),
        '2': (0, 2),
        '3': (1, 0),
        '4': (1, 1),
        '5': (1, 2),
        '6': (2, 0),
        '7': (2, 1),
        '8': (2, 2)
    }

    current_row = idx // n
    current_column = idx % n
    target_row, target_column = target_map[str(value)]
    
    return abs(target_row - current_row) + abs(target_column - current_column)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    if list(puzzle_state.config) == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        return True
    else:
        return False

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    sm = sys.argv[1].lower() # search method
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)    

    start_time = time.time()
    mem_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    if sm == "bfs":
        result, final_states = bfs_search(hard_state)
    elif sm == "dfs":
        result, final_states = dfs_search(hard_state)
    elif sm == "ast":
        result, final_states = A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    mem_final = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    running_time = time.time() - start_time
    ram_usage = (mem_final - mem_init) / 1000

    if result:
        writeOutput(sm, final_states, (running_time, ram_usage))

if __name__ == '__main__':
    main()
