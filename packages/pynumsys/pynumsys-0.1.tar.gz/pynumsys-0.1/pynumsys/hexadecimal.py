"""
Python module for converting hexadecimal to decimal, binary, and octal.It is
also capable of performing all arithmatic operations in hexadecimal such as
hexadecimal addition, subtraction, multiplication and division. More over if
you want the output of addition, subtraction, multiplication and division in
another specific number system such as output in octal, binary it can do it
for you.


Author: Roshaan Mehmood.

email: roshaan55@gmail.com

GitHub: https://github.com/roshaan555

Examples:
___________
**Hexadecimal to Decimal:**

import pynumsys as pns

hex_str = "29"

print(pns.hex_to_dec(hex_str))

**Output:**

41

**Hexadecimal to Binary:**

hex_str = "29"

print(pns.hex_to_bin(hex_str))

**Output:**

101001

**Hexadecimal to Octal:**

hex_str = "29"

print(pns.hex_to_oct(hex_str))

**Output:**

51

"""
from pynumsys.decimal import dec_to_bin, dec_to_oct


def hex_to_bin(hex_str):
    """
    Converts hexadecimal string to binary.

    **Hexadecimal:**

    It is a numbering system with a base of 16 that uses 16
    symbols to represent numbers. It's used in computer science to
    represent large numbers in a more compact way.

    It uses the numbers 0–9, along with the letters A–F to
    represent the values 10–15. For example, in the hexadecimal number
    3F416, the 4 is in the ones place, the F (or 15 in decimal) is in the
    sixteens place, and the 3 is in the two-hundred-and-fifty-six place.

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

    hex_str = "29"

    print(pns.hex_to_bin(hex_str))

    **Output:**

    101001

    :param hex_str: hexadecimal string to convert.
    :returns: binary of hexadecimal input string.
    """
    if isinstance(hex_str, str):
        deci = hex_to_dec(hex_str)
        binary_str = dec_to_bin(deci)
    else:
        raise ValueError("Input must be of string data type.")
    return binary_str


def hex_to_dec(hex_str):
    """
        Converts hexadecimal string to decimal.

        **Hexadecimal:**

        It is a numbering system with a base of 16 that uses 16
        symbols to represent numbers. It's used in computer science to
        represent large numbers in a more compact way.

        It uses the numbers 0–9, along with the letters A–F to
        represent the values 10–15. For example, in the hexadecimal number
        3F416, the 4 is in the ones place, the F (or 15 in decimal) is in the
        sixteens place, and the 3 is in the two-hundred-and-fifty-six place.

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

        hex_str = "29"

        print(pns.hex_to_dec(hex_str))

        **Output:**

        41

        :param hex_str: hexadecimal string to convert.
        :returns: decimal of hexadecimal input string.
    """
    if isinstance(hex_str, str):
        hex_to_dec_map = {
            '0': 0, '1': 1, '2': 2, '3': 3,
            '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, 'A': 10, 'B': 11,
            'C': 12, 'D': 13, 'E': 14, 'F': 15
        }

        hex_str = hex_str.upper()

        deci = 0

        for char in hex_str:
            deci = deci * 16 + hex_to_dec_map[char]
    else:
        raise ValueError("Input must be of string data type.")
    return deci


def hex_to_oct(hex_str):
    """
        Converts hexadecimal string to octal.

        **Hexadecimal:**

        It is a numbering system with a base of 16 that uses 16
        symbols to represent numbers. It's used in computer science to
        represent large numbers in a more compact way.

        It uses the numbers 0–9, along with the letters A–F to
        represent the values 10–15. For example, in the hexadecimal number
        3F416, the 4 is in the ones place, the F (or 15 in decimal) is in the
        sixteens place, and the 3 is in the two-hundred-and-fifty-six place.

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

        hex_str = "29"

        print(pns.hex_to_oct(hex_str))

        **Output:**

        51

        :param hex_str: hexadecimal string to convert.
        :returns: octal of hexadecimal input string.
        """
    if isinstance(hex_str, str):
        deci = hex_to_dec(hex_str)
        octal_str = dec_to_oct(deci)
    else:
        raise ValueError("Input must be of string data type.")
    return octal_str


