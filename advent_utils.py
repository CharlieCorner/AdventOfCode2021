from abc import ABC, abstractmethod


def read_input_file(filename: str) -> list:

    with open(filename) as fp:
        lines = fp.readlines()

    return [l.strip() for l in lines]


class AdventDay(ABC):

    def __init__(self, filename: str = None) -> None:
        if filename:
            self.parsed_input = self.parse_input(self.read_input(filename))

    @staticmethod
    def read_input(filename: str):
        return read_input_file(filename)
    
    @staticmethod
    def parse_matrix_numbers(lines: list) -> list:
        matrix_num = []

        for l in lines:
            matrix_num.append([int(d) for d in l])
            
        return matrix_num

    @abstractmethod
    def parse_input(self, lines: list) -> list:
        raise NotImplementedError

    @abstractmethod
    def part_1(self):
        raise NotImplementedError

    @abstractmethod
    def part_2(self):
        raise NotImplementedError
