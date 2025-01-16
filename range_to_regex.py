def range_to_regex(lo: str, hi: str) -> str:
    """
    For a given range of integers bound by lo and hi, returns a regex pattern matching all integers
    between lo and hi in decimal notation. Note that bounds are inclusive.
    Assumes that for range [lo-hi], lo <= hi always holds true.

    (Also why did I do this to myself)

    Quick, top-level breakdown of the algorithm:
        1. Cut of any common prefix between lo and hi. (If len(lo) < len(hi), this obviously is the empty string)
        2. Split the resulting new range in 3 parts: [lo-10^n], [10^n-10^m], [10^m-hi] (in code: bottom, mid, top)
            2.1 if len(lo) == len(hi), n = m, and thus the ranges are [lo-a*10^n], [a*10^n-b*10^n], [b*10^n-hi]
                top and bottom can then still be constructed by using match_up/down one digit to the right
        3. Construct the regex pattern for each part
            3.1 for bottom and top, this is done by recursively: for each digit k <= n, match all digits in range
                [lo[k]-9] or [0-hi[k]] respectively;
                for the remaining n-k digits, accept any digit (save special cases)
            3.2 for mid, calculate the range that hasn't been covered by bottom and top and match all numbers in that range

    Note:
        Algorithm is quadratic in both runtime and the expression it produces. That shouldn't be a problem tho since
        in this project it will only be used for numbers of a maximum length of 3.
    Note:
        I brute-force tested the construction for all possible ranges within [0, 255] and it passed all tests.


    """
    if int(lo) == int(hi):
        return lo

    if len(lo) == len(hi):
        first_diff = next((i for i, (l, h) in enumerate(zip(lo, hi)) if l != h))
        pattern = "".join([l for l in lo[:first_diff]])
        lo, hi = lo[first_diff:], hi[first_diff:]
        if len(hi) == 1:
            return f"{pattern}[{lo}-{hi}]"

        top = match_down(hi[1:], prefix=hi[0])
        bottom = match_up(lo[1:], prefix=lo[0])

        mid_filler = (len(lo) - 1) * "[0-9]"
        match int(hi[0]) - int(lo[0]):
            case 1:
                mid = "|"
            case 2:
                mid = "|" + str(int(lo[0]) + 1) + mid_filler + "|"
            case _:
                mid = "|" + f"[{int(lo[0]) + 1}-{int(hi[0]) - 1}]" + mid_filler + "|"

        pattern = pattern + "(" + bottom + mid + top + ")"
    else:
        top = match_down(hi, to_zero=False)
        bottom = match_up(lo)

        lo_leadzero = lo.zfill(len(hi))
        first_nonzero = next(
            (i for i, l in enumerate(lo_leadzero) if l != "0"), len(lo_leadzero) - 1
        )

        mid = (
            "|"
            + "[0-9]?" * (first_nonzero - 2)
            + "[1-9]"
            + "[0-9]" * (len(lo_leadzero) - first_nonzero)
            + "|"
            if len(hi) - len(lo) > 1
            else "|"
        )
        pattern = bottom + mid + top

    return pattern


def match_down(hi: str, prefix="", to_zero=True) -> str:
    """
    Constructs an expression to match all numbers between 0{n} and hi (assuming hi has length n).
    If `to_zero` is set to falses, it will match all numbers between hi and the next lowest power of 10, inclusive.
    """
    if not to_zero:
        if hi[0] == "1":
            pre = hi[0]
        else:
            pre = f"[1-{int(hi[0]) - 1}]" if hi[0] > "2" else "1"
            pre += "[0-9]" * (len(hi) - 1) + f"|{hi[0]}"
        return f"{prefix}{pre}({match_down(hi[1:], prefix='', to_zero=True)})"

    if len(hi) == 1:
        return f"{prefix}[0-{hi}]" if hi != "0" else prefix + hi
    if hi[0] == "0":
        return match_down(hi[1:], prefix=prefix + hi[0])
    range_k = f"[0-{int(hi[0]) - 1}]" if hi[0] != "1" else "0"
    range_k += "".join(["[0-9]" for _ in hi[1:]])

    return f"{prefix}{range_k}|{match_down(hi[1:], prefix=prefix + hi[0])}"


def match_up(lo: str, prefix="") -> str:
    """Constructs an expression to match all numbers from lo to the next highest power of 10."""
    if len(lo) == 1:
        return f"{prefix}[{lo}-9]"
    if lo[0] == "9":
        return match_up(lo[1:], prefix=prefix + lo[0])

    range_k = f"[{int(lo[0]) + 1}-9]"
    range_k += "".join(["[0-9]" for _ in lo[1:]])
    return f"{prefix}{range_k}|{match_up(lo[1:], prefix=prefix + lo[0])}"


if __name__ == "__main__":
    print("^(" + range_to_regex("91", "100") + ")$")