def hex_add(a, b, output="hexa"):
    """
    Adds two hexadecimal numbers without using built-in functions.

    Notes:
    --------------
    You can change output to any other number system such as binary, decimal,
    octal etc...

    Here are some ways to do it:

    **Decimal:** syntax ---> **hex_add(a, b, output="decimal")**.

    **Binary:** syntax ---> **hex_add(a, b, output="binary")**.

    Octal: syntax ---> hex_add(a, b, output="octal").

    Examples:
    --------------
    import pynumsys as pns

    print(pns.hex_add("73", "4A"))

    BD

    print(pns.hex_add("73", "4A", output="binary"))

    10111101

    print(pns.hex_add("73", "4A", output="octal"))

    275


    :param a: hexadecimal number 1.
    :param b: hexadecimal number 2.
    :param output: output string.
            By default, it outputs hexadecimal output but if you want to change to binary you
            can simply write **hex_add(a, b, output="binary")**.
    :returns: Addition of two hexadecimal numbers a and b.
    """
    if isinstance(a, str) and isinstance(b, str):
        hex_digits = "0123456789ABCDEF"
        carry = 0
        result = ""

        # Make both hex numbers the same length by padding with '0'
        a = a.zfill(max(len(a), len(b)))
        b = b.zfill(max(len(a), len(b)))

        # Perform addition from the rightmost digit to the left
        for i in range(len(a) - 1, -1, -1):
            sum_digits = hex_digits.index(a[i]) + hex_digits.index(b[i]) + carry
            carry = sum_digits // 16
            result = hex_digits[sum_digits % 16] + result

        # If there's a carry left, add it
        if carry:
            result = hex_digits[carry] + result

        if output == "hexa":
            return result
        if output == "binary":
            return hex_to_bin(result)
        if output == "decimal":
            return hex_to_dec(result)
        if output == "octal":
            return hex_to_oct(result)
        else:
            raise ValueError("Invalid Option. Please choose from one of these given options:"
                             """\noutput=\"hexa\""""
                             """\noutput=\"binary\""""
                             """\noutput=\"decimal\""""
                             """\noutput=\"octal\"""")
    else:
        raise ValueError("Inputs must be of string data type.")


def hex_sub(a, b, output="hexa"):
    """
        Subtracts two hexadecimal numbers without using built-in functions.

        Notes:
        --------------
        You can change output to any other number system such as binary, decimal,
        octal etc...

        Here are some ways to do it:

        **Decimal:** syntax ---> **hex_sub(a, b, output="decimal")**.

        **Binary:** syntax ---> **hex_sub(a, b, output="binary")**.

        **Octal:** syntax ---> **hex_sub(a, b, output="octal")**.

        Examples:
        --------------
        import pynumsys as pns

        print(pns.hex_sub("73", "4A"))

        29

        print(pns.hex_sub("73", "4A", output="binary"))

        101001

        print(pns.hex_sub("73", "4A", output="octal"))

        51


        :param a: hexadecimal number 1.
        :param b: hexadecimal number 2.
        :param output: output string.
                By default, it outputs hexadecimal output but if you want to change to binary you
                can simply write **hex_sub(a, b, output="binary")**.
        :returns: Subtraction of two hexadecimal numbers a and b.
        """
    if isinstance(a, str) and isinstance(b, str):
        hex_digits = "0123456789ABCDEF"
        borrow = 0
        result = ""

        # Make both hex numbers the same length by padding with '0'
        a = a.zfill(max(len(a), len(b)))
        b = b.zfill(max(len(a), len(b)))

        # Perform subtraction from the rightmost digit to the left
        for i in range(len(a) - 1, -1, -1):
            diff = hex_digits.index(a[i]) - hex_digits.index(b[i]) - borrow
            if diff < 0:
                diff += 16
                borrow = 1
            else:
                borrow = 0
            result = hex_digits[diff] + result

        if output == "hexa":
            return result.lstrip("0") or "0"
        if output == "binary":
            return hex_to_bin(result.lstrip("0") or "0")
        if output == "decimal":
            return hex_to_dec(result.lstrip("0") or "0")
        if output == "octal":
            return hex_to_oct(result.lstrip("0") or "0")
        else:
            raise ValueError("Invalid Option. Please choose from one of these given options:"
                             """\noutput=\"hexa\""""
                             """\noutput=\"binary\""""
                             """\noutput=\"decimal\""""
                             """\noutput=\"octal\"""")
    else:
        raise ValueError("Inputs must be of string data type.")


