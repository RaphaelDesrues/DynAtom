import numpy as np # type: ignore
from engine.system import System
from engine.atom import Atom
from assets.recorder import MDRecorder


class Engine():

    def __init__(self, temperature=200, timestep=1e-15, nsteps=500, boxsize=2):

        self.recorder = MDRecorder()
        self.system = System()
        self.temperature = temperature
        self.ts = timestep
        self.nsteps = nsteps
        self.boxsize = boxsize

        # Example : Add n atoms
        self.add_atoms(100, "O")
        self.add_atoms(100, "C")
        self.add_atoms(100, "H")
        


        # self.run_md()

    def add_atoms(self, n, type):
        positions = np.random.uniform(low=0, high=self.boxsize, size=(n, 2))
        for i in range(n):
            self.system.add_atom(Atom(type, positions[i]))


    # def run_md(self, mini=False, eq=False):

    #     # Initial conditions
    #     self.set_init_pos()
    #     self.set_init_vel()

    #     # Initial forces (needed for Verlet step 1)
    #     self.calc_forces()

    #     # Initial accelerations
    #     self.calc_acc()

    #     # Minimisation / Equilibration if needed
    #     if mini:
    #         self.minimize()
    #     if eq:
    #         self.eq()

    #     # MD loop
    #     for step in range(1, self.nsteps + 1):

    #         # 1) Update positions using current velocity & acceleration
    #         self.update_pos()

    #         # 2) Recompute forces at new positions (gives F(t+dt))
    #         self.calc_forces()

    #         self.recorder.record(self)

    #         # 3) new accelerations
    #         for atom in self.system.atoms:
    #             atom.new_acc = atom.force / atom.mass

    #         # 4) Update velocities using a(t) and a(t+dt)
    #         self.update_vel()

    #         # (Optional) energy print/debug
    #         if step % 100 == 0:
    #             print("Step: ", step)

    def run_once(self):
        # 1) Update positions
        self.update_pos()


        # 2) Compute forces
        # store LJ potential energy 
        self.calc_forces()

        # 3) Compute new acc
        for atom in self.system.atoms:
            atom.new_acc = atom.force / atom.mass

        # 4) Update velocities
        self.update_vel()

        # 5) Record energies
        # self = engine
        self.recorder.record(self)


    # ----------------------
    #  Initialisation
    # ----------------------

    def set_init_pos(self):
        for atom in self.system.atoms:
            atom.position = np.array(np.random.rand(2))

    def set_init_vel(self):
        for atom in self.system.atoms:
            # Simplified for now
            atom.velocity = np.random.normal(0, np.sqrt(self.temperature / atom.mass), 2)

    # ----------------------
    #  Minimization / Equilibration
    # ----------------------


    def minimize(self):
        pass

    # ----------------------
    #  Calculs
    # ----------------------

    def calc_LJ(self):
        """
        Lennard-Jones force and potential between all atoms.
        """

        sigma = 1.0      # size parameter
        epsilon = 1.0    # interaction strength

        potential_energy = 0.0  # accumulator

        # Reset all forces
        for atom in self.system.atoms:
            # [:] means "modify in place"
            atom.force[:] = 0.0

        # Compute pairwise interactions
        atoms = self.system.atoms
        for i in range(len(atoms)):
            for j in range(i + 1, len(atoms)):

                # Vector from atom i to atom j
                r_vec = atoms[j].position - atoms[i].position

                # Distance between the two atoms (norm of the vector)
                r = np.linalg.norm(r_vec)

                # ----------------------------------------
                # 1) Lennard-Jones potential energy
                # ----------------------------------------
                sr6  = (sigma / r) ** 6
                sr12 = sr6 * sr6

                V = 4 * epsilon * (sr12 - sr6)
                potential_energy += V

                # ----------------------------------------
                # 2) Lennard-Jones force magnitude
                # F = -dV/dr
                # ----------------------------------------
                # Derivative of LJ potential:
                # F(r) = 24 * epsilon * (2*(sigma/r)^12 - (sigma/r)^6) / r
                F = 24 * epsilon * (2*sr12 - sr6) / r

                # Force vector (direction = unit vector of r_vec)
                f_vec = F * (r_vec / r)

                # Equal and opposite forces
                atoms[i].force -= f_vec
                atoms[j].force += f_vec

        return potential_energy

    def calc_forces(self):
        # Compute Lennard-Jones forces
        self.potential_energy = self.calc_LJ()

    def calc_acc(self):
        for atom in self.system.atoms:
            atom.acc = atom.force / atom.mass

    # ----------------------
    #  Update positions / velocities
    # ----------------------

    def update_vel(self):
        dt = self.ts
        for atom in self.system.atoms:
            atom.velocity += 0.5 * (atom.acc + atom.new_acc) * dt
            atom.acc = atom.new_acc

    def update_pos(self):
        dt = self.ts
        for atom in self.system.atoms:
            atom.position += atom.velocity * dt + 0.5 * atom.acc * dt * dt
            atom.position = atom.position % self.boxsize
