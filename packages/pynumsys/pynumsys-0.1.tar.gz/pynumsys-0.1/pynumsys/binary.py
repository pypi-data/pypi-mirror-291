"""
Python module for converting binary to decimal, octal, and hexadecimal.It
is also capable of performing all arithmatic operations in binary such as
binary addition, subtraction, multiplication and division.

Author: Roshaan Mehmood.

email: roshaan55@gmail.com

GitHub: https://github.com/roshaan555

Examples:
___________
import pynumsys as pns

**Binary to Decimal:**

bin_str = "1110011"

print(pns.bin_to_dec(bin_str))

**Output:**

115

**Binary to Octal:**

bin_str = "1110011"

print(pns.bin_to_oct(bin_str))

**Output:**

163

**Binary to Hexadecimal:**

bin_str = "1110011"

print(pns.bin_to_hex(bin_str))

**Output:**

73

"""
from pynumsys.decimal import dec_to_hex


def bin_to_dec(binary):
    """
    Converts binary string to decimal.

    **Binary:**

    It is a number system that uses only two digits, 0 and 1, to
    represent data and instructions in computers. It's also known as a
    "base 2" system because data is converted using the power of two.

    It is the language that computers use to communicate with each other
    and store information. All information that a computer processes, such as
    text, images, and sound, is represented as binary code.

    **Decimal:**

    In computing and programming, It is a base-10 number system that
    uses 10 digits, 0–9, to represent numeric values. It's also known as the
    base-10 positional numeral system or denary. Decimals are commonly used in
    software development and data analysis.

    These are a special type of fraction. For example, 1/10 can be written as
    a decimal or a fraction. A decimal can also be terminating or repeating.
    A terminating decimal has a finite number of digits after the decimal point,
    while a repeating decimal has a pattern of digits that repeats indefinitely.

    Example:
    ______________
    import pynumsys as pns

    bin_str = "1110011"

    print(pns.bin_to_dec(bin_str))

    **Output:**

    115

    :param binary: binary string to convert.
    :returns: decimal of binary input string.
    """
    if isinstance(binary, str):
        deci = 0
        for digit in binary:
            deci = deci * 2 + int(digit)
    else:
        raise ValueError("Input must be of string data type.")
    return deci


def bin_to_oct(binary_str):
    """
        Converts binary string to octal.

        **Binary:**

        It is a number system that uses only two digits, 0 and 1, to
        represent data and instructions in computers. It's also known as a
        "base 2" system because data is converted using the power of two.

        It is the language that computers use to communicate with each other
        and store information. All information that a computer processes, such as
        text, images, and sound, is represented as binary code.

        **Octal:**

        This number system, or base-8 system, is a numeral system that uses
        numbers from 0 to 7 to represent numbers. It's a crucial system in computing
        because it can simplify binary code expression.

        Octal numbers can be used to represent binary values in a compact way, condensing
        three binary digits into a single octal digit. This makes it easier to read and
        reduces the length of numerical representations, which is useful when dealing with
        large binary values.

        Example:
        ______________
        import pynumsys as pns

        bin_str = "1110011"

        print(pns.bin_to_oct(bin_str))

        **Output:**

        163

        :param binary_str: binary string to convert.
        :returns: octal of binary input string.
    """
    if isinstance(binary_str, str):
        while len(binary_str) % 3 != 0:
            binary_str = '0' + binary_str

        # Dictionary to map binary triplets to their octal equivalents
        binary_to_octal_map = {
            '000': '0',
            '001': '1',
            '010': '2',
            '011': '3',
            '100': '4',
            '101': '5',
            '110': '6',
            '111': '7'
        }

        # Convert each group of three binary digits to its octal equivalent
        octal_str = ''
        for i in range(0, len(binary_str), 3):
            triplet = binary_str[i:i + 3]
            octal_str += binary_to_octal_map[triplet]
    else:
        raise ValueError("Input must be of string data type.")

    return octal_str


