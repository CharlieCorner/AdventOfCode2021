from statistics import median

from advent_utils import AdventDay


class Day7(AdventDay):
    def parse_input(self, lines: list) -> list:
        result = []
        for l in lines:
            result.extend([int(d) for d in l.split(",") if d.isdigit()])
        return result

    def part_1(self):
        crab_hor_pos = self.parse_input(self.read_input("7_input.txt"))
        
        # Calculate the position at which everyone is closer
        optimal_pos = int(median(crab_hor_pos))

        fuel_spent = self._calculate_spent_fuel(crab_hor_pos, optimal_pos)

        print(f"The crabs would spend {fuel_spent} in fuel to get to {optimal_pos}")

    def part_2(self):
        crab_hor_pos = self.parse_input(self.read_input("7_input.txt"))
        
        # Calculate the position at which everyone is closer
        optimal_pos = int(sum(crab_hor_pos) / len(crab_hor_pos))

        fuel_spent = self._calculate_spent_fuel(crab_hor_pos,
                                                optimal_pos,
                                                True)

        print(f"The crabs would spend {fuel_spent} in fuel to get to {optimal_pos}")

    def _calculate_spent_fuel(self, positions: list,
                              target: int,
                              use_crab_engineering: bool = False) -> int:
        if not use_crab_engineering:
            return sum([abs(crab - target) for crab in positions])
        else:
            return sum([sum(range(1, abs(crab - target) + 1)) for crab in positions])


if __name__ == "__main__":
    Day7().part_2()
