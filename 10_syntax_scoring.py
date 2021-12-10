from advent_utils import AdventDay


class Day10(AdventDay):

    illegal_char_scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }

    def parse_input(self, lines: list) -> list:
        return [l.strip() for l in lines]

    def part_1(self):
        chunks = self.parse_input(self.read_input("10_input.txt"))
        final_score = self._calculate_score(self._first_illegal_chars(chunks))
        print(f"Final score: {final_score}")

    def part_2(self):
        chunks = self.parse_input(self.read_input("10_test.txt"))
        final_score = self._calculate_score(self._first_illegal_chars(chunks))
        print(f"Final score: {final_score}")

    def _calculate_score(self, illegal_chars: list) -> list:
        result = 0

        for ic in illegal_chars:
            result += Day10.illegal_char_scores[ic]

        return result

    def _first_illegal_chars(self, chunks: list) -> list:
        legal_pairs = {
            "()": None,
            "{}": None,
            "<>": None,
            "[]": None,
        }

        result = []

        for chunk in chunks:
            brace_stack = []

            for char in chunk:

                if not brace_stack:
                    brace_stack.append(char)
                    continue
                
                # Open braces are added to the stack, no questions asked
                if char in ["(", "{", "[", "<"]:
                    brace_stack.append(char)
                    continue

                # There must be an immediate matching closing bracket, else
                #  the entry is corrupted
                if char in [")", "}", "]", ">"]:
                    if brace_stack[-1] + char in legal_pairs:
                        brace_stack.pop() # We have closed a pair
                    else:
                        result.append(char)
                        break
        return result







if __name__ == "__main__":
    Day10().part_1()
