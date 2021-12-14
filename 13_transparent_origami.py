from __future__ import annotations

from advent_utils import AdventDay


class Day13(AdventDay):

    class PaperSheet:
        def __init__(self, markings: list) -> None:
            self.markings = markings

            # We have parse the file, let's represent the whole paper now
            # First, let's determine the total dimensions of the paper, we sum 1 so as to make it
            #  an inclusive range
            max_x = max([x for x, _ in markings])
            max_y = max([y for _, y in markings])

            marked_paper = []

            for x in range(max_x + 1):
                row = []
                for y in range(max_y + 1):
                    row.append("#" if (x, y) in markings else ".")
                marked_paper.append(row)

            self.marked_paper = marked_paper

        def __str__(self) -> str:
            # Given that x is the horizontal axis and y is the vertical one, we need to transpose
            #  the matrix so that we have a consistent human-readable interpretation of the sheet
            transposed_paper = list(zip(*self.marked_paper))
            return "\n".join([" ".join(row) for row in transposed_paper])

        def do_fold(self, axis: str, axis_position: int) -> Day13.PaperSheet:
            raise NotImplementedError

    def parse_input(self, lines: list) -> list:
        folds = []
        markings = []
        parse_folds = False

        for l in lines:
            l = l.strip()

            if not l:
                # We are about to parse folds
                parse_folds = True
                continue

            if not parse_folds:
                mark_x, mark_y = l.split(",")
                markings.append((int(mark_x), int(mark_y)))
            else:
                _, _, axis = l.split(" ")
                axis, axis_position = axis.split("=")
                folds.append((axis, int(axis_position)))

        marked_paper = Day13.PaperSheet(markings)

        return marked_paper, folds

    def part_1(self):
        marked_paper, folds = self.parsed_input

        return super().part_1()

    def part_2(self):
        return super().part_2()


if __name__ == "__main__":
    Day13("13_test.txt").part_1()
