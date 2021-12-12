from advent_utils import AdventDay


class Day11(AdventDay):
    def __init__(self, filename: str = None) -> None:
        super().__init__(filename=filename)

    def parse_input(self, lines: list) -> list:
        octopuses = []

        for l in lines:
            l = l.strip()
            octopuses.append([int(o) for o in l])

        return octopuses

    def part_1(self):
        octopuses = self.parsed_input
        steps = 100
        num_flashes = self._simulate_steps(octopuses, steps)
        print(f"After {steps} steps, there have been a total of {num_flashes}")

    def part_2(self):
        return super().part_2()

    def _simulate_steps(self, octopuses: list, steps: int) -> int:
        num_of_flashes = 0

        self._print_octopuses(octopuses)

        for step in range(steps):

            flashing_octopi = {}

            # Increase the energy level by 1
            for x, row in enumerate(octopuses):
                for y, octopus in enumerate(row):
                    octopus = octopus + 1 if octopus < 9 else 0
                    octopuses[x][y] = octopus

            # Check and count for flashes
            for x, row in enumerate(octopuses):
                for y, octopus in enumerate(row):

                    # FLAAAAASH, AAAAAAAH!
                    if octopus == 0 and (x, y) not in flashing_octopi:
                        self._flash_neighbors(
                            (x, y), octopuses, flashing_octopi)

            num_of_flashes += len(flashing_octopi)

            print(f"After step {step + 1}:")
            self._print_octopuses(octopuses)

        return num_of_flashes

    # Oh my...
    def _flash_neighbors(self, initial_point: tuple, octopuses: list, flashing_octopi: dict) -> int:

        neighbor_stack = [initial_point]

        while neighbor_stack:
            x, y = neighbor_stack.pop()
            point_val = octopuses[x][y]

            # Share the powah
            if point_val == 0 and (x, y) not in flashing_octopi:

                flashing_octopi[(x, y)] = None

                for new_x, new_y in [
                    (x - 1, y),  # Up
                    (x + 1, y),  # Down
                    (x, y - 1),  # Left
                    (x, y + 1),  # Right
                    (x - 1, y - 1),  # Diag TopLeft
                    (x - 1, y + 1),  # Diag TopRight
                    (x + 1, y - 1),  # Diag BottomLeft
                    (x + 1, y + 1),  # Diag BottomRight
                ]:

                    # Check that coordinates are valid:
                    if (0 <= new_x < len(octopuses)) and (0 <= new_y < len(octopuses[0])):

                        octopuses, neighbor_stack = self._process_neighbor((new_x, new_y),
                                                                           octopuses,
                                                                           neighbor_stack,
                                                                           flashing_octopi)

    def _process_neighbor(self, neighbor_point: tuple, octopuses: list, neighbor_stack: list, flashing_octopi: dict) -> tuple:
        x, y = neighbor_point
        octo_val = octopuses[x][y]

        # The octopus is already flashing, don't attempt to increase its power level
        if octo_val == 0:
            if (x, y) not in flashing_octopi:
                neighbor_stack.append((x, y))
            
            return octopuses, neighbor_stack

        octopuses[x][y] = octo_val + 1 if octo_val < 9 else 0

        # Add unexplored flashing octopuses to the stack
        if octopuses[x][y] == 0 and (x, y) not in flashing_octopi:
            neighbor_stack.append((x, y))

        return octopuses, neighbor_stack

    def _print_octopuses(self, octopuses: list):
        print("\n".join([" ".join([str(d) for d in row])
              for row in octopuses]), end="\n\n")


if __name__ == "__main__":
    Day10("11_input.txt").part_1()
