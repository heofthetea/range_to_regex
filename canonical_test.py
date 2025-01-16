from range_to_regex import range_to_regex
import re
import argparse


def main(max, silent):
    for lo in range(max):
        print(f"{lo} out of {max:_}")
        try:
            for hi in range(lo, max):
                try:
                    pattern = (
                        "^(" + range_to_regex(str(lo), str(hi)) + ")$"
                    )  # pattern is generated with bounds inclusive
                except Exception as e:
                    print(f"[{lo}, {hi}] -> {e}")
                    raise e
                pattern = re.compile(pattern)
                if not silent:
                    print(f"[{lo}, {hi}] -> {pattern.pattern}: ", end="\t\t")
                try:
                    for i in range(0, lo):
                        try:
                            assert not pattern.match(str(i))
                        except AssertionError as e:
                            raise AssertionError(f"should not match")
                    for i in range(lo, hi + 1):
                        try:
                            assert pattern.match(str(i))
                        except AssertionError as e:
                            raise AssertionError(f"should match")
                    for i in range(hi + 1, max):
                        try:
                            assert not pattern.match(str(i))
                        except AssertionError as e:
                            raise AssertionError(f"should not match")
                except AssertionError as e:
                    print("\n------failed------")
                    print(e)
                    print("pattern:", pattern.pattern)
                    print(f"range: [{lo}-{hi}]")
                    print("i:", i)
                    raise e
                if not silent:
                    print(f"{max} tests passed")
        except Exception as e:
            exit(e)

    print("\n" * 4)
    print(f"ALL TESTS PASSED! THE CONVERTER WORKS IN THE RANGE [0, {max})!")
    print(f"total tests run:{max**3:_}")


"""
Can we just take a moment to appreciate the absurdity of this construction
We have doubly nested loops to construct every possible range, then we run a regex construction
that behaves quadratically relative to len(hi)
In total this abomination has a time complexity of fucking O(n^4), fucking FOUR, and it still runs in like 10 seconds
"""

if __name__ == "__main__":
    description = """
Script to canonically test range_to_regex for every possible range in the range [0, max). 
For every possible range, it tests all numbers in [0, max) and asserts whether the pattern behaves correctly, 
i.e. either matches or doesn't match the number.

"""
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--max", type=int, default=256, help="Maximum range value")
    parser.add_argument("--silent", action="store_true", help="Silent mode")

    args = parser.parse_args()

    max = args.max
    silent = args.silent

    main(max, silent)
