"""
Python module for converting decimal to binary, octal, and hexadecimal.

Author: Roshaan Mehmood.

email: roshaan55@gmail.com

GitHub: https://github.com/roshaan555

Examples:
___________
**Decimal to Binary:**

import pynumsys as pns

dec_num = 115

print(pns.dec_to_bin(dec_num))

**Output:**

1110011

**Decimal to Octal:**

dec_num = 115

print(pns.dec_to_oct(dec_num))

**Output:**

163

**Decimal to Hexadecimal:**

dec_num = 115

print(pns.dec_to_hex(bin_str))

**Output:**

73

"""


def dec_to_bin(dec):
    """
    Converts decimal number to binary string.

    **Decimal:**

    In computing and programming, It is a base-10 number system that
    uses 10 digits, 0–9, to represent numeric values. It's also known as the
    base-10 positional numeral system or denary. Decimals are commonly used in
    software development and data analysis.

    These are a special type of fraction. For example, 1/10 can be written as
    a decimal or a fraction. A decimal can also be terminating or repeating.
    A terminating decimal has a finite number of digits after the decimal point,
    while a repeating decimal has a pattern of digits that repeats indefinitely.

    **Binary**

    It is a number system that uses only two digits, 0 and 1, to
    represent data and instructions in computers. It's also known as a
    "base 2" system because data is converted using the power of two.

    It is the language that computers use to communicate with each other
    and store information. All information that a computer processes, such as
    text, images, and sound, is represented as binary code.

    Example:
    ______________
    import pynumsys as pns

    dec_num = 115

    print(pns.dec_to_bin(dec_num))

    **Output:**

    1110011

    :param dec: decimal number to convert.
    :returns: binary string of decimal number.
    """
    if not isinstance(dec, str):
        if dec == 0:
            return '0'

        binary_str = ''
        while dec > 0:
            remainder = dec % 2
            binary_str = str(remainder) + binary_str
            dec //= 2
    else:
        raise ValueError("String not allowed, only integer or float")

    return binary_str


def dec_to_oct(dec):
    """
        Converts decimal number to octal string.

        **Decimal:**

        In computing and programming, It is a base-10 number system that
        uses 10 digits, 0–9, to represent numeric values. It's also known as the
        base-10 positional numeral system or denary. Decimals are commonly used in
        software development and data analysis.

        These are a special type of fraction. For example, 1/10 can be written as
        a decimal or a fraction. A decimal can also be terminating or repeating.
        A terminating decimal has a finite number of digits after the decimal point,
        while a repeating decimal has a pattern of digits that repeats indefinitely.

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

        dec_num = 115

        print(pns.dec_to_oct(dec_num))

        **Output:**

        163

        :param dec: decimal number to convert.
        :returns: octal string of decimal number.
    """
    if not isinstance(dec, str):
        octalNum = 0
        countval = 1
        dNo = dec

        while (dec != 0):
            # decimals remainder is calculated
            remainder = dec % 8

            # storing the octalvalue
            octalNum += remainder * countval

            # storing exponential value
            countval = countval * 10
            dec //= 8
    else:
        raise ValueError("String not allowed, only integer or float")

    return octalNum


def dec_to_hex(decimal):
    """
        Converts decimal number to octal string.

        **Decimal:**

        In computing and programming, It is a base-10 number system that
        uses 10 digits, 0–9, to represent numeric values. It's also known as the
        base-10 positional numeral system or denary. Decimals are commonly used in
        software development and data analysis.

        These are a special type of fraction. For example, 1/10 can be written as
        a decimal or a fraction. A decimal can also be terminating or repeating.
        A terminating decimal has a finite number of digits after the decimal point,
        while a repeating decimal has a pattern of digits that repeats indefinitely.

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

        dec_num = 115

        print(pns.dec_to_hex(dec_num))

        **Output:**

        73

        :param decimal: decimal number to convert.
        :returns: hexadecimal string of decimal number.
    """
    if not isinstance(decimal, str):
        integer_part = int(decimal)
        fractional_part = decimal - integer_part

        def int_to_hex(decimal):
            if decimal == 0:
                return '0'

            hex_chars = '0123456789ABCDEF'
            hexadecimal_str = ''

            while decimal > 0:
                remainder = decimal % 16
                hexadecimal_str = hex_chars[remainder] + hexadecimal_str
                decimal //= 16

            return hexadecimal_str

        def frac_to_hex(fractional, precision=8):
            hex_chars = '0123456789ABCDEF'
            hexadecimal_str = ''

            while fractional > 0 and len(hexadecimal_str) < precision:
                fractional *= 16
                digit = int(fractional)
                hexadecimal_str += hex_chars[digit]
                fractional -= digit

            return hexadecimal_str

        # Convert integer part to hexadecimal
        integer_hex = int_to_hex(integer_part)

        # Convert fractional part to hexadecimal if it's not zero
        if fractional_part > 0:
            fractional_hex = frac_to_hex(fractional_part)
            return f"{integer_hex}.{fractional_hex}"
        else:
            return integer_hex
    else:
        raise ValueError("String not allowed, only integer or float")


# Driver code
if __name__ == '__main__':
    print(dec_to_bin(115))
    print(dec_to_oct(115))
    print(dec_to_hex(115))
