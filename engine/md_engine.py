import numpy as np # type: ignore
from engine.system import System
from engine.atom import Atom
import logging


class Engine():

    def __init__(self, params, recorder):
        self.system = System()
        self.params = params
        self.recorder = recorder

        n_atoms = self.params["n_atoms"]
        self.add_atoms(n=n_atoms, type="C")

    def add_atoms(self, n, type):
        positions = self.set_init_pos(n)
        for i in range(n):
            self.system.add_atom(Atom(type, positions[i]))

    def run_once(self):

        # 1) Compute forces at t
        self.calc_forces()
        
        # 2) Compute new acc
        self.update_acc()

        # 3) Update positions
        self.update_pos()

        # 4) Compute forces at t+dt
        self.calc_forces()
        new_acc = self.system.forces / self.system.masses[:,None]

        # 3) Update velocities
        self.update_vel(new_acc)

        # 5) Update accelerations
        self.system.accelerations = new_acc

        # Record energies
        # self = engine
        self.recorder.record(self)

    # ----------------------
    #  Initialisation
    # ----------------------

    def set_init_pos(self, n):
        return np.random.uniform(low=0,
                                 high=self.params["boxsize"],
                                 size=(n, 2)
                                )

    def set_init_vel(self):
        temp = self.params["temperature"]
        # Simplified for now
        self.system.velocities = np.random.normal(
            0, np.sqrt(temp / self.system.masses)[:,None],
            (len(self.system.masses),2)
        )


    # ----------------------
    #  Minimization / Equilibration
    # ----------------------

    def minimize(self, n_steps=100000, int_step=1e-6, conv_crit=1e-3):
        logging.info("Computing Minimisation...")
        for i in range(n_steps):
            if i % 10000 == 0:
                logging.info(f"Minimisation step n° {i}")
            # Calc atom forces
            self.calc_forces()
            F = self.system.forces # (N,2)

            # Force vector norm for each atom
            norm = np.linalg.norm(F, axis=1, keepdims=True) # (N,1)

            # Avoid division by 0
            norm[norm == 0] = 1

            # Compute a normalised (norm = 1) vector
            # Avoid movement scales difference between atoms
            F_normalised = F / norm

            # Update positions
            self.system.positions += int_step*F_normalised

            # Ensure periodicity
            self.system.positions %= self.params["boxsize"]

            # if hasattr(self, "render_step"):
                # logging.warning("Engine has render_step")
                # self.render_step()
            self.recorder.record(self)
            # Stop if converged upon criterion
            if np.max(norm) < conv_crit:
                logging.info("Minimisation converged!")
                break
        logging.info("Minimisation has not converged")

    def equilibrate(self, n_steps=100000, tau=1e-1):
        logging.info("Computing Equilibration...")
        dt = self.params["timestep"]
        T_target = self.params["temperature"]

        self.calc_forces()
        self.update_acc()

        for i in range(n_steps):
            if i % 10000 == 0:
                logging.info(f"Equilibration step n° {i}")
            # 1) Update positions
            self.update_pos()

            # 2) Compute forces at new positions
            self.calc_forces()
            new_acc = self.system.forces / self.system.masses[:,None]

            # 3) Update velocities
            self.update_vel(new_acc)

            # 4) Replace accelerations
            self.system.accelerations = new_acc

            # ---- THERMOSTAT BERENDSEN ----
            T = self.compute_temperature()

            # Avoid division by zero if T = 0
            if T == 0:
                continue

            lambda_T = np.sqrt(1 + dt/tau * (T_target/T - 1))

            # Scale velocities
            self.system.velocities *= lambda_T
        logging.info("Equilibration finished")

    # ----------------------
    #  Calculs
    # ----------------------

    def calc_kinetic_ene(self):
        """Compute the total kinetic energy """
        m = self.system.masses # (N,)
        v2 = np.sum(self.system.velocities**2, axis=1) # (N,)
        self.system.kinetic_ene = 0.5 * np.sum(m * v2)
        return self.system.kinetic_ene

    def calc_LJ(self):
        """
        Lennard-Jones force and potential between all atoms.
        """

        sigma = 1.0      # size parameter
        epsilon = 1.0    # interaction strength

        # Compute pairwise interactions
        # Vector from atom i to atom j, shape (N,N,2)
        r_vec = self.system.positions[:, None, :] - \
                self.system.positions[None, :, :]

        # Distance between the two atoms (norm of the vector)
        r = np.linalg.norm(r_vec, axis = 2)
        r[r == 0] = np.inf

        # ----------------------------------------
        # 1) Lennard-Jones potential energy
        # ----------------------------------------
        sr6  = (sigma / r) ** 6
        sr12 = sr6 * sr6

        ene =  4 * epsilon * (sr12 - sr6)
        # Potential energy for each atom
        self.system.ene_pot_LJ = np.sum(ene, axis=1)
        # Total potential energy
        self.system.ene_pot_LJ_total = 0.5 * np.sum(ene)

        # ----------------------------------------
        # 2) Lennard-Jones force magnitude
        # F = -dV/dr
        # ----------------------------------------
        # Derivative of LJ potential:
        # F(r) = 24 * epsilon * (2*(sigma/r)^12 - (sigma/r)^6) / r
        F = 24 * epsilon * (2*sr12 - sr6) / r
        F = F[:, :, None]

        # Force vector (direction = unit vector of r_vec)
        f_vec = F * (r_vec / r[:, :, None])

        # Equal and opposite forces
        # For each component of each atom, we sum the partial force
        # from all interactions (N, 2) # N atoms ; x, y components
        return f_vec.sum(axis=1)

    def calc_forces(self):
        # Compute Lennard-Jones forces
        self.system.forces = self.calc_LJ()

    def calc_total_ene(self):
        K_ene = self.calc_kinetic_ene()
        V_ene = self.system.ene_pot_LJ_total # todo: modify to total V
        self.system.total_ene = K_ene + V_ene

    def calc_acc(self):
        # (N, 2) and (N,) not possible -> (N, 1) for masses
        self.system.accelerations = self.system.forces / \
                                    self.system.masses[:, None]

    def compute_temperature(self):
        v2 = np.sum(self.system.velocities**2, axis=1)
        kinetic = 0.5 * np.sum(self.system.masses * v2)
        N = len(self.system.masses)
        dof = 2 * N    # 2D = 2 DOF per atom
        return kinetic / (0.5 * dof)

    # ----------------------
    #  Update positions / velocities
    # ----------------------

    def update_acc(self):
        self.system.accelerations = self.system.forces / \
        self.system.masses[:,None]

    def update_vel(self, new_acc):
        dt = self.params["timestep"]
        self.system.velocities += 0.5 * (
            self.system.accelerations + new_acc
        ) * dt

    def update_pos(self):
        dt = self.params["timestep"]
        self.system.positions += (
            self.system.velocities * dt + \
            0.5 * self.system.accelerations * dt * dt
        )

        self.system.positions %= self.params["boxsize"]







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