from __future__ import annotations

import heapq

from advent_utils import AdventDay


class Day15(AdventDay):
    def parse_input(self, lines: list) -> list:
        cavern = []
        nodes = {}

        for x, line in enumerate(lines):
            line = line.strip()
            row = []

            for y, cost in enumerate(line):
                cost = int(cost)
                row.append(cost)

                nodes[(x,y)] = NavigationNode((x,y),
                                              cost)
            cavern.append(row)
            
        return cavern, nodes
    
    def part_1(self):
        cavern, nodes = self.parsed_input
        goal = (9,9)
        result = self.navigate_cavern(cavern, nodes, goal)

        costs = []
        node = result["end_node"]
        while node:
            costs.append(node.initial_cost)
            node = node.prev_node

        print(f"Cost of solution at goal: {sum(costs)}")
        

    def part_2(self):
        return super().part_2()

    def navigate_cavern(self, cavern: list,
                        nodes: dict,
                        goal: tuple,
                        start: tuple=(0,0)):
        frontier = []  # We'll heapify as we go along
        visited = set()
        
        for node in nodes.values():
            node.goal = goal
            node.cavern = cavern

        frontier.append(nodes[start])
        heapq.heapify(frontier)

        while frontier:

            # In order to preserve how the heap looked like when we processed the node, let's create a string with the info
            
            #heap_snapshot = "[" + ", ".join([f"F(x)={x.cost}" for x in frontier]) + "]"
            current_node = heapq.heappop(frontier)

            # We add the heap information to the current node so that, when we traverse the final solution, we'll see how
            #  the heap looked like in chronological order.
            current_node.accumulated_cost = current_node.prev_node.cost_of_solution if current_node.prev_node else current_node.initial_cost

            if current_node.position == goal:
                return {
                    "end_node": current_node,
                    "visited": visited,
                    "success": True
                }

            for neighbor in current_node.get_possible_movements():
                neighbor = nodes[neighbor]

                if neighbor.position not in visited and not current_node.has_been_visited:
                    neighbor.prev_node = current_node
                    heapq.heappush(frontier, neighbor)

            visited.add(current_node.position)
            current_node.has_been_visited = True

        return {
            "visited": visited,
            "success": False
        }

class NavigationNode:
    def __init__(self,
                 position: tuple,
                 initial_cost: int) -> None:
        self.position = position
        self.initial_cost = initial_cost
        self.has_been_visited = False
        
        # To be set later
        self.accumulated_cost = 0
        self.cavern = None
        self.goal = None
        self.prev_node = None
    
    @property
    def cost_of_solution(self):
        # if not self.goal:
        return self.initial_cost
        #else:
            # Calculate the Manhattan distance to the goal
            # manhattan_distance = abs(self.goal[0] - self.position[0]) + abs(self.goal[1] - self.position[1])
            #return manhattan_distance + self.accumulated_cost
    
    def __lt__(self, other: NavigationNode):
        return self.cost_of_solution <= other.cost_of_solution
    
    def get_possible_movements(self) -> list:
        x, y = self.position

        legal_moves = []

        for move in [
            (x - 1, y), # UP
            (x + 1, y), # DOWN
            (x, y - 1), # LEFT
            (x, y + 1), # RIGHT
        ]:
            new_x, new_y = move
            if 0 <= new_x < len(self.cavern) and 0 <= new_y < len(self.cavern[0]):
                legal_moves.append(move)
        
        return legal_moves


if __name__ == "__main__":
    Day15("15_test.txt").part_1()