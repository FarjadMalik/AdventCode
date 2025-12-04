# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def part_1(banks: list[str]) -> int:
    """
    Find sum of the maximum joltage (2 digit) from each battery bank.
    Args:

    Returns:
    """
    total = 0

    for b in banks:
        max = 0
        if len(b) < 2:
            continue
        for l in range(len(b)-1):
            # left = b[l]
            for r in range(l+1, len(b)):
                # right = b[r]
                joltage = int(f"{b[l]}{b[r]}")
                if joltage > max:
                    # logger.debug(f"Bank - {b}, Left - {b[l]}, right - {b[r]}, jolt - {joltage}")
                    max = joltage
        total += max
    return total

def max_subseq_k(bank: str, d: int) -> int:
    """
    Return the lexicographically largest subsequence of a bank of length exactly d(digits), preserving order of digits.
    """
    joltage = []
    to_remove = len(bank) - d
    for ch in bank:

        # While we can still remove digits, and stack top is less than current digit,
        # pop it to make number larger
        while to_remove > 0 and joltage and joltage[-1] < ch:
            joltage.pop()
            to_remove -= 1
        # Otherwise just append to our list
        joltage.append(ch)

    # If we've not removed enough (e.g. digits were non-increasing),
    # truncate from the end
    return int(''.join(joltage[:d]))

def part_2(banks: list[str], nob: int=12) -> int:
    """
    Find sum of the maximum joltage (by default 12 batteries) from each battery bank.
    Args:
        banks: a list of battery bank
        nob: number of digits (batteries from a bank) to be used for joltage

    Returns:
    """
    total = 0

    for b in  banks:
        if len(b) < nob:
            continue
        max = max_subseq_k(b, nob)
        total += max

    return total

def main(fp_input: str) -> None:
    """
    
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")

    banks = []
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        banks.extend([line.strip() for line in f if line.strip()])
    
    logger.debug(f"Battery Banks len- {len(banks)}")
    # logger.debug(f"Battery Banks - {banks}")

    result = part_1(banks)
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")

    result = part_2(banks, nob=2)
    logger.info(f"Solved for {fp_input}, use (part 2 for p1): {result}")

    result = part_2(banks)
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")


if __name__ == "__main__":
    main(fp_input="src/2026/d3/test.txt")
    main(fp_input="src/2026/d3/input.txt")
