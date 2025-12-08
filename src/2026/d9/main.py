# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def part_1() -> int:
    """
    """
    ...

def part_2() -> int:
    """
    """
    ...

def main(fp_input: str) -> None:
    """
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")
    
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        content = f.read()
    logger.debug(f"File content - \n{content}")
    # data = [row for row in content.splitlines()]  

    result = part_1()
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")

    result = part_2()
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")


if __name__ == "__main__":
    main(fp_input="src/2026/d9/test.txt")
    # main(fp_input="src/2026/d9/input.txt")
