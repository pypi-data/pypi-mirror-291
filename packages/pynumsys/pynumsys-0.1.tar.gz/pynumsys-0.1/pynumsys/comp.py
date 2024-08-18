"""
Python module for complementing binary string such as 1's complement and
2's complement and for hexadecimal string such as 15's complement and 16's
complement.

Author: Roshaan Mehmood.

email: roshaan55@gmail.com

GitHub: https://github.com/roshaan555

Examples:
___________
import pynumsys as pns

**2's Complement:**

bin_str = "1110011"

print(pns.twos_comp(bin_str, 8))

**Output:**

10001101

**1's Complement:**

bin_str = "1110011"

print(pns.ones_comp(bin_str, 8))

**Output:**

10001100

**15's Complement:**

hex_num = "73"

print(pns.fifteens_complement(hex_num))

**Output:**

8C

**16's Complement:**

hex_num = "73"

print(pns.sixteens_complement(hex_num))

**Output:**

8D

"""


def twos_comp(binary_str, bit_length=8):
    """
    Calculates 2's complement of a binary string.

    **2's Complement:**

    Two's complement is the most common method of representing signed
    (positive, negative, and zero) integers on computers, and more
    generally, fixed point binary values. Two's complement uses the
    binary digit with the greatest value as the sign to indicate whether
    the binary number is positive or negative; when the most significant
    bit is 1 the number is signed as negative and when the most significant
    bit is 0 the number is signed as positive. As a result, non-negative
    numbers are represented as themselves: 6 is 0110, zero is 0000, and -6
    is 1010 (~6 + 1). Note that while the number of binary bits is fixed
    throughout a computation it is otherwise arbitrary.

    Example:
    ____________
    import pynumsys as pns

    bin_str = "1110011"

    print(pns.twos_comp(bin_str, 8))

    **Output:** 10001101

    print(pns.twos_comp(bin_str, 12))

    **Output:** 111110001101

    print(pns.twos_comp(bin_str, 16))

    **Output:** 1111111110001101

    :param binary_str: binary string.
    :param bit_length: length of bits.
    :returns: 2's complement of binary string.
    """
    # Ensure the binary string fits within the specified bit length
    if len(binary_str) > bit_length:
        raise ValueError("Binary string length exceeds specified bit length.")

    # Pad the binary string with leading zeros to fit the bit length
    binary_str = binary_str.zfill(bit_length)

    # Step 1: Invert the bits
    inverted_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)

    # Step 2: Convert the inverted binary string to an integer
    inverted_value = int(inverted_str, 2)

    # Step 3: Add 1 to the inverted value to get the two's complement
    twos_complement_value = inverted_value + 1

    # Step 4: Convert back to binary string, ensuring it fits the bit length
    twos_complement_str = bin(twos_complement_value)[2:].zfill(bit_length)

    # Ensure the result fits within the specified bit length
    if len(twos_complement_str) > bit_length:
        twos_complement_str = twos_complement_str[-bit_length:]

    return twos_complement_str


def ones_comp(binary_str, bit_length=8):
    """
        Calculates 1's complement of a binary string.

        **1's Complement:**

        One's complement is the value of a binary number that is obtained by
        inverting all the bits in its binary representation. This means that
        0s are swapped for 1s and vice versa.

        One's complement can also be used to find the one's complement of a
        negative number. To do this, invert all the digits in the binary number.

        Example:
        ____________
        import pynumsys as pns

        bin_str = "1110011"

        print(pns.ones_comp(bin_str, 8))

        **Output:** 10001100

        print(twos_comp(bin_str, 12))

        **Output:** 111110001100

        print(twos_comp(bin_str, 16))

        **Output:** 1111111110001100

        :param binary_str: binary string.
        :param bit_length: length of bits.
        :returns: 1's complement of binary string.
    """
    if len(binary_str) > bit_length:
        raise ValueError("Binary string length exceeds specified bit length.")
    # Ensure the binary string fits within the specified bit length by padding with zeros
    binary_str = binary_str.zfill(bit_length)

    # Flip each bit in the binary string
    complement_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)

    return complement_str


def fifteens_complement(hex_num):
    """
        Calculates 1's complement of a binary string.

        **15's Complement:**

        15's complement of a number is obtained by subtracting all bits from FFFF

        Example:
        ____________
        import pynumsys as pns

        hex_num = "73"

        print(pns.fifteens_compliment(hex_num))

        **Output:** 8C

        :param hex_num: hexadecimal string.
        :returns: 15's complement of hexadecimal string.
    """
    # Convert the hex string to uppercase to handle lowercase inputs
    hex_num = hex_num.upper()

    # Create a mapping of hex digits to their 15's complement
    complement_map = {
        '0': 'F', '1': 'E', '2': 'D', '3': 'C',
        '4': 'B', '5': 'A', '6': '9', '7': '8',
        '8': '7', '9': '6', 'A': '5', 'B': '4',
        'C': '3', 'D': '2', 'E': '1', 'F': '0'
    }

    # Calculate the complement
    complement = ''.join(complement_map[digit] for digit in hex_num)

    return complement


def sixteens_complement(hex_num):
    """
        Calculates 1's complement of a binary string.

        **16's Complement:**

        16's complement of a number is obtained by subtracting all bits from
        FFFF and then adding 1 to obtained number.

        Example:
        ____________
        import pynumsys as pns

        hex_num = "73"

        print(pns.sixteens_compliment(hex_num))

        **Output:** 8D

        :param hex_num: hexadecimal string.
        :returns: 16's complement of hexadecimal string.
    """
    def add_one_to_hex(hex_str):
        # Reverse the string to handle addition from the least significant digit
        hex_str = hex_str[::-1]

        carry = 1
        result = []

        for digit in hex_str:
            if digit.isdigit():
                value = int(digit)
            else:
                value = ord(digit) - ord('A') + 10  # Convert 'A'-'F' to 10-15

            new_value = value + carry

            if new_value >= 16:
                carry = 1
                new_value -= 16
            else:
                carry = 0

            if new_value < 10:
                result.append(str(new_value))
            else:
                result.append(chr(new_value - 10 + ord('A')))

        if carry == 1:
            result.append('1')

        # Reverse the result back to the original order
        return ''.join(result[::-1])
    # Convert the hex string to uppercase to handle lowercase inputs
    hex_num = hex_num.upper()

    # Create a mapping of hex digits to their 15's complement
    complement_map = {
        '0': 'F', '1': 'E', '2': 'D', '3': 'C',
        '4': 'B', '5': 'A', '6': '9', '7': '8',
        '8': '7', '9': '6', 'A': '5', 'B': '4',
        'C': '3', 'D': '2', 'E': '1', 'F': '0'
    }

    # Calculate the 15's complement
    fifteens_complement = ''.join(complement_map[digit] for digit in hex_num)

    # Add 1 to the 15's complement manually
    sixteens_complement = add_one_to_hex(fifteens_complement)

    return sixteens_complement


if __name__ == '__main__':
    binary_input = "1110011"
    # bit_length = 8

    twos_comp = twos_comp(binary_input, 12)
    print(f"The two's complement of {binary_input} is {twos_comp}")
    print(f"The one's complement of {binary_input} is {ones_comp(binary_input)}")

    # Example usage
    hex_num = "73"
    fifteens_comp = fifteens_complement(hex_num)
    sixteens_comp = sixteens_complement(hex_num)
    print(f"The 15's complement of {hex_num} is {fifteens_comp}")
    print(f"The 15's complement of {hex_num} is {sixteens_comp}")
