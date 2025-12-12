import numpy as np

# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def part_1(areas: np.ndarray, tree_fits: list) -> int:
    """
    """
    # for region_area, fit in tree_fits:
    #     logger.debug(f"region_area, fit - {region_area, fit}")
    #     logger.debug(f"areas @ fit - {areas @ fit}")
    return sum(region_area >= areas @ fit for region_area, fit in tree_fits)

def main(fp_input: str) -> None:
    """
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")
    
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        content = f.read()

    *packages, trees = content.split("\n\n")
    areas = np.array([package.count("#") for package in packages])

    tree_regionfits = []
    for tree in trees.splitlines():
        region, fits = tree.split(": ")
        h, w = region.split('x')
        region_area = int(h)*int(w)
        fits = np.array(fits.split(), dtype=int)
        tree_regionfits.append((region_area, fits))

    # logger.debug(f"tree_regionfits - {tree_regionfits}")

    result = part_1(areas, tree_regionfits)
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d12/test.txt")
    main(fp_input="src/2026/d12/input.txt")
