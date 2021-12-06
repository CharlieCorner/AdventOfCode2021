def part_1():
    transposed_bits = transpose(parse_bits(read_input_file("3_test.txt")))

    gamma_rate, epsilon_rate = calculate_gamma_epsilon_rate(transposed_bits)

    power_consumption = gamma_rate * epsilon_rate

    print(f"Gamma: {gamma_rate}, epsilon: {epsilon_rate}, power: {power_consumption}")
    

def part_2():
    bits = parse_bits(read_input_file("3_test.txt"))

    o2_gen_rating = calculate_o2_rating(bits)

    co2_scrubber_rating = calculate_co2_rating(bits)

    life_support_rating = o2_gen_rating * co2_scrubber_rating

    print(f"O2 Rating: {o2_gen_rating}, co2_rating: {co2_scrubber_rating}, life_support_rating: {life_support_rating}")

def calculate_o2_rating(bits: list) -> int:
    num_digits = len(bits[0])
    
    # Start with all the numbers
    result = bits.copy()

    # Test for each of the column of digits
    for i in range(num_digits):

        sum_col_digits = sum([candidate[i] for candidate in result])
        max_sum = len(result)

        # Determine value to keep
        if sum_col_digits >= max_sum / 2:
            most_common_value = 1
        else:
            most_common_value = 0

        # Remove numbers that don't have the most common value in them
        result = list(filter(lambda candidate: candidate[i] == most_common_value, result))

        if len(result) == 1:
            break
    
    return binary_2_int(result[0])


def calculate_co2_rating(bits: list) -> int:
    num_digits = len(bits[0])
    
    # Start with all the numbers
    result = bits.copy()

    # Test for each of the column of digits
    for i in range(num_digits):
        sum_col_digits = sum([candidate[i] for candidate in result])
        max_sum = len(result)

        # Determine value to keep
        if sum_col_digits >= max_sum / 2:
            least_common_value = 0
        else:
            least_common_value = 1

        # Remove numbers that don't have the most common value in them
        result = list(filter(lambda candidate: candidate[i] == least_common_value, result))

        if len(result) == 1:
            break
    
    return binary_2_int(result[0])

def calculate_gamma_epsilon_rate(transposed_bits: list) -> tuple:
    gamma_binary = []
    epsilon_binary = []

    for column_of_bits in transposed_bits:
        max_bits = len(column_of_bits)
        bit_sum = sum(column_of_bits)

        if bit_sum > max_bits/2:
            gamma_binary.append(1)
            epsilon_binary.append(0)
        else:
            gamma_binary.append(0)
            epsilon_binary.append(1)
    
    return binary_2_int(gamma_binary), binary_2_int(epsilon_binary)

def binary_2_int(binary: list) -> int:
    # Convert from list of binary to int by shifting the bits and OR with the result
    int_res = 0
    for b in binary:
        int_res = (int_res << 1) | b
    return int_res

def parse_bits(lines: list) -> list:
    bits = []

    # Convert each digit from str to a list of int
    for l in lines:
        digits = []

        for d in l:
            if d.isdigit():
                digits.append(int(d))
        
        bits.append(digits)
    
    return bits

def transpose(matrix: list) -> list:
        # Transpose the matrix to get count the columns easily treating them as rows
    return list(zip(*matrix))
    
def read_input_file(filename: str) -> list:

    with open(filename) as fp:
        lines = fp.readlines()
    
    return lines

if __name__ == "__main__":
    part_2()
