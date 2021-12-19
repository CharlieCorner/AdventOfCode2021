from __future__ import annotations

import heapq

from advent_utils import AdventDay


class Day15(AdventDay):
    def parse_input(self, lines: list) -> list:
        cavern = []

        for l in lines:
            l = l.strip()

            cavern.append([int(d) for d in l])
            
        return cavern
    
    def part_1(self):
        cavern = self.parsed_input
        goal = (len(cavern) - 1, len(cavern[0]) - 1)
        result = self.navigate_cavern(cavern, goal)

        node = result["end_node"]

        print(f"Cost of solution at goal: {node.accumulated_cost}")
        

    def part_2(self):
        return super().part_2()

    def navigate_cavern(self, cavern: list,
                        goal: tuple,
                        start: tuple=(0,0)):
        frontier = []  # We'll heapify as we go along
        visited = set()

        start_node = NavigationNode(position=start,
                                    cavern = cavern,
                                    goal=goal)

        frontier.append(start_node)
        heapq.heapify(frontier)

        while frontier:

            current_node = heapq.heappop(frontier)

            if current_node.position == goal:
                return {
                    "end_node": current_node,
                    "visited": visited,
                    "success": True
                }

            for neighbor_position in current_node.get_possible_movements():

                if neighbor_position not in visited and not current_node.has_been_visited:
                    neighbor = NavigationNode(neighbor_position,
                                              goal,
                                              cavern,
                                              parent=current_node)
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
                 goal: tuple,
                 cavern: list,
                 parent: NavigationNode=None) -> None:
        self.position = position
        self.initial_cost = cavern[position[0]][position[1]]
        self.has_been_visited = False
        self.parent = parent
        self.goal = goal
        self.cavern = cavern

        # We don't count the start cost per the instructions
        self.accumulated_cost = 0 if not parent else parent.accumulated_cost + self.initial_cost
        self.prev_node = None
    
    @property
    def distance_to_goal(self):
        # Calculate the Manhattan distance to the goal
        manhattan_distance = abs(self.goal[0] - self.position[0]) + abs(self.goal[1] - self.position[1])
        return manhattan_distance
    
    @property
    def path_taken(self):
        path = []
        node = self

        while node:
            path.append(node.initial_cost)
            node = node.parent
        
        return path[::-1]
    
    def __lt__(self, other: NavigationNode):
        # Break the tie with the Manhattan distance
        #if self.accumulated_cost == other.accumulated_cost:
        #    return self.distance_to_goal < other.distance_to_goal
        total_cost = self.accumulated_cost + self.distance_to_goal
        other_total_cost = other.accumulated_cost + self.distance_to_goal
        return total_cost < other_total_cost
    
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
    Day15("15_input.txt").part_1()