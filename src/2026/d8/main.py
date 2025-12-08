import math

from typing import NamedTuple
from itertools import combinations
from collections import deque
from math import prod

# Internal imports
from src.utils.logger import get_logger
from src.utils.helper import UnionFind

logger = get_logger(__name__)


class Box(NamedTuple):
    """ The location of a Junction Box in 3D space """
    x: int
    y: int
    z: int

def get_distance(box1: Box, box2: Box) -> float:
    """ 
    Returns the Euclidean distance between two boxes. 
    """
    return math.sqrt((box1.x - box2.x)**2 + (box1.y - box2.y)**2 + (box1.z - box2.z)**2)

def part_1(data: list[str], nconnection: int=1000, ncircuits: int=3) -> int:
    """
    Find the n largest circuits from a number of connections and return the product of their sizes.
    """
    boxes = [Box(*map(int, points.split(","))) for points in data]
    connections = list(combinations(boxes, 2))
    connections.sort(key=lambda x: get_distance(x[0], x[1]))

    # logger.debug(f"Boxes - {len(boxes)}")
    # logger.debug(f"connections - {len(connections)}")

    # We can reuse our UnionFind class here as well but lets leave it as is for now
    
    # Build represents connecting n boxes
    connecting_dict = {box: [] for box in boxes}
    for box1, box2 in connections[:nconnection]:
        connecting_dict[box1].append(box2)
        connecting_dict[box2].append(box1)
    
    def find_connected_circuits():
        """
        BFS to find all the circuits. A circuit is defined as connected junction boxes.
        """
        # set to keep track of boxes
        visited = set()
        # list of separate circuits
        circuits = [] 
        
        for box in boxes:
            if box in visited:
                continue
                
            # A circuit set to find connected boxes
            circuit = set() 
            queue = deque([box]) # For efficient queue operations
            visited.add(box)
            
            # Process all connected boxes in this circuit
            while queue:
                current = queue.popleft()
                circuit.add(current)
                
                for neighbor in connecting_dict[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            circuits.append(circuit)

        return circuits
    
    # Find n largest circuits and multiply their len
    circuits = find_connected_circuits()
    assert len(circuits) >= ncircuits, f"Not enough circuits found: {len(circuits)} < {ncircuits}"
    circuits.sort(key=len, reverse=True) # Sort, largest first
    return prod([len(c) for c in circuits[:ncircuits]]) # len(circuits[0]) * len(circuits[1]) * len(circuits[2]))


def part_2(data: list[str]) -> int | None:
    """
    """
    boxes = [Box(*map(int, points.split(","))) for points in data]
    connections = list(combinations(boxes, 2))
    connections.sort(key=lambda x: get_distance(x[0], x[1]))

    circuits = UnionFind(boxes)

    for b1, b2 in connections:
        circuits.merge(b1, b2)
        if len(circuits.components) == 1:
            return b1.x * b2.x
    
    return None

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
    data = [row for row in content.splitlines()]    

    result = part_1(data, nconnection=10)
    logger.debug(f"File result part 1 - {result}")

    result = part_2(data)
    logger.debug(f"File result part 2 - {result}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d8/test.txt")
    main(fp_input="src/2026/d8/input.txt")
