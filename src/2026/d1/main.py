# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def part_1(rotations: list[int], position: int=50, dial_max: int=100) -> int:
    """
    Args:
        rotations: list of rotations to be run on the dial
        position: current position of the dial
        dial_max: max clicks on the dial, by default 100 (0-99)

    Returns: returns final count of zeros found after each rotation
    """
    zeros = 0

    # Go over the list and apply rotations sequantially and count if the zero marker is hit
    for rot in rotations:
        position += rot
        # if a 0 is hit then add
        zeros += position % 100 == 0

    return zeros

def part_2(rotations: list[int], position: int=50, dial_max: int=100) -> int:
    """
    Args:
        rotations: list of rotations to be run on the dial
        position: current position of the dial, by default 50
        dial_max: max clicks on the dial, by default 100 (0-99)

    Returns: returns final count of zeros found at each rotation plus the crossings in between
    """
    zeros = 0

    # Go over the list and apply rotations sequantially and count if the zero marker is hit + also add crossings
    for rot in rotations:
        at_zero = position == 0
        crossings, position = divmod(position + rot, 100)
        zeros += abs(crossings)
        if rot < 0:
            zeros += (position == 0) - at_zero

    return zeros

def main(fp_input: str, position: int = 50, dial_max: int=100) -> None:
    """
    
    Args:
        fp_input: input file path containing the dials (line by line)
        position: initial position of the dial when we start, by default 50
        dial_max: max clicks on the dial, by default 100 (0-99)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")

    # Read input file and load rotations info as a list
    rotations = []
    with open(fp_input, "r", encoding="utf-8") as f:
        rotations.extend([line.strip() for line in f if line.strip()])
    
    logger.debug(f"Rotations - {len(rotations)}")
    
    # Convert rotations into a list of summable values i.e. replace R with + and L with - signs
    rotations = [int(r[1:]) * (1 if r[0] == "R" else -1) for r in rotations]

    # Solve for each part
    zero_clicks = part_1(rotations, position, dial_max)
    logger.info(f"Open the door for {fp_input} using (part 1): {zero_clicks}")

    zero_clicks = part_2(rotations, position, dial_max)
    logger.info(f"Open the door for {fp_input} using (part 2): {zero_clicks}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d1/test.txt")
    main(fp_input="src/2026/d1/input.txt")
