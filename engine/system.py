class System():
    """A class representing a system of atoms.
    
    Attributes:
        atoms (list): A list of atoms in the system. Initialized to an empty list if no atoms are provided.
    
    Methods:
        add_atom(atom): Adds an atom to the system.
    """
    def __init__(self, atoms = None):
        
        self.atoms = atoms if atoms is not None else []

    def add_atom(self, atom):
        self.atoms.append(atom)