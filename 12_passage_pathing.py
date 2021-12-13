# So that I can use type annotations for the self class
from __future__ import annotations

from advent_utils import AdventDay


class Day12(AdventDay):
    def parse_input(self, lines: list) -> list:
        caves = {}

        for l in lines:
            l = l.strip()
            from_cave_name, to_cave_name = l.split("-")

            # Get or create the caves with the given names
            from_cave = caves[from_cave_name] if from_cave_name in caves else Cave(
                from_cave_name)
            to_cave = caves[to_cave_name] if to_cave_name in caves else Cave(
                to_cave_name)

            # Create bidirectional connections between the caves
            from_cave.connect_to(to_cave)
            to_cave.connect_to(from_cave)

            caves[from_cave_name] = from_cave
            caves[to_cave_name] = to_cave

        return caves

    def part_1(self):
        cave_map = self.parsed_input
        nav = Navigator(cave_map=cave_map)
        result = nav.start_navigation()

        result = [str(point) for point in result]
        result.sort()

        for point in result:
            print(point)

        print(f"There are {len(result)} possible paths.")

    def part_2(self):
        cave_map = self.parsed_input
        nav = Navigator(cave_map=cave_map)

        nav.Pointer.small_cave_visits_allowed = 1

        result = nav.start_navigation()

        result = [str(point) for point in result]
        result.sort()

        for point in result:
            print(point)

        print(f"There are {len(result)} possible paths.")


class Cave:
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_small = name.islower()
        self.is_start = "start" == name
        self.is_end = "end" == name
        self.connections = []

    def connect_to(self, other_cave: Cave):
        if other_cave not in self.connections:
            self.connections.append(other_cave)

    def __str__(self) -> str:
        return self.name


class Navigator:

    class Pointer:

        small_cave_visits_allowed = 1

        def __init__(self, current_cave: Cave,
                     prev_pointer: Navigator.Pointer = None) -> None:
            self.current_cave = current_cave
            self.reached_end = current_cave.is_end

            if prev_pointer:
                self.path_so_far = prev_pointer.path_so_far.copy()
                self.visited_caves = prev_pointer.visited_caves.copy()
                self.has_visited_small_cave_twice = prev_pointer.has_visited_small_cave_twice
            else:
                self.path_so_far = []
                self.visited_caves = {}
                self.has_visited_small_cave_twice = False

            # Add tracking of the current cave
            self.path_so_far.append(current_cave)

            if current_cave in self.visited_caves:
                self.visited_caves[current_cave] += 1
            else:
                self.visited_caves[current_cave] = 1

        def get_next_caves(self) -> list:
            if self.reached_end:
                return []

            # Apply rules of navigation
            result = []
            for next_cave in self.current_cave.connections:

                if self.cave_should_be_explored(next_cave):
                    result.append(Navigator.Pointer(next_cave, self))

            return result

        def cave_should_be_explored(self, next_cave: Cave) -> bool:
            # Big caves are exempt of conditions
            if not next_cave.is_small:
                return True

            # Don't go back to the beginning
            if next_cave.is_start:
                return False

            # Run for the goal!
            if next_cave.is_end:
                return True

            # We are only allowed to continue if we haven't explored a cave twice yet
            # if next_cave.is_small and self.has_visited_small_cave_twice:
            #    return False

            cave_visits_quota = self.visited_caves[next_cave] if next_cave in self.visited_caves else 0

            has_visits_quota = cave_visits_quota < self.small_cave_visits_allowed

            small_cave_allowed = next_cave.is_small and has_visits_quota

            # We can only visit a small cave more than once, once
            self.has_visited_small_cave_twice = True

            return small_cave_allowed

        def __str__(self) -> str:
            return ",".join([cave.name for cave in self.path_so_far])

    def __init__(self, cave_map: dict) -> None:
        self.cave_map = cave_map
        self.pointer_stack = []
        self.found_paths = []

    def start_navigation(self) -> list:
        self.pointer_stack.append(self.Pointer(self.cave_map["start"]))

        while self.pointer_stack:
            pointer = self.pointer_stack.pop()

            if pointer.reached_end:
                self.found_paths.append(pointer)
            else:
                self.pointer_stack.extend(pointer.get_next_caves())

        return self.found_paths


if __name__ == "__main__":
    Day12("12_input.txt").part_2()
