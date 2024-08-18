"""
Python module for converting octal to decimal, binary, and hexadecimal.It
is also capable of performing all arithmatic operations in octal such as
octal addition, subtraction, multiplication and division. More over if you
want the output of addition, subtraction, multiplication and division in
another specific number system such as output in octal, binary it can do
it for you.


Author: Roshaan Mehmood.

email: roshaan55@gmail.com

GitHub: https://github.com/roshaan555

Examples:
___________
**Octal to Decimal:**

import pynumsys as pns

hex_str = "163"

print(pns.oct_to_dec(hex_str))

**Output:**

115

**Hexadecimal to Binary:**

hex_str = "163"

print(pns.hex_to_bin(hex_str))

**Output:**

1110011

**Hexadecimal to Octal:**

hex_str = "163"

print(pns.oct_to_hex(hex_str))

**Output:**

73

"""

from pynumsys.decimal import dec_to_bin, dec_to_hex


def oct_to_bin(octal_str):
    """
        Converts octal string to binary.

        **Octal:**

        This number system, or base-8 system, is a numeral system that uses
        numbers from 0 to 7 to represent numbers. It's a crucial system in computing
        because it can simplify binary code expression.

        Octal numbers can be used to represent binary values in a compact way, condensing
        three binary digits into a single octal digit. This makes it easier to read and
        reduces the length of numerical representations, which is useful when dealing with
        large binary values.

        **Binary:**

        It is a number system that uses only two digits, 0 and 1, to
        represent data and instructions in computers. It's also known as a
        "base 2" system because data is converted using the power of two.

        It is the language that computers use to communicate with each other
        and store information. All information that a computer processes, such as
        text, images, and sound, is represented as binary code.

        Example:
        ______________
        import pynumsys as pns

        hex_str = "163"

        print(oct_to_bin(hex_str))

        **Output:**

        1110011

        :param octal_str: octal string to convert.
        :returns: binary of octal input string.
    """
    if isinstance(octal_str, str):
        deci = oct_to_dec(octal_str)
        binary_str = dec_to_bin(deci)
    else:
        raise ValueError("Input must be of string data type.")
    return binary_str


def oct_to_dec(octal_str):
    """
        Converts octal string to decimal.

        **Octal:**

        This number system, or base-8 system, is a numeral system that uses
        numbers from 0 to 7 to represent numbers. It's a crucial system in computing
        because it can simplify binary code expression.

        Octal numbers can be used to represent binary values in a compact way, condensing
        three binary digits into a single octal digit. This makes it easier to read and
        reduces the length of numerical representations, which is useful when dealing with
        large binary values.

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

        hex_str = "163"

        print(pns.oct_to_dec(hex_str))

        **Output:**

        115

        :param octal_str: octal string to convert.
        :returns: decimal of octal input string.
    """
    if isinstance(octal_str, str):
        decimal = 0
        power = 0
        for digit in reversed(octal_str):
            decimal += int(digit) * (8 ** power)
            power += 1
    else:
        raise ValueError("Input must be of string data type.")
    return decimal


def oct_to_hex(octal_str):
    """
        Converts octal string to hexadecimal.

        **Octal:**

        This number system, or base-8 system, is a numeral system that uses
        numbers from 0 to 7 to represent numbers. It's a crucial system in computing
        because it can simplify binary code expression.

        Octal numbers can be used to represent binary values in a compact way, condensing
        three binary digits into a single octal digit. This makes it easier to read and
        reduces the length of numerical representations, which is useful when dealing with
        large binary values.

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

        hex_str = "163"

        print(pns.oct_to_hex(hex_str))

        **Output:**

        73

        :param octal_str: octal string to convert.
        :returns: hexadecimal of octal input string.
    """
    if isinstance(octal_str, str):
        deci = oct_to_dec(octal_str)
        hexadecimal_str = dec_to_hex(deci)
    else:
        raise ValueError("Input must be of string data type.")
    return hexadecimal_str


