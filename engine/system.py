class System():

    def __init__(self, atoms = None):
        
        self.atoms = atoms if atoms is not None else []

    def add_atom(self, atom):
        self.atoms.append(atom)