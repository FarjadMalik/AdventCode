import numpy as np

from scipy.ndimage import convolve

# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def part_1(grid: np.ndarray, kernel: np.ndarray) -> int:
    """
    Args:

    Returns:
    """
    neighbours = convolve(grid, kernel, mode="constant")
    # logger.debug(f"Neighbours - {neighbours}")
    # logger.debug(f"Total Logical op - {np.logical_and(grid, neighbours < 4)}")
    # logger.debug(f"Total - {np.logical_and(grid, neighbours < 4).sum()}")

    return np.logical_and(grid, neighbours < 4).sum()


def part_2(grid: np.ndarray, kernel: np.ndarray) -> int:
    """
    Args:

    Returns: 
    """
    rolls = grid.copy()

    while True:
        # logger.debug(f"rolls - {rolls}, grid sum - {grid.sum()}, rolls sum - {rolls.sum()}")
        to_remove = np.logical_and(rolls, convolve(rolls, kernel, mode="constant") < 4)
        # logger.debug(f"to_remove - {to_remove}")
        if not to_remove.any():
            return grid.sum() - rolls.sum()
        rolls -= to_remove

def main(fp_input: str) -> None:
    """
    
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")

    grid = []
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        grid.extend([line.strip() for line in f if line.strip()])
    
    logger.debug(f"Grid with rolls of paper len - {len(grid)}")

    # Convert to np array
    grid = np.array([[int(col=='@') for col in row] for row in grid], dtype=int)
    # logger.debug(f"Grid with rolls of paper - {grid}")

    # Define kernel to be used, all 8 adjacent neighbours
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    
    result = part_1(grid, kernel)
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")
    
    result = part_2(grid, kernel)
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d4/test.txt")
    main(fp_input="src/2026/d4/input.txt")
