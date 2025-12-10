from itertools import combinations
from shapely import Polygon

# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def area(p1, p2):
    x1, y1 = map(int, p1.split(","))
    x2, y2 = map(int, p2.split(","))

    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

def part_1(data: list[str]) -> int:
    """
    """
    return max(area(a, b) for a, b in combinations(data, 2))

def rect(p1, p2):
    x1, y1 = map(int, p1.split(","))
    x2, y2 = map(int, p2.split(","))
    return Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])

def part_2(data: list[str]) -> int:
    """
    """
    base_polygon = Polygon([list(map(int, p.split(","))) for p in data])
    return max(
        area(a, b) for a, b in combinations(data, 2) if base_polygon.covers(rect(a, b))
    )

def main(fp_input: str) -> None:
    """
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")
    
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        content = f.read()
    redtiles = [row for row in content.splitlines()]  
    # logger.debug(f"File redtiles - \n{redtiles}")

    result = part_1(redtiles)
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")

    result = part_2(redtiles)
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d9/test.txt")
    main(fp_input="src/2026/d9/input.txt")
