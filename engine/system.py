import numpy as np #type: ignore


class System():
    """Class representing a system of atoms.
    
    This class manages the properties and behaviors of a collection of atoms, including their positions, velocities, accelerations, forces, and masses. It also calculates potential and kinetic energies.
    
    Attributes:
        atoms (list): A list of atoms in the system.
        positions (numpy.ndarray): An array of shape (n, 2) representing the positions of the atoms.
        velocities (numpy.ndarray): An array of shape (n, 2) representing the velocities of the atoms.
        accelerations (numpy.ndarray): An array of shape (n, 2) representing the accelerations of the atoms.
        forces (numpy.ndarray): An array of shape (n, 2) representing the forces acting on the atoms.
        masses (numpy.ndarray): An array of shape (n,) representing the masses of the atoms.
        ene_pot_LJ (float): The potential energy calculated using the Lennard-Jones potential.
        ene_pot_LJ_total (float): The total Lennard-Jones potential energy of the system.
        kinetic_ene (float): The kinetic energy of the system.
        potentiel_ene (float): The potential energy of the system.
        total_ene (float): The total energy of the system.
    
    Methods:
        add_atom(atom): Adds an atom to the system and updates its properties.
    """
    def __init__(self, atoms = None):
        
        self.atoms = atoms if atoms is not None else []
        
        # Numpy matrices for the calculs
        self.positions = np.zeros((0, 2))
        self.velocities = np.zeros((0, 2))
        self.accelerations = np.zeros((0, 2))
        self.forces = np.zeros((0, 2))
        self.masses = np.zeros((0,))
        self.ene_pot_LJ = 0
        self.ene_pot_LJ_total = 0
        self.kinetic_ene = 0
        self.potentiel_ene = 0
        self.total_ene = 0


    def add_atom(self, atom):
        self.atoms.append(atom)

        pos = atom.initial_position.reshape(1, 2)
        self.positions = np.vstack((self.positions, pos))
        self.velocities = np.vstack((self.velocities, np.zeros((1, 2))))
        self.accelerations = np.vstack((self.accelerations, np.zeros((1, 2))))
        self.forces = np.vstack((self.forces, np.zeros((1, 2))))
        self.masses = np.append(self.masses, atom.mass)