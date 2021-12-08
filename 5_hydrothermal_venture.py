from advent_utils import read_input_file

def part_1():
    line_coordinates = expand_coordinates(parse_coordinates(read_input_file("5_input.txt")))
    count_coord = count_coordinates(line_coordinates)
    dangerous_points = len(list(filter(lambda c: c > 1, count_coord.values())))
    print(f"There are {dangerous_points} dangerous points!")

def part_2():
    line_coordinates = expand_coordinates(parse_coordinates(read_input_file("5_input.txt")),
                                          consider_diagon=True)
    count_coord = count_coordinates(line_coordinates)
    dangerous_points = len(list(filter(lambda c: c > 1, count_coord.values())))
    print(f"There are {dangerous_points} dangerous points!")

def parse_coordinates(lines: list) -> list:
    result = []

    for l in lines:
        xy1, xy2 = l.split("->")
        x1, y1 = xy1.strip().split(",")
        x2, y2 = xy2.strip().split(",")

        result.append(((int(x1), int(y1)), (int(x2), int(y2))))

    return result

def expand_coordinates(pairs: list, consider_diagon: bool = False) -> list:
    result = []

    for p in pairs:
        row = []
        xy1, xy2 = p

        x1, y1 = xy1
        x2, y2 = xy2

        is_diagonal = x1 != x2 and y1 != y2

        if is_diagonal and not consider_diagon:
            continue

        if not is_diagonal:
            # We want to iterate by adding numbers in the for loop, so let's determine
            #  the start_x and start_y to be the lesser coordinate
            # We add 1 to the limit to the right to make the range inclusive
            start_x = min(x1, x2)
            end_x = max(x1, x2) + 1

            start_y = min(y1, y2)
            end_y = max(y1, y2) + 1

            # These nested loops will allow us to move horizontally or vertically without
            #  having to detect the direction of the line
            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    row.append((x, y))
        else:
            # For diagonal movement we need to increase/decrease x and y at the same rate, we
            #  need to detect the direction of the diagonal
            step_x = 1 if x1 < x2 else -1
            step_y = 1 if y1 < y2 else -1

            pos_x = x1
            pos_y = y1

            # We add the step so as to respect direction and make sure the interval is inclusive
            while pos_x != x2 + step_x and pos_y != y2 + step_y:
                row.append((pos_x, pos_y))
                pos_x += step_x
                pos_y += step_y

        result.append(row)
    
    return result

def count_coordinates(coordinates: list) -> dict:
    result = {}

    for list_coord in coordinates:
        for coord in list_coord:
            if coord in result:
                result[coord] += 1
            else:
                result[coord] = 1
    
    return result


if __name__ == "__main__":
    part_2()
