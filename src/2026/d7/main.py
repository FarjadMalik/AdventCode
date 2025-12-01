# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def part_1() -> None:
    """
    Args:

    Returns:
    """
    ...

def part_2() -> None:
    """
    Args:

    Returns: 
    """
    ...

def main(fp_input: str, position: int = 50, dial_max: int=100) -> None:
    """
    
    Args:
        fp_input: input file path containing the dials (line by line)
        position: initial position of the dial when we start, by default 50
        dial_max: max clicks on the dial, by default 100 (0-99)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")

    logger.info(f"Solved for {fp_input}, use (part 2): {0}")


if __name__ == "__main__":
    main(fp_input="src/2026/d7/input.txt")
