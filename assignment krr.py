from typing import Tuple, Set, Dict

# Knowledge Base Class for Propositional Logic (KB)
class PropositionalKB:
    def __init__(self):
        # Knowledge Base: Dictionary to store propositional symbols (variables)
        self.kb = {
            'Wind': set(),         # Set of positions with wind
            'Trap': set(),         # Set of positions with traps
            'Treasure': set(),     # Set of positions with treasures
            'Safe': set(),         # Set of safe positions
            'RobotAt': None,       # Robot's current position (x, y)
        }
    
    def get_adjacent_cells(self, x: int, y: int) -> Set[Tuple[int, int]]:
        """
        Given a position (x, y), return the set of valid adjacent cells within the 4x4 grid.
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        adj = set()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= 4 and 1 <= ny <= 4:
                adj.add((nx, ny))
        return adj
    
    def update_percepts(self, pos: Tuple[int, int], percepts: Dict[str, bool]):
        """
        Updates the knowledge base based on the robot's percepts at position (x, y).
        """
        x, y = pos
        self.kb['RobotAt'] = (x, y)
        
        # Update the knowledge base based on wind and glitter percepts
        if percepts.get('Wind'):
            self.kb['Wind'].add((x, y))
            # Mark adjacent cells as potential traps
            for ax, ay in self.get_adjacent_cells(x, y):
                self.kb['Trap'].add((ax, ay))
        
        if percepts.get('Glitter'):
            self.kb['Glitter'] = True
            self.kb['Treasure'].add((x, y))  # Mark this cell as a treasure location
        
        # Mark safe cells: If no wind, mark adjacent cells as safe
        if not percepts.get('Wind'):
            for ax, ay in self.get_adjacent_cells(x, y):
                self.kb['Safe'].add((ax, ay))

    def mark_safe_cells(self):
        """
        Updates the KB by marking all cells that are not adjacent to any traps as safe.
        """
        for x in range(1, 5):
            for y in range(1, 5):
                if (x, y) not in self.kb['Trap']:
                    self.kb['Safe'].add((x, y))

    def is_safe(self, x: int, y: int) -> bool:
        """
        Checks if a given cell (x, y) is safe.
        """
        return (x, y) in self.kb['Safe']
    
    def is_trap(self, x: int, y: int) -> bool:
        """
        Checks if a given cell (x, y) contains a trap.
        """
        return (x, y) in self.kb['Trap']
    
    def is_treasure(self, x: int, y: int) -> bool:
        """
        Checks if a given cell (x, y) contains treasure.
        """
        return (x, y) in self.kb['Treasure']
    
    def query(self, qtype: str, x: int, y: int):
        """
        Answers queries such as 'trap', 'safe', or 'treasure' for a given cell.
        """
        if qtype == "trap":
            return self.is_trap(x, y)
        elif qtype == "safe":
            return self.is_safe(x, y)
        elif qtype == "treasure":
            return self.is_treasure(x, y)
        else:
            return None
    
    def print_kb(self):
        """
        Print the current knowledge base for visualization.
        """
        print("Knowledge Base:")
        print("Wind Locations:", self.kb['Wind'])
        print("Trap Locations:", self.kb['Trap'])
        print("Treasure Locations:", self.kb['Treasure'])
        print("Safe Locations:", self.kb['Safe'])
        print("Robot Position:", self.kb['RobotAt'])
        print("")


# Example of Usage:
kb = PropositionalKB()

# Step 1: Robot starts at (1, 1) with no wind detected
kb.update_percepts((1, 1), {'Wind': False, 'Glitter': False})
kb.mark_safe_cells()

# Step 2: Robot moves to (1, 2), detects wind
kb.update_percepts((1, 2), {'Wind': True, 'Glitter': False})
kb.mark_safe_cells()

# Step 3: Robot moves to (2, 2), detects no wind or glitter
kb.update_percepts((2, 2), {'Wind': False, 'Glitter': False})
kb.mark_safe_cells()

# Step 4: Robot moves to (2, 3), detects glitter (treasure found)
kb.update_percepts((2, 3), {'Wind': False, 'Glitter': True})
kb.mark_safe_cells()

# Querying the Knowledge Base
kb.print_kb()

# Answer queries about the grid
print("Is (1, 2) a trap?", kb.query("trap", 1, 2))         # Expected False, no trap detected
print("Is (1, 1) safe?", kb.query("safe", 1, 1))           # Expected True, no wind or trap
print("Is (2, 3) treasure?", kb.query("treasure", 2, 3))   # Expected True, treasure detected at (2,3)
print("Is (1, 3) a trap?", kb.query("trap", 1, 3))         # Expected True, marked as trap due to wind at (1,2)
