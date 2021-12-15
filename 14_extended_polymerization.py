from advent_utils import AdventDay

class Rule:
    def __init__(self, origin: str, result: str) -> None:
        self.origin = origin
        self.result = result

class Day14(AdventDay):
    def parse_input(self, lines: list) -> list:
        polymer_template = None
        rules = {}

        for l in lines:
            l = l.strip()
            
            if not polymer_template:
                polymer_template = l
                continue

            if not l:
                continue

            origin, result = l.split(" -> ")
            rules[origin] = Rule(origin, result)
        
        return polymer_template, rules

    def part_1(self):
        polymer_template, rules = self.parsed_input
        return super().part_1()

    def part_2(self):
        return super().part_2()


if __name__ == "__main__":
    Day14("14_test.txt").part_1()
