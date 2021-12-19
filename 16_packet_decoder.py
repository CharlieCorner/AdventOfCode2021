from __future__ import annotations
from types import DynamicClassAttribute

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
        # Parse the header with the version and type
        version = binary_2_decimal(binary[:3])
        type = binary_2_decimal(binary[3:6])
        data = binary[6:]

        if type == 4:
            return LiteralValuePacket(version=version,
                                      data=data)
        else:
            return OperatorPacket(version=version,
                                  type_id=type,
                                  data=data)

    @staticmethod
    def detect_packet_boundaries(binary: str) -> list:
        raise NotImplementedError


class Packet:
    def __init__(self, version: int, type_id: int) -> None:
        self.version = version
        self.type_id = type_id
        self.subpackets = []
        self.value = None


class LiteralValuePacket(Packet):
    def __init__(self, version: int, data: str) -> None:
        super().__init__(version, type_id=4)  # All LiteralValue packets are ID = 4

        self.value = self._parse_value(data)

    def _parse_data(self, data):
        continue_parsing_data = True
        index = 0
        val = ""

        while continue_parsing_data:
            val += data[index + 1:index + 5]
            continue_parsing_data = data[index] == "1"
            index += 5
        return binary_2_decimal(val)


class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int, data: str) -> None:
        super().__init__(version, type_id)

        self.length_type_id = int(data[0])
        self.is_number_of_packets = self.length_type_id == 1

        # Remove the bit that we have consumed
        data = data[1:]

        if self.is_number_of_packets:
            num_packets = binary_2_decimal(data[:11])
            data = data[11:]

            for _ in range(num_packets):
                self.subpackets.append(PacketParser.parse_packet(data[:11]))
                data = data[11:]
        else:
            bits_in_subpackets = binary_2_decimal(data[:15])
            data = data[15:]
            self.subpackets.extend(
                PacketParser.detect_packet_boundaries(data[:bits_in_subpackets]))


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
