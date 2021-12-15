from __future__ import annotations

from advent_utils import AdventDay


class Day13(AdventDay):

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

        marked_paper = PaperSheet(markings)

        return marked_paper, folds

    def part_1(self):
        marked_paper, folds = self.parsed_input
        print(f"Start as: \n {str(marked_paper)}")

        for axis, axis_position in folds:
            marked_paper.do_fold(axis, axis_position)
            print("\n\nNew shape:")
            print(str(marked_paper))
            print(f"Marks count: {marked_paper.num_markings}")
            break

    def part_2(self):
        return super().part_2()


class PaperSheet:
    def __init__(self, markings: list) -> None:
        self.markings = markings

        # We have parse the file, let's represent the whole paper now
        # First, let's determine the total dimensions of the paper, we sum 1 so as to make it
        #  an inclusive range
        self.max_x = max([x for x, _ in markings])
        self.max_y = max([y for _, y in markings])

        marked_paper = []

        for x in range(self.max_x + 1):
            row = []
            for y in range(self.max_y + 1):
                row.append("#" if (x, y) in markings else ".")
            marked_paper.append(row)

        self.marked_paper = marked_paper

    def __str__(self) -> str:
        # Given that x is the horizontal axis and y is the vertical one, we need to transpose
        #  the matrix so that we have a consistent human-readable interpretation of the sheet
        transposed_paper = list(zip(*self.marked_paper))
        return "\n".join([" ".join(row) for row in transposed_paper])

    def _set_marked_paper(self, marked_paper):
        self.marked_paper = marked_paper
        self.max_y = len(self.marked_paper[0]) - 1
        self.max_x = len(self.marked_paper) - 1

    @property
    def num_markings(self):
        result = 0

        for y, row in enumerate(self.marked_paper):
            for x, val in enumerate(row):
                result += 1 if "#" == val else 0
        return result

    def do_fold(self, axis: str, axis_position: int) -> PaperSheet:
        if "x" == axis:
            # Let's fold the paper horizontally
            # Create a new paper that has been folded
            new_marked_paper = self.marked_paper[:axis_position]

            for y in range(self.max_y + 1):
                for x in range(axis_position + 1, self.max_x + 1):
                    distance = x - axis_position
                    target_x = axis_position - distance

                    if "#" == self.marked_paper[x][y]:
                        new_marked_paper[target_x][y] = "#"
            
            self._set_marked_paper(new_marked_paper)

        else:
            # Let's fold the paper up, for that calculate the distance of the points BELOW the fold
            #  line to the fold line, then substract that to the position of the fold line to get
            #  the new y coordinate and update accordingly
            # Given that we have stored the matrix "sideways", to fold up we are really folding
            #  horizontally for axis y

            # Create a new paper that has been folded
            new_marked_paper = [y[:axis_position]
                                for y in [x for x in self.marked_paper]]

            for y in range(axis_position + 1, self.max_y + 1):
                for x in range(self.max_x + 1):
                    distance = y - axis_position
                    target_y = axis_position - distance

                    if "#" == self.marked_paper[x][y]:
                        new_marked_paper[x][target_y] = "#"

            self._set_marked_paper(new_marked_paper)


if __name__ == "__main__":
    Day13("13_input.txt").part_1()
