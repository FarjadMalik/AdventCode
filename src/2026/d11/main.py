import networkx as nx

from functools import cache

# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)


def parse_raw(data: str):
    """
    Docstring for parse_raw
    
    :param data: Raw data from the input file
    :type data: str
    """
    lines = [line.partition(": ") for line in data.splitlines()]
    # logger.debug(f"lines - {lines}")
    network = nx.DiGraph({node: neighbors.split() for node, _, neighbors in lines})
    return network

def part_1(network : nx.DiGraph) -> int:
    """
    """
    # logger.debug(f"All simple paths: \n{list(nx.all_simple_paths(network, "you", "out"))}")
    return len(list(nx.all_simple_paths(network, "you", "out")))

def part_2(graph: nx.DiGraph) -> int:
    """ 
    Count unique paths from start_node to "out" using recursion and memoization.
    """

    @cache
    def _count(current: str, seen) -> int:
        """ Inner function used because the graph itself is unhashable. """
        if current == "out":
            return seen == 2
        seen += current in {"fft", "dac"}
        return sum(_count(neighbor, seen) for neighbor in graph[current])
    
    return _count("svr", 0)

def main(fp_input: str) -> None:
    """
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")
    
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        content = f.read()
    device_network = parse_raw(content)
    logger.debug(f"File content - \n{device_network}")


    # result = part_1(device_network)
    # logger.info(f"Solved for {fp_input}, use (part 1): {result}")

    result = part_2(device_network)
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d11/test.txt")
    # main(fp_input="src/2026/d11/test_p2.txt")
    main(fp_input="src/2026/d11/input.txt")
