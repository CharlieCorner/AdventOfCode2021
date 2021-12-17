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
        return super().part_1()

    def part_2(self):
        return super().part_2()


if __name__ == "__main__":
    Day15("15_test.txt").part_1()