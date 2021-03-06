from collections import Counter

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

        polymer = self.polymerization(
            polymer_template, rules, steps=10, debug=False)
        print(f"Polymer of size: {len(polymer)}")

        most_common, less_common = self.calculate_most_less_common(polymer)
        print(f"Most common: {most_common}\nLess common: {less_common}")

        print(f"Final result: {most_common[1] - less_common[1]}")

    def part_2(self):
        polymer_template, rules = self.parsed_input

        counts = self.optimal_polymerization(polymer_template,
                                             rules,
                                             steps=40,
                                             debug=True)

        most_common, less_common = self.calculate_most_less_common_from_optimal(counts)
        print(f"Most common: {most_common}\nLess common: {less_common}")

        print(f"Final result: {most_common[1] - less_common[1]}")

    def polymerization(self, polymer_template: str, rules: dict, steps: int, debug: bool = False) -> str:
        polymer = polymer_template

        for step in range(steps):
            step_polymer = []

            for i in range(len(polymer)):

                # Don't forget the last letter!
                if i == len(polymer) - 1:
                    step_polymer.append(polymer[i])
                else:
                    pair = polymer[i] + polymer[i + 1]
                    result = polymer[i] + rules[pair].result
                    step_polymer.append(result)

            polymer = "".join(step_polymer)

            if debug:
                print(f"After step {step + 1}: size {len(polymer)}")
        return polymer

    def optimal_polymerization(self, polymer: str, rules: dict, steps: int, debug: bool = False) -> str:
        last_pairs = Counter([polymer[i]+polymer[i+1] for i in range(len(polymer) - 1)])
        char_count = Counter(polymer)

        for step in range(steps):
            # Generate new pairs
            new_pairs = Counter()
            
            for p, cnt in last_pairs.items():
                # Get the child character from this pair
                pair_result = rules[p].result

                # The result should be counted as many times as the parent pairs
                char_count.update({pair_result: cnt})

                # A pair produces 2 pairs
                for new_pair in [p[0] + pair_result, pair_result + p[1]]:
                    new_pairs.update({new_pair: cnt})

            last_pairs = new_pairs

            if debug:
                print(f"Step {step + 1}...")

        return char_count

    def calculate_most_less_common(self, polymer) -> tuple:
        count = Counter(polymer)
        max_key = max(count, key=count.get)
        min_key = min(count, key=count.get)
        return (max_key, count[max_key]), (min_key, count[min_key])

    def calculate_most_less_common_from_optimal(self, counts: Counter) -> tuple:
        max_key = max(counts, key=counts.get)
        min_key = min(counts, key=counts.get)
        return (max_key, counts[max_key]), (min_key, counts[min_key])



if __name__ == "__main__":
    Day14("14_input.txt").part_2()
