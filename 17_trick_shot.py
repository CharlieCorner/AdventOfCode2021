import re

from advent_utils import AdventDay


class Day17(AdventDay):
    def parse_input(self, lines: list) -> list:
        # target area: x=20..30, y=-10..-5
        target = re.sub('[:,]+', '', lines[0]) # We only expect one line
        target = target.split(" ")[2:]

        x = target[0].split("=")[1].split("..")
        y = target[1].split("=")[1].split("..")

        min_x, max_x = [int(d) for d in x]
        min_y, max_y = [int(d) for d in y]
        return min_x, max_x, min_y, max_y

    def part_1(self):
        min_x, max_x, min_y, max_y = self.parsed_input
        return super().part_1()

    def part_2(self):
        return super().part_2()


if __name__ == "__main__":
    Day17("17_test.txt").part_1()
