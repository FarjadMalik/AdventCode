import numpy as np

# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def part_1(content: str) -> int:
    """
    """
    # Read values and last line separately, last line contains operators
    *lines, _last = content.splitlines()

    # Convert values into an np array
    data = np.array([list(map(int, l.split())) for l in lines])
    # Get a list of ops by splitting last line
    ops = _last.split()

    # Check if the columns in the data match our given operations
    if data.shape[1] != len(ops):
        ValueError(f"Length of the values and corresponding operations dont match - {data.T, ops}")

    # for each pair of col (from Transposed matrix) and given operation perform np function and return their sum
    return sum(np.prod(col) if op == '*' else np.sum(col)
               for col, op in zip(data.T, ops)
               )

def part_2(content: str) -> int:
    """
    """
    # Split content line by line and make sure to also read spaces to cater for positional units
    data = np.array([list(row) for row in content.splitlines()])

    # Define variables, total to store cummalative sum value after each operation, 
    # and values array to store integers before an operation is reached
    total = 0
    values = []
    
    # Tranpose to a column matrix so that we have each position correctly aligned
    # Iterate over transpose data and calculate when an op is read
    for col in data.T[::-1]:
        
        try:
            # append int values from the col (except last row which is ops) to our list
            values.append(int("".join(col[:-1])))

            # check if this col contains an operation, if so then add apply the operation and add to total
            if np.isin(col[-1], ('*', '+')):
                total += int(np.prod(values) if col[-1] == '*' else np.sum(values))

        except:
            # in case the whole col is empty and values cannot be append then
            # it means its an empty col and hence we clear and restart
            values.clear()

    return total

def main(fp_input: str) -> None:
    """
    
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")

    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        content = f.read()

    # Solve for part 1
    result = part_1(content)
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")

    # Solve for part 2
    result = part_2(content)
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d6/test.txt")
    main(fp_input="src/2026/d6/input.txt")
