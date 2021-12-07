def part_1():
    drawings, boards = parse_lines(read_input_file("4_case.txt"))

    last_num, winning_board = play_bingo(drawings, boards)

    print(winning_board)
    print(f"Last num: {last_num}. Board score: {winning_board.board_score}. Final score: {last_num * winning_board.board_score}")

def part_2():
    drawings, boards = parse_lines(read_input_file("4_case.txt"))

    last_num, winning_board = play_bingo(drawings, boards, should_win_quickly=False)

    print(winning_board)
    print(f"Last num: {last_num}. Board score: {winning_board.board_score}. Final score: {last_num * winning_board.board_score}")

def parse_lines(lines: list) -> tuple:
    drawings = [int(d) for d in lines[0].split(",") if d.isdigit()]
    boards = []

    # Parse Boards
    board_lines = []
    for i in range(2, len(lines)):
        l = lines[i].strip()

        if not l:
            boards.append(Board(board_lines))
            board_lines = []
            continue

        board_lines.extend([int(num) for num in l.split(" ") if num.isdigit()])
    
    if board_lines:
        boards.append(Board(board_lines))
    
    return drawings, boards

class Board:
    def __init__(self, grid_vals: list) -> None:
        self.grid_vals = grid_vals
        self.has_won = False
        self.markings = [False for val in range(len(grid_vals))]
    
    @property
    def board_score(self):
        result = 0

        for idx, mark in enumerate(self.markings):
            if not mark:
              result += self.grid_vals[idx]

        return result  

    def mark_number(self, num: int):
        for idx, val in enumerate(self.grid_vals):
            if val == num:
                self.markings[idx] = True
        self._check_for_win()
    
    def _check_for_win(self):
        
        # Check horizontally
        for h in range(0, len(self.grid_vals), 5):
            if all(self.markings[h:h+5]):
                self.has_won = True
                return

        # Check vertically
        for v in range(5):
            if all(self.markings[v::5]):
                self.has_won = True
                return
    
    def __str__(self) -> str:
        col_count = 1
        result = []
        row = []

        for i, val in enumerate(self.grid_vals):
            formatted_val = str(val)
            
            if self.markings[i]:
                formatted_val += "*"
            
            row.append(formatted_val)

            if col_count == 5:
                result.append(" ".join(row))
                row = []
                col_count = 1
            else:
                col_count += 1
        
        return "\n" + '\n'.join(result) + "\n"

def play_bingo(draws: list, boards: list, should_win_quickly: bool = True) -> tuple:
    last_num = None
    last_winning_board = None

    for d in draws:
    
        print(f"Drawing {d}...")
        for b in boards:
            b.mark_number(d)

            if should_win_quickly and b.has_won:
                return d, b
            elif not should_win_quickly and b.has_won:
                last_num = d
                last_winning_board = b
                boards = list(filter(lambda brd: not brd.has_won, boards))

    return last_num, last_winning_board


def read_input_file(filename: str) -> list:

    with open(filename) as fp:
        lines = fp.readlines()
    
    return lines

if __name__ == "__main__":
    part_2()
