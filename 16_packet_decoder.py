from __future__ import annotations

from advent_utils import AdventDay

def hexadecimal_2_binary(hexadecimal: str) -> str:
    hexa_mapping = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111"
    }
    binary = ""

    for h in hexadecimal:
        binary += hexa_mapping[h]
    
    return binary

def binary_2_decimal(binary: str) -> int:
    return int(binary, 2)

class PacketParser:
    
    @staticmethod
    def parse_packet(binary: str) -> Packet:
        raise NotImplementedError

class Packet:
    def __init__(self, version: int, type_id: int) -> None:
        self.version = version
        self.type_id = type_id
        self.subpackets = []


class LiteralValuePacket(Packet):
    def __init__(self, version: int, value_bits: str) -> None:
        self.value_bits = binary_2_decimal(value_bits)
        super().__init__(version, type_id=4)  # All LiteralValue packets are ID = 4


class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int, length_type_id:int , subpacket_data: str) -> None:
        
        self.length_type_id = length_type_id
        self.is_number_of_packets = length_type_id == 1

        self.length = 11 if self.is_number_of_packets else 15

        super().__init__(version, type_id)


class Day16(AdventDay):
    def parse_input(self, lines: list) -> list:
        return lines

    def part_1(self):
        packet = None

        for transmision in self.parsed_input:
            print(f"Transmission: {transmision}")
            
            binary_rep = hexadecimal_2_binary(transmision)
            print(f"Binary: {binary_rep}")

            packet = PacketParser.parse_packet(binary_rep)
        
        

    def part_2(self):
        return super().part_2()


if __name__ == "__main__":
    Day16("16_test.txt").part_1()
