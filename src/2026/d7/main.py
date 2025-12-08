from collections import Counter

# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def part_1(start : int, splitters: list[int]) -> int:
    """
    """
    # create a set for beams to be able to keep track of light
    nsplits, beams = 0, {start}
    # for each split process the beam
    for splitter in splitters:
        # if beam is at split value then split and add -1 and +1 points as new beams
        if splitter in beams:
            nsplits += 1
            beams.remove(splitter)
            beams.update((splitter - 1, splitter + 1))
    return nsplits

def part_2(start : int, splitters: list[int]) -> int:
    """
    """
    # Create a counter and store the timelines from it, from start and one timeline
    beams = Counter({start: 1})
    # for each splitter
    for splitter in splitters:
        if splitter in beams:
            # remove from counter and get its current value
            count = beams.pop(splitter)
            # add timelines (-1 and +1) by adding the previous timeline value
            beams[splitter - 1] += count
            beams[splitter + 1] += count
    # return sum of all timelines from remaining counter    
    return beams.total()

def main(fp_input: str) -> None:
    """
    
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")
    
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        content = f.read()
    # logger.debug(f"File content - \n{content}")

    # get indices for the start and every split charater in our grid
    start = content.index("S")
    # logger.debug(f"File start - {start}")
    splitters = [i for row in content.splitlines() for i, char in enumerate(row) if char == '^']
    # logger.debug(f"File splitters - {splitters}")

    result = part_1(start, splitters)
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")

    result = part_2(start, splitters)
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d7/test.txt")
    main(fp_input="src/2026/d7/input.txt")
