# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def part_1(ranges: list, ingredients: list) -> int:
    """
    Args:

    Returns:
    """
    # Check if each available ingredient is within any of the ingredient ID ranges (inclusive)
    fresh_ingredients = [id for id in ingredients 
                 if any(id >= start and id <= end for start, end in ranges)]

    return len(fresh_ingredients)

def merge_overlapping_ranges(ranges: list) -> list:
    """
    Ranges in the form of tuples which can be overlapping. Compresses to non-overlapping ranges. 
    
    :param ranges: Description
    :type ranges: list
    :return: Description
    :rtype: list[Any]
    """
    # Sort ranges by start; if same start, sort by end
    ranges.sort() 
    # logger.debug(f"Sorted ranges - {ranges}")

    # Create a new list for non-overlapping (no) ranges and append first sorted range
    no_ranges = []
    no_ranges.append(ranges[0])
    
    # First range already added so process the rest of the ranges
    for range in ranges[1:]:
        # logger.debug(f"Iterating range - {range}")
        last_start, last_end = no_ranges[-1]
        # logger.debug(f"Iterating last_start, last_end - {last_start, last_end}")
        # Check for overlapping interval
        if last_start <= range[0] <= last_end:
            new_end = max(last_end, range[1])
            # logger.debug(f"Adjusting range - {(last_start, new_end)}")
            no_ranges[-1] = (last_start, new_end)
        else:
            no_ranges.append(range)
      
    # logger.debug(f"Non-overlapping ranges - {no_ranges}")
    return no_ranges

def part_2(ranges: list) -> int:
    """
    Args:

    Returns: 
    """
    # merge ranges so that overlapping ranges are catered for
    ranges = merge_overlapping_ranges(ranges)

    # return sum of merged ranges (+1 to cater for inclusivity)
    return sum(end-start+1 for start, end in ranges)

def parse_food_db(food_db: str) -> tuple[list[tuple[int, ...]], list[int]]:
    """
    """
    valid_ranges = []
    ingredients = []

    valid_ranges, ingredients = food_db.split("\n\n")
    valid_ranges = [tuple(map(int, line.split("-"))) for line in valid_ranges.splitlines()]
    ingredients = list(map(int, ingredients.splitlines()))

    # valid_ranges = []
    # food_ids = []
    # for item in food_db:
    #     item = item.strip()
    #     logger.debug(f"item - {item}")
    #     if not item:
    #         continue

    #     if '-' in item:
    #         logger.debug(f"start, end - {map(int, item.split("-"))}")
    #         start, end = map(int, item.split("-"))
    #         valid_ranges.append((start, end))
        
    #     else:
    #         try:
    #             food_ids.append(int(item))
    #         except ValueError:
    #             raise ValueError(f"Invalid integer line: {item}")

    return valid_ranges, ingredients

def main(fp_input: str) -> None:
    """
    
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")

    content = ""
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        content = f.read()
    
    logger.debug(f"Food content - {content}")

    valid_ranges, ingredients = parse_food_db(content)
    
    logger.debug(f"valid_ranges - {valid_ranges}")
    logger.debug(f"ingredients - {ingredients}")
    
    
    result = part_1(valid_ranges, ingredients)
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")
    
    result = part_2(valid_ranges)
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d5/test.txt")
    main(fp_input="src/2026/d5/input.txt")
