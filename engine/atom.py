import numpy as np # type: ignore


ATOM_DICT = { # type: mass, charge
    "H": (1.0, 1),
    "C": (16.0, 0),
    "O": (18.0, -1),
}


class Atom():
    """Class representing an atom with specific properties.
    
    Attributes:
        type (str): The type of the atom, which must be a key in ATOM_DICT.
        mass (float): The mass of the atom, retrieved from ATOM_DICT based on the atom type.
        charge (float): The charge of the atom, retrieved from ATOM_DICT based on the atom type.
        initial_position (numpy.ndarray): The initial position of the atom in 2D space, defaulting to a zero vector if not provided.
    
    Args:
        atom_type (str, optional): The type of the atom. Must be a valid key in ATOM_DICT.
        position (numpy.ndarray, optional): The initial position of the atom. If not provided, defaults to a zero vector.
        
    Raises:
        ValueError: If the provided atom_type is not found in ATOM_DICT.
    """
    def __init__(self, atom_type=None, position=None):

        self.type = atom_type
        
        if atom_type not in ATOM_DICT:
            raise ValueError(f"{atom_type} not in ATOM_DICT")
        
        self.mass = ATOM_DICT[atom_type][0]
        self.charge = ATOM_DICT[atom_type][1]
        self.initial_position = position if position is not None else np.zeros(2)

