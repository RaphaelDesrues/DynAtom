class MDRecorder():
    """MDRecorder is a class for recording potential energy and forces from a molecular dynamics (MD) engine.
    
    Attributes:
        potential (list): A list to store recorded potential energy values.
        forces (list): A list to store recorded force values.
    
    Methods:
        record(engine): Records the potential energy from the given MD engine.
    """
    def __init__(self):
        
        self.LJ_potential = []
        self.forces = []
        self.positions = []

    def record(self, engine):
        """Record values from the MD engine the force computing
        """
        # Atom positions
        self.positions = [atom.position for atom in engine.system.atoms]

        # LJ potenetial energy
        self.LJ_potential.append(engine.potential_energy)

        # Total forces


    
        