# https://en.wikipedia.org/wiki/Minifloat
# https://gist.github.com/aaronfranke/0d1217e521c4ec784d39e92b5f039115

# IEEE-style floating-point format table generator (Python)
# Python version: https://gist.github.com/aaronfranke/0d1217e521c4ec784d39e92b5f039115
# GDScript version: https://gist.github.com/aaronfranke/8b2c39bfbe48068c574e4daf2710c875
import copy

# SEMB values can describe any IEEE-like binary floating-point format.
sign_bit: bool = True
exponent_bits: int = 4
mantissa_bits: int = 3
## Can be set to an integer. If null, the bias will be automatically determined
## to match IEEE formats, symmetric around 1. Specialized use cases may benefit
## from overriding this, but this should usually be kept as automatic.
bias = None


def main() -> None:
    assert exponent_bits > 0, "Exponent bit amount cannot be zero or negative. A float must have at least 1 exponent bit, or else it's just an integer, loses Inf/NaN, etc."
    assert mantissa_bits >= 0, "Mantissa bit amount cannot be negative. However, mantissa is allowed to have zero bits."
    global bias
    if bias == None:
        bias = int(pow(2, exponent_bits - 1)) - 1
    # Generate the mantissa row without an exponent bias.
    mantissa_base = _generate_mantissa_base(mantissa_bits)
    # Generate the cells of the table.
    table_cell_rows: list[list] = _generate_table_data_cells(mantissa_base)
    # Format the cells as a WikiText table.
    wikitext: str = _format_pretty_table_wikitext(table_cell_rows)
    print(wikitext)


def _format_pretty_table_wikitext(table_cell_rows: list[list]) -> str:
    output_text: str = '{| class="wikitable" style="text-align:right; font-size:small"\n!\n! '
    # Generate the header row.
    first_row: list = table_cell_rows[0]
    for i in range(len(first_row)):
        column_width = len(str(first_row[i]))
        if i != 0:
            output_text += " || "
        output_text += ("… " + _int_to_bits(i, mantissa_bits)).rjust(column_width, " ")
    # Generate the main rows.
    table_row_count: int = len(table_cell_rows)
    for i in range(table_row_count):
        output_text += "\n|-\n! "
        if sign_bit:
            output_text += "0 " if i < table_row_count // 2 else "1 "
        output_text += _int_to_bits(i, exponent_bits) + " …\n"
        row: list = table_cell_rows[i]
        for j in range(len(row)):
            if j == 0:
                output_text += "| "
            else:
                output_text += " || "
            output_text += row[j]
    output_text += "\n|}"
    return output_text


def _generate_table_data_cells(mantissa_base: list[float]) -> list[list]:
    rows: list[list] = []
    column_widths: list[int] = []
    exponent_range: int = int(pow(2, exponent_bits)) - 1
    # Generate the main rows.
    for i in range(exponent_range):
        row: list = []
        rows.append(row)
        exponent: int = i - bias
        if i == 0:
            exponent += 1
        multiplier = pow(2, exponent)
        for j in range(len(mantissa_base)):
            mantissa_number: float = mantissa_base[j]
            if i == 0:
                column_widths.append(_starting_column_width())
                mantissa_number -= 1.0
            stringified_number = str(mantissa_number * multiplier)
            if len(stringified_number) > column_widths[j]:
                column_widths[j] = len(stringified_number)
                if sign_bit:
                    column_widths[j] += 1
            row.append(stringified_number)
    # Add the infinity/NaN row.
    inf_nan_row: list = ["Inf"]
    for i in range(len(mantissa_base) - 1):
        inf_nan_row.append("NaN")
    rows.append(inf_nan_row)
    # If there is a sign bit, append a duplicate of every row, with a minus sign.
    if sign_bit:
        for row in copy.deepcopy(rows):
            for cell_index in range(len(row)):
                row[cell_index] = "−" + row[cell_index]
            rows.append(row)
    # Pad each column's entries to be the same length.
    for i in range(len(rows)):
        row = rows[i]
        for j in range(len(row)):
            column_width: int = column_widths[j]
            row[j] = str(row[j]).rjust(column_width, " ")
    return rows


def _starting_column_width() -> int:
    ret: int = 2 + mantissa_bits
    if sign_bit:
        if ret < 4:
            return 4
    else:
        if ret < 3:
            return 3
    return ret


def _generate_mantissa_base(bits_amount: int) -> list[float]:
    mantissa_base: list[float] = []
    mantissa_step: float = pow(2, -bits_amount)
    mantissa_value: float = 1.0
    while True:
        mantissa_base.append(mantissa_value)
        mantissa_value += mantissa_step
        if mantissa_value >= 2.0:
            break
    return mantissa_base


def _int_to_bits(number: int, bits_amount: int) -> str:
    ret: str = ""
    digit_value: int = 1
    for i in range(bits_amount):
        if number & digit_value == 0:
            ret = "0" + ret
        else:
            ret = "1" + ret
        digit_value *= 2
    return ret


if __name__ == "__main__":
    main()