def bin_to_hex(binary_str):
    """
        Converts binary string to octal.

        **Binary:**

        It is a number system that uses only two digits, 0 and 1, to
        represent data and instructions in computers. It's also known as a
        "base 2" system because data is converted using the power of two.

        It is the language that computers use to communicate with each other
        and store information. All information that a computer processes, such as
        text, images, and sound, is represented as binary code.

        **Hexadecimal:**

        It is a numbering system with a base of 16 that uses 16
        symbols to represent numbers. It's used in computer science to
        represent large numbers in a more compact way.

        It uses the numbers 0–9, along with the letters A–F to
        represent the values 10–15. For example, in the hexadecimal number
        3F416, the 4 is in the ones place, the F (or 15 in decimal) is in the
        sixteens place, and the 3 is in the two-hundred-and-fifty-six place.

        Example:
        ______________
        import pynumsys as pns

        bin_str = "1110011"

        print(pns.bin_to_hex(bin_str))

        **Output:**

        73

        :param binary_str: binary string to convert.
        :returns: hexadecimal of binary input string.
    """
    if isinstance(binary_str, str):
        deci = bin_to_dec(binary_str)
        hexadecimal_str = dec_to_hex(deci)
    else:
        raise ValueError("Input must be of string data type.")
    return hexadecimal_str


def bin_add(a, b):
    """
        Adds two binary numbers without using built-in functions.

        Example:
        --------------
        import pynumsys as pns

        print(pns.bin_add("1010", "1101"))

        10111

        :param a: binary number 1.
        :param b: binary number 2.
        :returns: Addition of two binary numbers a and b.
    """
    max_len = max(len(a), len(b))

    # Pad the shorter binary number with leading zeros
    a = a.zfill(max_len)
    b = b.zfill(max_len)

    result = ''
    carry = 0

    # Perform bit-by-bit addition from right to left
    for i in range(max_len - 1, -1, -1):
        bit_sum = carry
        bit_sum += 1 if a[i] == '1' else 0
        bit_sum += 1 if b[i] == '1' else 0

        result = ('1' if bit_sum % 2 == 1 else '0') + result
        carry = 0 if bit_sum < 2 else 1

    if carry != 0:
        result = '1' + result

    return result


def bin_sub(a, b):
    """
        Subtracts two binary numbers without using built-in functions.

        Example:
        --------------
        import pynumsys as pns

        print(pns.bin_sub("1101", "1010"))

        11

        :param a: binary number 1.
        :param b: binary number 2.
        :returns: Addition of two binary numbers a and b.
    """
    max_len = max(len(a), len(b))

    # Pad the shorter binary number with leading zeros
    a = a.zfill(max_len)
    b = b.zfill(max_len)

    result = ''
    borrow = 0

    # Perform bit-by-bit subtraction from right to left
    for i in range(max_len - 1, -1, -1):
        bit_diff = (1 if a[i] == '1' else 0) - (1 if b[i] == '1' else 0) - borrow

        if bit_diff >= 0:
            result = ('1' if bit_diff == 1 else '0') + result
            borrow = 0
        else:
            result = '1' + result
            borrow = 1

    # Remove leading zeros
    return result.lstrip('0')


def bin_mul(a, b):
    """
        Multiplies two binary numbers without using built-in functions.

        Example:
        --------------
        import pynumsys as pns

        print(pns.bin_mul("101", "11"))

        11

        :param a: binary number 1.
        :param b: binary number 2.
        :returns: Multiplication of two binary numbers a and b.
    """
    a = a[::-1]
    b = b[::-1]
    result = '0'

    for i in range(len(b)):
        if b[i] == '1':
            result = bin_add(result, a + '0' * i)

    return result


def bin_div(dividend, divisor):
    """
        Divides two binary numbers without using built-in functions.

        Example:
        --------------
        import pynumsys as pns

        print(pns.bin_div("1101", "11"))

        100

        :param dividend: binary number 1.
        :param divisor: binary number 2.
        :returns: Multiplication of two binary numbers a and b.
    """
    dividend = list(dividend)
    divisor_len = len(divisor)
    quotient = ''

    temp = dividend[:divisor_len]

    for i in range(divisor_len, len(dividend) + 1):
        if ''.join(temp).lstrip('0') >= divisor:
            quotient += '1'
            temp = list(bin_sub(''.join(temp), divisor))
        else:
            quotient += '0'

        if i < len(dividend):
            temp.append(dividend[i])

    return quotient.lstrip('0')


if __name__ == '__main__':
    # print(bin_to_dec("1110011"))
    # print(bin_to_oct("1110011"))
    # print(bin_to_hex("1110011"))

    print(bin_add("1010", "1101"))
    print(bin_sub("1101", "1010"))
    print(bin_mul("101", "11"))
    print(bin_div("1101", "11"))
