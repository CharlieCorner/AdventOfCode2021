from advent_utils import AdventDay


class Chunk:

    illegal_char_scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }

    closing_char_scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }

    def __init__(self,
                 chunk: str,
                 is_corrupt: bool,
                 stack: list,
                 first_illegal_char: str = None) -> None:
        self.chunk = chunk
        self.is_corrupt = is_corrupt
        self.is_incomplete = not is_corrupt
        self.first_illegal_char = first_illegal_char
        self.stack = stack

        if is_corrupt:
            self.score = self._calculate_corrupt_score()
        else:
            self.missing_chars = self._calculate_missing_chars()
            self.score = self._calculate_incomplete_score()

    def _calculate_corrupt_score(self) -> int:
        return Chunk.illegal_char_scores[self.first_illegal_char]

    def _calculate_incomplete_score(self) -> int:
        score = 0

        for char in self.missing_chars:
            score *= 5
            score += Chunk.closing_char_scores[char]

        return score

    def _calculate_missing_chars(self) -> list:
        missing = []
        for open_char in self.stack[::-1]:
            if open_char == "(":
                missing.append(")")
            elif open_char == "[":
                missing.append("]")
            elif open_char == "{":
                missing.append("}")
            elif open_char == "<":
                missing.append(">")
        return missing

    def __str__(self) -> str:
        return self.chunk


class Day10(AdventDay):

    def parse_input(self, lines: list) -> list:
        return [l.strip() for l in lines]

    def part_1(self):
        chunks = self.parse_input(self.read_input("10_input.txt"))
        final_score = sum(
            [c.score for c in self._process_chunks(chunks) if c.is_corrupt])
        print(f"Final score: {final_score}")

    def part_2(self):
        chunks = self.parse_input(self.read_input("10_input.txt"))

        scores = [c.score for c in self._process_chunks(
            chunks) if c.is_incomplete]
        
        scores.sort()

        print(f"Final score: {scores[len(scores)//2]}")

    def _process_chunks(self, chunks: list) -> list:
        legal_pairs = {
            "()": None,
            "{}": None,
            "<>": None,
            "[]": None,
        }

        result = []

        for chunk in chunks:
            brace_stack = []
            chunk_is_corrupted = False

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
                        brace_stack.pop()  # We have closed a pair
                    else:
                        result.append(Chunk(chunk,
                                            is_corrupt=True,
                                            stack=brace_stack,
                                            first_illegal_char=char))
                        chunk_is_corrupted = True
                        break
            # If there's still something in the stack and the chunk is not corrupted,
            #  it is an incomplete chunk
            if not chunk_is_corrupted and brace_stack:
                result.append(Chunk(chunk,
                                    is_corrupt=False,
                                    stack=brace_stack))
        return result


if __name__ == "__main__":
    Day10().part_2()
