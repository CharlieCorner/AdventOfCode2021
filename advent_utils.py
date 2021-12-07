def read_input_file(filename: str) -> list:

    with open(filename) as fp:
        lines = fp.readlines()
    
    return lines