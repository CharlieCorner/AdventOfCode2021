from __future__ import annotations
from types import DynamicClassAttribute
from abc import ABC, abstractmethod

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
    def parse_data_stream(data: str) -> Packet:

        version = binary_2_decimal(data[:3])
        type = binary_2_decimal(data[3:6])

        if type == 4:
            new_packet = LiteralValuePacket(version=version,
                                            data=data[6:])
        else:
            new_packet = OperatorPacket(version=version,
                                        type_id=type,
                                        data=data[6:])
        return new_packet

    @staticmethod
    def sum_versions(packet: Packet) -> int:
        result = 0
        stack = [packet]

        # We'll perform a DFS to get all of the packets
        while stack:
            p = stack.pop()
            result += p.version
            stack.extend(p.subpackets)
            
        return result


class Packet:
    def __init__(self, version: int, type_id: int, data: str) -> None:
        self.version = version
        self.type_id = type_id
        self.subpackets = []
        self.value = None
        self.parsed_bits = self.parse_data(data)

    @abstractmethod
    def parse_data(self, data: str) -> list:
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self.value) if self.value else str(self.subpackets)


class LiteralValuePacket(Packet):
    def __init__(self, version: int, data: str) -> None:
        # All LiteralValue packets are ID = 4
        super().__init__(version, type_id=4, data=data)

    def parse_data(self, data: str) -> int:
        continue_parsing_data = True
        index = 0
        val = ""

        while continue_parsing_data:
            continue_parsing_data = data[index] == "1"
            val += data[index + 1:index + 5]
            index += 5

        self.value = binary_2_decimal(val)

        # Count the bits in the header that were already parsed by the PacketParser
        return index + 6


class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int, data: str) -> None:
        super().__init__(version, type_id, data=data)

    def parse_data(self, data: str) -> int:
        index = 0

        self.length_type_id = int(data[index])
        self.is_number_of_packets = self.length_type_id == 1

        index += 1

        if self.is_number_of_packets:
            num_packets = binary_2_decimal(data[index:index + 11])
            index += 11

            for _ in range(num_packets):
                new_packet = PacketParser.parse_data_stream(data[index:])
                self.subpackets.append(new_packet)
                index += new_packet.parsed_bits
        else:
            bits_in_subpackets = binary_2_decimal(data[index:index + 15])
            index += 15
            bit_limit = index + bits_in_subpackets

            while index < bit_limit:
                new_packet = PacketParser.parse_data_stream(data[index:])
                self.subpackets.append(new_packet)
                index += new_packet.parsed_bits

        # We add to the count the 6 bits needed for the headers
        return index + 6


class Day16(AdventDay):
    def parse_input(self, lines: list) -> list:
        return lines

    def part_1(self):
        packet = None

        for transmision in self.parsed_input:
            print(f"Transmission: {transmision}")

            binary_rep = hexadecimal_2_binary(transmision)
            print(f"Binary: {binary_rep}")

            packet = PacketParser.parse_data_stream(binary_rep)

            sum_versions = PacketParser.sum_versions(packet)

            print(f"The sum of version for {transmision} is: {sum_versions}")

    def part_2(self):
        return super().part_2()


if __name__ == "__main__":
    Day16("16_test.txt").part_1()
