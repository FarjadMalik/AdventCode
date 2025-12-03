# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def is_valid(value: int) -> bool:
    """
    Check if an int is valid. 
    Valid int are made only of some sequence of digits repeated twice. 
    So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs
    
    """
    as_str = str(value)
    mid = len(as_str) // 2
    return as_str[:mid] != as_str[mid:]

def invalids(start: int, end: int):
    """
    Iterative function to calculate all the invalids between a start-end range. An int is invalid 
    if it is made only of some sequence of digits repeated at least twice. 
    So, 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times), 
    and 1111111 (1 seven times) are all invalid IDs.
    """
    as_str = str(start)
    if len(as_str) != len(str(end)):
        yield from invalids(start, int("9" * len(as_str)))
        yield from invalids(int("1" + "0" * len(as_str)), end)
        return

    seen = set()
    for i in range(1, len(as_str) // 2 + 1):
        if len(as_str) % i:
            continue
        initial = int(as_str[:i])
        while True:
            possible = int(str(initial) * (len(as_str) // i))
            if possible > end:
                break
            initial += 1
            if possible not in seen and possible >= start:
                seen.add(possible)
                yield possible
                
def part_1(ranges: list[tuple[int, int]]) -> int:
    """
    Args:

    Returns:
    """
    total = 0
    for start, end in ranges:
        for value in range(start, end + 1):
            if not is_valid(value):
                total += value
    
    return total

def part_2(ranges: list[tuple[int, int]]) -> int:
    """
    Args:

    Returns: 
    """
    return sum(sum(invalids(start, end)) for start, end in ranges)


def main(fp_input: str) -> None:
    """
    
    Args:
        fp_input: input file path
    """
    logger.info(f"Input file path: {fp_input}")

    ranges = []
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        content = f.read().replace("\n", "")
    # for each part in the content create a start-end tuple
    for part in content.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            ranges.append((start, end))
    
    # logger.debug(f"Ranges parsed: {ranges}")

    result = part_1(ranges)
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")
    
    result = part_2(ranges)
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")

 
if __name__ == "__main__":
    # main(fp_input="src/2026/d2/test.txt")
    main(fp_input="src/2026/d2/input.txt")