def hex_mul(a, b, output="hexa"):
    """
        Multiplies two hexadecimal numbers without using built-in functions.

        Notes:
        --------------
        You can change output to any other number system such as binary, decimal,
        octal etc...

        Here are some ways to do it:

        **Decimal:** syntax ---> **hex_mul(a, b, output="decimal")**.

        **Binary:** syntax ---> **hex_mul(a, b, output="binary")**.

        **Octal:** syntax ---> **hex_mul(a, b, output="octal")**.

        Examples:
        --------------
        import pynumsys as pns

        print(pns.hex_mul("73", "4A"))

        213E

        print(pns.hex_mul("73", "4A", output="binary"))

        10000100111110

        print(pns.hex_mul("73", "4A", output="octal"))

        20476


        :param a: hexadecimal number 1.
        :param b: hexadecimal number 2.
        :param output: output string.
                By default, it outputs hexadecimal output but if you want to change to binary you
                can simply write **hex_mul(a, b, output="binary")**.
        :returns: Multiplication of two hexadecimal numbers a and b.
    """
    if isinstance(a, str) and isinstance(b, str):
        hex_digits = "0123456789ABCDEF"
        result = "0"

        # Multiply each digit of b with a
        for i in range(len(b) - 1, -1, -1):
            current_result = ""
            carry = 0
            digit2 = hex_digits.index(b[i])

            for j in range(len(a) - 1, -1, -1):
                digit1 = hex_digits.index(a[j])
                product = digit1 * digit2 + carry
                carry = product // 16
                current_result = hex_digits[product % 16] + current_result

            if carry:
                current_result = hex_digits[carry] + current_result

            # Add trailing zeros based on the position of the digit in b
            current_result += "0" * (len(b) - 1 - i)
            result = hex_add(result, current_result)

        if output == "hexa":
            return result
        if output == "binary":
            return hex_to_bin(result)
        if output == "decimal":
            return hex_to_dec(result)
        if output == "octal":
            return hex_to_oct(result)
        else:
            raise ValueError("Invalid Option. Please choose from one of these given options:"
                             """\noutput=\"hexa\""""
                             """\noutput=\"binary\""""
                             """\noutput=\"decimal\""""
                             """\noutput=\"octal\"""")
    else:
        raise ValueError("Inputs must be of string data type.")


def hex_div(a, b, output="hexa", quot=False):
    """
        Divides two hexadecimal numbers without using built-in functions.

        Notes:
        --------------
        You can change output to any other number system such as binary, decimal,
        octal etc...

        Here are some ways to do it:

        **Decimal:** syntax ---> **hex_div(a, b, output="decimal")**.

        **Binary:** syntax ---> **hex_div(a, b, output="binary")**.

        **Octal**: syntax ---> **hex_div(a, b, output="octal")**.


        If you want quotient from division it can return it by optional parameter
        **'quot'** which by default is False and the syntax is given below:


        **Syntax: hex_div(a, b, quot="True")**


        Examples:
        --------------
        import pynumsys as pns

        print(pns.hex_div("73", "4A"))

        29

        print(pns.hex_div("73", "4A", output="binary"))

        101001

        print(pns.hex_div("73", "4A", output="octal"))

        51

        Output with quotient:

        print(pns.hex_div("73", "4A", quot="True"))

        (1, 29)

        Output without quotient:

        print(pns.hex_sub("73", "4A"))

        29

        :param a: hexadecimal number 1.
        :param b: hexadecimal number 2.
        :param output: output string.
                By default, it outputs hexadecimal output but if you want to change to binary you
                can simply write **hex_div(a, b, output="binary")**.
        :param quot: quotient.
                (Optional) Boolean Value which defaults false. If you want quotient you can make it True
                and it will give quotient and remainder in a tuple.
        :returns: Division of two hexadecimal numbers a and b with quotient(optional).
    """
    if isinstance(a, str) and isinstance(b, str):
        hex_digits = "0123456789ABCDEF"

        def hex_compare(a, b):
            """Compares two hexadecimal numbers as strings."""
            if len(a) > len(b):
                return 1
            elif len(a) < len(b):
                return -1
            else:
                return (a > b) - (a < b)

        quotient = ""
        remainder = ""

        for digit in a:
            remainder += digit
            count = 0

            while hex_compare(remainder, b) >= 0:
                remainder = hex_sub(remainder, b)
                count += 1

            quotient += hex_digits[count]
        if quot:
            return quotient.lstrip("0") or "0", remainder.lstrip("0") or "0"
        else:
            if output == "hexa":
                return remainder.lstrip("0") or "0"
            if output == "binary":
                return hex_to_bin(remainder.lstrip("0") or "0")
            if output == "decimal":
                return hex_to_dec(remainder.lstrip("0") or "0")
            if output == "octal":
                return hex_to_oct(remainder.lstrip("0") or "0")
            else:
                raise ValueError("Invalid Option. Please choose from one of these given options:"
                                 """\noutput=\"hexa\""""
                                 """\noutput=\"binary\""""
                                 """\noutput=\"decimal\""""
                                 """\noutput=\"octal\"""")
    else:
        raise ValueError("Inputs must be of string data type.")


if __name__ == "__main__":
    print(hex_add("73", "4A"))
    print(hex_sub("73", "4A"))
    print(hex_mul("73", "4A"))
    print(hex_div("73", "4A"))

    # Example usage
    # hex_str = "73"
    # deci_str = hex_to_dec(hex_str)
    # print(deci_str)
    # print(hex_to_bin(hex_str))
    # print(hex_to_oct(hex_str))
