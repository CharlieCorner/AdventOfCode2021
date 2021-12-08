from abc import ABC, abstractmethod

def read_input_file(filename: str) -> list:

    with open(filename) as fp:
        lines = fp.readlines()
    
    return lines

class AdventDay(ABC):

    @staticmethod
    def read_input(filename: str):
        return read_input_file(filename)
    
    @abstractmethod
    def parse_input(self, lines: list) -> list:
        raise NotImplementedError
    
    @abstractmethod
    def part_1(self):
        raise NotImplementedError
    
    @abstractmethod
    def part_2(self):
        raise NotImplementedError