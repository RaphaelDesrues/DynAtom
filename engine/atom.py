import numpy as np # type: ignore


ATOM_DICT = { # type: mass
    "H": 1.0,
    "C": 16.0,
    "O": 18.0,
}


class Atom():

    def __init__(self, atom_type=None, position=None):

        self.type = atom_type
        
        if atom_type not in ATOM_DICT:
            raise ValueError(f"{atom_type} not in ATOM_DICT")
        
        self.mass = ATOM_DICT[atom_type]

        self.position = position if position is not None else np.zeros(3)
        self.velocity = np.zeros(3)
        self.acc = np.zeros(3)
        self.new_acc = np.zeros(3)
        self.force = np.zeros(3)

