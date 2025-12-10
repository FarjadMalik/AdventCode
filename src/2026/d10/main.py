import numpy as np
import itertools

from dataclasses import dataclass
from scipy.optimize import linprog
from scipy.optimize import Bounds, LinearConstraint, milp

# Internal imports
from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class Machine:
    """ 
    Represents a factory machine based on the schematic input 
    """

    # We need this because the leading zero bits are lost when converting to int
    # So we need to know how many bits we started with
    num_lights: int 
    lights: int # E.g. ".##." -> 0b110 = 6
    buttons: list[list[int]]
    joltages: list[int]

    def __post_init__(self):
        """ Create button masks from button indices """
        # E.g. [3] [1,3] ... -> [0b1000, 0b1010, ...] = [8, 10, ...]
        self.button_masks = [sum(1 << i for i in indices) for indices in self.buttons]
    
    def get_presses_lights(self) -> int:
        """
        Determine fewest button presses to reach target state (all lights matching target).
        Start with all lights OFF (0). 
        Target state represents specific configuration of ON lights we need.
        Buttons toggle lights (XOR).
        So we need: (Button_A ^ Button_B ^ ...) == target_state.

        Return k, the fewest number of button presses required.
        """
        num_buttons = len(self.button_masks)
        
        # Try k presses, from 0 to num_buttons
        for k in range(num_buttons + 1): # E.g. [0, 1, 2, 3]
            # We can brute force all combinations of k buttons
            for combo in itertools.combinations(self.button_masks, k):
                # Calculate the result of pressing these k buttons
                current_state = 0
                for mask in combo: # Apply each button in the combo
                    current_state ^= mask
                
                if current_state == self.lights:
                    return k
                    
        raise ValueError("No solution found for machine")
    
    def get_presses_joltages(self) -> int:
        """
        Minimum button presses to match target joltages.
        
        This problem is an optimization problem where we need to find non-negative integers.
        We model this as an Integer Linear Programming (ILP) problem:
        
        Variables: x[0], x[1], ... x[num_buttons-1] = number of times to press each button.
        Objective: Minimize sum(x) (total button presses).
        Constraints: The sum of button effects must exactly equal the target joltage for each light.
        """
        # # Build the Coefficient Matrix 'A' (num_lights rows x num_buttons cols)
        # # Each row 'i' represents a light (equation).
        # # Each col 'j' represents a button (variable).
        # # A[i][j] = 1 means "Button j adds 1 to Light i".
        # A = [[bool(button & (1 << i)) for button in self.button_masks] for i in range(len(self.joltages))]
        # # logger.debug(f"A - {A}")

        # # Build the Target Vector 'b'
        # # These are the RHS values for our equations: "Light i needs 5 jolts".
        # # Equation i: Sum(Buttons affecting Light i) = b[i]
        # b = np.array(self.joltages)
        
        # # Define the Cost Vector 'c'
        # # The solver minimizes the dot product of c and x (c · x).
        # # This means it minimizes: (c[0]*x[0] + c[1]*x[1] + ... + c[n]*x[n])
        # # Since we want to minimize the *total count* of presses, every button costs 1.
        # # If we wanted to minimize just Button 0 presses, c would be [1, 0, 0...].
        # c = np.ones(len(self.buttons))

        # # Use linprog from scipy to solve this efficiently where target is our joltages
        # return int(linprog(c, A_eq=A, b_eq=b, integrality=True).fun)
        num_buttons = len(self.buttons)
        
        # Build the Coefficient Matrix 'A' (num_lights rows x num_buttons cols)
        # Each row 'i' represents a light (equation).
        # Each col 'j' represents a button (variable).
        # A[i][j] = 1 means "Button j adds 1 to Light i".
        A = np.zeros((self.num_lights, num_buttons))
        for j, indices in enumerate(self.buttons):
            for i in indices:
                A[i, j] = 1
                
        # Build the Target Vector 'b'
        # These are the RHS values for our equations: "Light i needs 5 jolts".
        # Equation i: Sum(Buttons affecting Light i) = b[i]
        b = np.array(self.joltages)
        
        # Define the Cost Vector 'c'
        # The solver minimizes the dot product of c and x (c · x).
        # This means it minimizes: (c[0]*x[0] + c[1]*x[1] + ... + c[n]*x[n])
        # Since we want to minimize the *total count* of presses, every button costs 1.
        # If we wanted to minimize just Button 0 presses, c would be [1, 0, 0...].
        c = np.ones(num_buttons)
        
        # Define Linear Constraints
        # A @ x == b  (The button effects sum to exactly the target)
        constraints = LinearConstraint(A, b, b)
        
        # Define Integrality Constraint
        # We need whole number button presses. 0.5 presses doesn't exist.
        # 1 = Integer, 0 = Continuous. We set all to 1.
        integrality = np.ones(num_buttons)
        
        # Define Bounds
        # We can't have negative button presses (lb=0).
        # upper bound is infinity.
        bounds = Bounds(lb=0, ub=np.inf)
        
        # Run the Mixed-Integer Linear Programming Solver
        res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)
        
        if not res.success:
            logger.warning(f"MILP failed for joltages {self.joltages}: {res.message}")
            return 0
            
        # Result x is returned as floats, even with integer constraints.
        # Due to floating point precision, 5 might be 4.99999999.
        # Casting directly to int() would floor it to 4 (wrong).
        solution = np.round(res.x).astype(int)
        
        # Verify we have a solution
        # (A @ solution) means Matrix A multipled by Vector solution.
        # This calculates the actual produced joltages for each light.
        if not np.all(A @ solution == b):
             logger.error("MILP solution verification failed")
             return 0
             
        return int(np.sum(solution))
    
    def __str__(self):
        return f"Lights: {bin(self.lights)[2:]}, " \
             + f"Buttons: [{', '.join([bin(b)[2:] for b in self.button_masks])}], " \
             + f"Joltages: {self.joltages}"