def oct_add(a, b, output="octal"):
    """
        Adds two octal numbers without using built-in functions.

        Notes:
        --------------
        You can change output to any other number system such as binary, decimal,
        hexadecimal etc...

        Here are some ways to do it:

        **Decimal:** syntax ---> **oct_add(a, b, output="decimal")**.

        **Binary:** syntax ---> **oct_add(a, b, output="binary")**.

        **Octal:** syntax ---> **oct_add(a, b, output="hexa")**.

        Examples:
        --------------
        import pynumsys as pns

        print(pns.oct_add("73", "4A"))

        333

        print(pns.oct_add("73", "4A", output="binary"))

        11011011

        print(pns.oct_add("73", "4A", output="hexa"))

        DB


        :param a: octal number 1.
        :param b: octal number 2.
        :param output: output string.
                By default, it outputs octal output but if you want to change to binary you
                can simply write **oct_add(a, b, output="binary")**.
        :returns: Addition of two octal numbers a and b.
    """

    def octal_digits_to_bits(octal_str):
        # Each octal digit represents 3 bits
        return len(octal_str) * 3

    # Determine the bit length based on the inputs
    max_len = max(len(a), len(b))
    bit_length = octal_digits_to_bits('0' * max_len)

    # Pad the octal numbers to the same length
    a = a.zfill(max_len)
    b = b.zfill(max_len)

    result = []
    carry = 0

    # Perform addition from right to left
    for i in range(max_len - 1, -1, -1):
        digit_sum = int(a[i], 8) + int(b[i], 8) + carry
        result.append(oct(digit_sum % 8)[2:])
        carry = digit_sum // 8

    if carry:
        result.append(oct(carry)[2:])

    # Reverse the result and pad with zeros to match the bit length
    result_str = ''.join(result[::-1]).zfill(max_len)
    if output == "octal":
        return result_str
    if output == "binary":
        return oct_to_bin(result_str)
    if output == "hexa":
        return oct_to_hex(result_str)
    if output == "decimal":
        return oct_to_dec(result_str)
    else:
        raise ValueError("Invalid Option. Please choose from one of these given options:"
                         """\noutput=\"octal\""""
                         """\noutput=\"binary\""""
                         """\noutput=\"hexa\""""
                         """\noutput=\"decimal\"""")


def oct_sub(a, b, output="octal"):
    """
        Subtracts two octal numbers without using built-in functions.

        Notes:
        --------------
        You can change output to any other number system such as binary, decimal,
        hexadecimal etc...

        Here are some ways to do it:

        **Decimal:** syntax ---> **oct_sub(a, b, output="decimal")**.

        **Binary:** syntax ---> **oct_sub(a, b, output="binary")**.

        **Octal:** syntax ---> **oct_sub(a, b, output="hexa")**.

        Examples:
        --------------
        import pynumsys as pns

        print(pns.oct_sub("73", "4A"))

        013

        print(pns.oct_sub("73", "4A", output="binary"))

        1011

        print(pns.hex_sub("73", "4A", output="hexa"))

        B


        :param a: octal number 1.
        :param b: octal number 2.
        :param output: output string.
                By default, it outputs octal output but if you want to change to binary you
                can simply write **oct_sub(a, b, output="binary")**.
        :returns: Subtraction of two octal numbers a and b.
    """
    def octal_digits_to_bits(octal_str):
        # Each octal digit represents 3 bits
        return len(octal_str) * 3

    # Determine the bit length based on the inputs
    max_len = max(len(a), len(b))
    bit_length = octal_digits_to_bits('0' * max_len)

    # Pad the octal numbers to the same length
    a = a.zfill(max_len)
    b = b.zfill(max_len)

    result = []
    borrow = 0

    # Perform subtraction from right to left
    for i in range(max_len - 1, -1, -1):
        digit_diff = int(a[i], 8) - int(b[i], 8) - borrow

        if digit_diff < 0:
            digit_diff += 8
            borrow = 1
        else:
            borrow = 0

        result.append(oct(digit_diff)[2:])

    # Reverse the result, remove leading zeros, and pad with zeros to match the bit length
    result_str = ''.join(result[::-1]).lstrip('0').zfill(max_len)
    if output == "octal":
        return result_str
    if output == "binary":
        return oct_to_bin(result_str)
    if output == "hexa":
        return oct_to_hex(result_str)
    if output == "decimal":
        return oct_to_dec(result_str)
    else:
        raise ValueError("Invalid Option. Please choose from one of these given options:"
                         """\noutput=\"octal\""""
                         """\noutput=\"binary\""""
                         """\noutput=\"hexa\""""
                         """\noutput=\"decimal\"""")


