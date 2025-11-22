import numpy as np # type: ignore


ATOM_DICT = { # type: mass
    "H": 1.0,
    "C": 16.0,
    "O": 18.0,
}


class Atom():
    """Class representing an atom in a physical system.
    
    Attributes:
        type (str): The type of the atom, which must be a key in ATOM_DICT.
        mass (float): The mass of the atom, retrieved from ATOM_DICT based on the atom type.
        position (numpy.ndarray): The position of the atom in 2D space, default is a zero vector.
        velocity (numpy.ndarray): The velocity of the atom in 2D space, initialized to a zero vector.
        acc (numpy.ndarray): The current acceleration of the atom in 2D space, initialized to a zero vector.
        new_acc (numpy.ndarray): The new acceleration of the atom in 2D space, initialized to a zero vector.
        force (numpy.ndarray): The force acting on the atom in 2D space, initialized to a zero vector.
    
    Args:
        atom_type (str, optional): The type of the atom. Must be a valid key in ATOM_DICT.
        position (numpy.ndarray, optional): The initial position of the atom. If None, defaults to a zero vector.
    
    Raises:
        ValueError: If atom_type is not in ATOM_DICT.
    """
    def __init__(self, atom_type=None, position=None):

        self.type = atom_type
        
        if atom_type not in ATOM_DICT:
            raise ValueError(f"{atom_type} not in ATOM_DICT")
        
        self.mass = ATOM_DICT[atom_type]

        self.position = position if position is not None else np.zeros(2)
        self.velocity = np.zeros(2)
        self.acc = np.zeros(2)
        self.new_acc = np.zeros(2)
        self.force = np.zeros(2)

