import numpy as np # type: ignore
 

class MDRecorder():
    """MDRecorder is a class for recording molecular dynamics simulation data.
    
    Attributes:
        positions (list): A list to store the positions of particles at each recorded step.
        forces (list): A list to store the forces acting on particles at each recorded step.
        accelerations (list): A list to store the accelerations of particles at each recorded step.
        velocities (list): A list to store the velocities of particles at each recorded step.
        LJ_potential_total (list): A list to store the total Lennard-Jones potential energy at each recorded step.
        LJ_potential_per_atom (list): A list to store the Lennard-Jones potential energy per atom at each recorded step.
        kinetic_energy (list): A list to store the kinetic energy of the system at each recorded step.
        total_energy (list): A list to store the total energy of the system at each recorded step.
        force_norm_total (list): A list to store the total norm of forces at each recorded step.
        acc_norm_total (list): A list to store the total norm of accelerations at each recorded step.
        vel_norm_total (list): A list to store the total norm of velocities at each recorded step.
    
    Methods:
        record(engine): Records the current state of the simulation, including positions, velocities, accelerations, forces, and energy metrics.
    """
    def __init__(self):
        
        self.positions = []
        self.forces = []
        self.accelerations = []
        self.velocities = []

        self.LJ_potential_total = []
        self.LJ_potential_per_atom = []
        self.kinetic_energy = []
        self.total_energy = []

        self.force_norm_total = []
        self.acc_norm_total = []
        self.vel_norm_total = []

    def record(self, engine):
        # Data per atoms        
        self.positions.append(engine.system.positions.copy())
        self.velocities.append(engine.system.velocities.copy())
        self.accelerations.append(engine.system.accelerations.copy())
        self.forces.append(engine.system.forces.copy())

        # Energies
        self.LJ_potential_total.append(engine.system.ene_pot_LJ_total)
        self.LJ_potential_per_atom.append(engine.system.ene_pot_LJ.copy())
        self.kinetic_energy.append(engine.system.kinetic_ene)
        self.total_energy.append(engine.system.total_ene)

        # Total forces
        f_norm = np.linalg.norm(engine.system.forces, axis=1).sum()
        self.force_norm_total.append(f_norm)

        # Total accelerations
        a_norm = np.linalg.norm(engine.system.accelerations, axis=1).sum()
        self.acc_norm_total.append(a_norm)

        # Total velocities
        v_norm = np.linalg.norm(engine.system.velocities, axis=1).sum()
        self.vel_norm_total.append(v_norm)


    
        