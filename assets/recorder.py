class MDRecorder():

    def __init__(self):
        
        self.potential = []
        self.forces = []

    def record(self, engine):
        """Record values from the MD engine the force computing
        """

        # LJ potenetial energy
        self.potential.append(engine.potential_energy)

        # Total forces
        