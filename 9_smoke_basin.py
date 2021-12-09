from typing import final
from advent_utils import AdventDay


class Day9(AdventDay):
    def parse_input(self, lines: list) -> list:
        result = []

        for l in lines:
            result.append([int(c) for c in l.strip()])

        return result

    def part_1(self):
        heightmap = self.parse_input(self.read_input("9_input.txt"))
        low_points = self._detect_low_points(heightmap)
        risk_level = sum([heightmap[x][y] + 1 for x,y in low_points])

        print(f"{len(low_points)} Low points detected with a risk level of {risk_level}")


    def part_2(self):
        heightmap = self.parse_input(self.read_input("9_input.txt"))
        basin_sizes = self._detect_basin_sizes(heightmap, self._detect_low_points(heightmap))
        basin_sizes.sort()
        
        final_result = 1
        for size in basin_sizes[-3:]:
            final_result *= size

        print(f"{basin_sizes[-3:]} biggest basin sizes with a final result of {final_result}")

    def _detect_low_points(self, heightmap: list) -> list:
        result = []

        for x, row in enumerate(heightmap):
            for y, val in enumerate(row):
                neighbors = [val]
                # We need to check in a cross to see if val, the center, is indeed the
                #  lowest value, just make sure we do a boundary check
                
                # Left
                if y - 1 >= 0:
                    neighbors.append(heightmap[x][y - 1])

                # Right
                if y + 1 < len(row):
                    neighbors.append(heightmap[x][y + 1])

                # Up
                if x - 1 >= 0:
                    neighbors.append(heightmap[x - 1][y])

                # Down
                if x + 1 < len(heightmap):
                    neighbors.append(heightmap[x + 1][y])
                
                # Check the lowest value of the cross and exclude those that are all 9
                if val != 9 and val == min(neighbors):
                    result.append((x, y))

        return result

    def _detect_basin_sizes(self, heightmap: list, low_points: list) -> list:
        result = []

        for lp in low_points:
            result.append(len(self._explore_basins(heightmap, lp)))

        return result
    
    def _explore_basins(self, heightmap: list, lowest_point: tuple) -> list:
        basin = []

        # Store tuples of x,y coordinates
        explore_stack = [lowest_point]
        visited_points = {}

        while explore_stack:
            point = explore_stack.pop()
            x, y = point
            val = heightmap[x][y]
            visited_points[point] = None

            if val != 9:
                # The point is part of the basin
                if point not in basin:
                    basin.append((x,y))

                # Add neighbors to the explore stack if and only if we haven't visited them before
                # Left
                if y - 1 >= 0 and (x, y - 1) not in visited_points:
                    explore_stack.append((x, y - 1))

                # Right
                if y + 1 < len(heightmap[x]) and (x, y + 1) not in visited_points:
                    explore_stack.append((x, y + 1))

                # Up
                if x - 1 >= 0 and (x - 1, y) not in visited_points:
                    explore_stack.append((x - 1, y))

                # Down
                if x + 1 < len(heightmap) and (x + 1, y) not in visited_points:
                    explore_stack.append((x + 1, y))
        
        return basin

if __name__ == "__main__":
    Day9().part_2()