def oct_mul(a, b, output="octal"):
    """
        Multiplies two octal numbers without using built-in functions.

        Notes:
        --------------
        You can change output to any other number system such as binary, decimal,
        hexadecimal etc...

        Here are some ways to do it:

        **Decimal:** syntax ---> **oct_mul(a, b, output="decimal")**.

        **Binary:** syntax ---> **oct_mul(a, b, output="binary")**.

        **Octal:** syntax ---> **oct_mul(a, b, output="hexa")**.

        Examples:
        --------------
        import pynumsys as pns

        print(pns.oct_mul("73", "4A"))

        27270

        print(pns.oct_mul("73", "4A", output="binary"))

        10111010111000

        print(pns.oct_mul("73", "4A", output="hexa"))

        2EB8


        :param a: octal number 1.
        :param b: octal number 2.
        :param output: output string.
                By default, it outputs octal output but if you want to change to binary you
                can simply write **oct_mul(a, b, output="binary")**.
        :returns: Multiplication of two octal numbers a and b.
    """
    # Initialize the result as a list of zeros
    result = [0] * (len(a) + len(b))

    # Reverse the strings to make it easier to multiply from right to left
    a, b = a[::-1], b[::-1]

    # Perform the multiplication digit by digit
    for i in range(len(a)):
        for j in range(len(b)):
            product = int(a[i], 8) * int(b[j], 8)
            result[i + j] += product
            result[i + j + 1] += result[i + j] // 8
            result[i + j] %= 8

    # Remove leading zeros from the result
    while len(result) > 1 and result[-1] == 0:
        result.pop()

    if output == "octal":
        return ''.join(oct(digit)[2:] for digit in result[::-1])
    if output == "binary":
        return oct_to_bin(''.join(oct(digit)[2:] for digit in result[::-1]))
    if output == "hexa":
        return oct_to_hex(''.join(oct(digit)[2:] for digit in result[::-1]))
    if output == "decimal":
        return oct_to_dec(''.join(oct(digit)[2:] for digit in result[::-1]))
    else:
        raise ValueError("Invalid Option. Please choose from one of these given options:"
                         """\noutput=\"octal\""""
                         """\noutput=\"binary\""""
                         """\noutput=\"hexa\""""
                         """\noutput=\"decimal\"""")


def oct_div(dividend, divisor, output="octal", quot=False):
    """
        Divides two octal numbers without using built-in functions.

        Notes:
        --------------
        You can change output to any other number system such as binary, decimal,
        octal etc...

        Here are some ways to do it:

        **Decimal:** syntax ---> **oct_div(a, b, output="decimal")**.

        **Binary:** syntax ---> **oct_div(a, b, output="binary")**.

        **Octal:** syntax ---> **oct_div(a, b, output="hexa")**.


        If you want quotient from division it can return it by optional parameter
        **'quot'** which by default is False and the syntax is given below:


        **Syntax: oct_div(a, b, quot="True")**


        Examples:
        --------------
        import pynumsys as pns

        print(pns.oct_div("73", "4A"))

        13

        print(pns.oct_div("73", "4A", output="binary"))

        1011

        print(pns.oct_div("73", "4A", output="hexa"))

        B

        Output with quotient:

        print(pns.oct_div("73", "4A", quot="True"))

        ('1', '13')

        Output without quotient:

        print(pns.oct_div("73", "4A"))

        13

        :param dividend: octal number 1.
        :param divisor: octal number 2.
        :param output: output string.
                By default, it outputs octal output but if you want to change to binary you
                can simply write **oct_div(a, b, output="binary")**.
        :param quot: quotient.
                (Optional) Boolean Value which defaults false. If you want quotient you can make it True
                and it will give quotient and remainder in a tuple.
        :returns: Division of two octal numbers a and b with quotient(optional).
    """
    if quot:
        if int(divisor, 8) == 0:
            raise ValueError("Divisor cannot be zero.")

        # Convert dividend and divisor from octal to decimal for the division process
        dividend_decimal = int(dividend, 8)
        divisor_decimal = int(divisor, 8)

        # Perform the division in decimal
        quotient_decimal = dividend_decimal // divisor_decimal
        remainder_decimal = dividend_decimal % divisor_decimal

        # Convert quotient and remainder back to octal
        quotient = oct(quotient_decimal)[2:]  # Strip the '0o' prefix
        remainder = oct(remainder_decimal)[2:]  # Strip the '0o' prefix

        lst = quotient, remainder

        return tuple(map(int, lst))
    else:
        dividend_decimal = int(dividend, 8)
        divisor_decimal = int(divisor, 8)

        # Perform the division in decimal
        remainder_decimal = dividend_decimal % divisor_decimal

        # Convert quotient and remainder back to octal
        remainder = oct(remainder_decimal)[2:]  # Strip the '0o' prefix
        if output == "octal":
            return remainder
        if output == "binary":
            return oct_to_bin(remainder)
        if output == "hexa":
            return oct_to_hex(remainder)
        if output == "decimal":
            return oct_to_dec(remainder)
        else:
            raise ValueError("Invalid Option. Please choose from one of these given options:"
                             """\noutput=\"octal\""""
                             """\noutput=\"binary\""""
                             """\noutput=\"hexa\""""
                             """\noutput=\"decimal\"""")


if __name__ == '__main__':
    # Example usage
    # octal_str = "163"
    # binary_str = oct_to_bin(octal_str)
    # print(binary_str)
    # print(oct_to_dec(octal_str))
    # print(oct_to_hex(octal_str))

    print(oct_add("163", "150"))
    print(oct_sub("163", "150"))
    print(oct_mul("163", "150", "hexa"))
    print(oct_div("163", "150"))
