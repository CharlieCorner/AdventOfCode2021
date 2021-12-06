def part_1():
    instructions = parse_instructions(read_input_file("2_input_case.txt"))

    horizontal_position = 0
    depth = 0

    for instruction in instructions:
        direction, units = instruction

        if direction == "forward":
            horizontal_position += units
        elif direction == "up":
            depth -= units
        elif direction == "down":
            depth += units
    
    print(f"Final depth: {depth}. Horizontal position: {horizontal_position}")
    print(f"Multiplication result: {depth * horizontal_position}")


def part_2():
    instructions = parse_instructions(read_input_file("2_input_case.txt"))

    horizontal_position = 0
    depth = 0
    aim = 0

    for instruction in instructions:
        direction, units = instruction

        if direction == "forward":
            horizontal_position += units
            depth += aim * units

        elif direction == "up":
            aim -= units
        elif direction == "down":
            aim += units
    
    print(f"Final depth: {depth}. Horizontal position: {horizontal_position}")
    print(f"Multiplication result: {depth * horizontal_position}")

def parse_instructions(lines: str) -> list:
    instructions = []

    for l in lines:
        i, units = l.split()
        units = int(units)
        instructions.append((i, units))
    
    return instructions

def read_input_file(filename: str) -> list:

    with open(filename) as fp:
        lines = fp.readlines()
    
    return lines

if __name__ == "__main__":
    part_2()