def parse_schematic_input(data: list[str]) -> list[Machine]:
    machines = []

    for line in data:
        # Split line to get separate parts of the schema
        lights, *buttons, joltages = line.split()
        
        # Extract Lights and also number of bits
        # We can map index 0 to bit 0, index 1 to bit 1, etc.
        nlights = len(lights[1:-1])
        lights = sum(2**i * (c == "#") for i, c in enumerate(lights[1:-1]))
        # Extract Buttons, e.g. (3) (1,3) (2) ...
        buttons = [list(map(int, button[1:-1].split(','))) for button in buttons]   
        # logger.debug(f"{buttons=}")
        # buttons_mask = [sum(1 << i for i in list(map(int, button[1:-1].split(',')))) for button in buttons]                
        # Extract Joltages, e.g. {3,5,4,7}
        joltages = [int(x) for x in joltages[1:-1].split(',')]
        
        machines.append(Machine(nlights, lights, buttons, joltages))

    return machines

def part_1(machines: list[Machine]) -> int:
    """
    """
    buttons_pressed = 0
    
    for i, machine in enumerate(machines):
        # logger.debug(f"Machine {i}: {machine}")
        presses = machine.get_presses_lights()
        # logger.debug(f"Presses: {presses}")
        buttons_pressed += presses
        
    return buttons_pressed

def part_2(machines: list[Machine]) -> int:
    """
    """
    buttons_pressed = 0
    
    for i, machine in enumerate(machines):
        # logger.debug(f"Machine {i}: {machine}")
        presses = machine.get_presses_joltages()
        # logger.debug(f"Presses: {presses}")
        buttons_pressed += presses
        
    return buttons_pressed

def main(fp_input: str) -> None:
    """
    Args:
        fp_input: input file path containing the dials (line by line)
    """
    logger.info(f"Your password is encrypted in: {fp_input}")
    
    # Read input file content 
    with open(fp_input, "r", encoding="utf-8") as f:
        content = f.read()
    schema = [row for row in content.splitlines()]  
    machines = parse_schematic_input(schema)
    # logger.debug(f"Machines - \n{machines}")

    result = part_1(machines)
    logger.info(f"Solved for {fp_input}, use (part 1): {result}")

    result = part_2(machines)
    logger.info(f"Solved for {fp_input}, use (part 2): {result}")


if __name__ == "__main__":
    # main(fp_input="src/2026/d10/test.txt")
    main(fp_input="src/2026/d10/input.txt")
