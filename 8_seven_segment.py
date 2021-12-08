from advent_utils import AdventDay


class Day8(AdventDay):
    def parse_input(self, lines: list) -> tuple:
        signals = []
        four_digits = []

        for l in lines:
            s, d = l.split("|")
            signals.append([i for i in s.strip().split(" ")])
            four_digits.append([i for i in d.strip().split(" ")])

        return signals, four_digits

    def part_1(self):
        unique_signals, four_digits = self.parse_input(
            self.read_input("8_input.txt"))

        num_unique_segments = self.count_unique_segments(four_digits)

        print(f"Unique segments appear {num_unique_segments} times")

    def part_2(self):
        unique_signals, four_digits = self.parse_input(
            self.read_input("8_input.txt"))

        final_result = sum([self.deduce_numbers(
            unique_signals[i], four_digits[i]) for i in range(len(unique_signals))])

        print(f"Final sum of deduced numbers is: {final_result}")

    def deduce_numbers(self, signals: list, digits: list) -> int:
        # Deduce unique segments first 1,4,7,8
        deductions = {}
        pending_deductions = []

        for s in signals:
            length = len(s)

            if length == 2:
                deductions[1] = s
            elif length == 4:
                deductions[4] = s
            elif length == 3:
                deductions[7] = s
            elif length == 7:
                deductions[8] = s
            else:
                pending_deductions.append(s)

        for pd in pending_deductions:
            if len(pd) == 6:

                # We can deduce the 9 by knowing that it's the number with 6 segments that
                #  contains both all segments in 4 and 7
                is_nine = all([seg in pd for seg in deductions[4] + deductions[7]])
                if is_nine:
                    deductions[9] = pd
                    # Remove the 9 from the pending deductions
                    pending_deductions = list(
                        filter(lambda seg: seg != pd, pending_deductions))
                    break

        for pd in pending_deductions:
            if len(pd) == 6:
                # With 9 out of the way, we can now use 7 to determine who is 6
                is_six = not all(seg in pd for seg in deductions[7])
                if is_six:
                    deductions[6] = pd
                    pending_deductions = list(
                        filter(lambda seg: seg != pd, pending_deductions))
                    continue

                if not is_six:
                    deductions[0] = pd
                    pending_deductions = list(
                        filter(lambda seg: seg != pd, pending_deductions))
                    continue

        # Let's deduce now the numbers with 5 segments based on what we already have
        for pd in pending_deductions:
            if len(pd) == 5:
                # 3 can be determined by using 1
                is_three = all(seg in pd for seg in deductions[1])
                if is_three:
                    deductions[3] = pd
                    # Remove the 3 from the pending deductions
                    pending_deductions = list(
                        filter(lambda seg: seg != pd, pending_deductions))
                    continue

                # 5 can be determined by using 6 because all segments in six must be in 5
                is_five = all(seg in deductions[6] for seg in pd)
                if is_five:
                    deductions[5] = pd
                    # Remove the 5 from the pending deductions
                    pending_deductions = list(
                        filter(lambda seg: seg != pd, pending_deductions))
                    continue

                if not is_five and not is_three:
                    deductions[2] = pd
                    pending_deductions = list(
                        filter(lambda seg: seg != pd, pending_deductions))
                    continue
        # With the deduction done, let's reverse the k,v of the map for easier lookup
        result = 0
        factor = 1000
        for d in digits:
            for num, segments in deductions.items():
                if len(d) == len(segments) and all(seg in d for seg in segments):
                    result += num * factor
                    factor //= 10
                    break
        return result

    def count_unique_segments(self, digits: list):
        # Unique segments are 1 (uses 2 segments), 4 (4 segments), 7 (3 segments) and 8 (7 segments)
        unique_count = 0

        for line in digits:
            for digit in line:
                if len(digit) in [2, 3, 4, 7]:
                    unique_count += 1

        return unique_count


if __name__ == "__main__":
    Day8().part_2()
