try:
    from sage_lib.partition.PartitionManager import PartitionManager
    from sage_lib.miscellaneous.data_mining import *
    from sage_lib.miscellaneous.SOAP_tools import *

except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del sys

try:
    import numpy as np

    from sklearn.manifold import TSNE
    from sklearn.decomposition import PCA

except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sklearn.manifold: {str(e)}\n")
    del sys

try:
    import os
    import copy
    from tqdm import tqdm
    from typing import Dict, List, Tuple, Union
    from collections import defaultdict
    from joblib import Memory

except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing os: {str(e)}\n")
    del sys
    
try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    import seaborn as sns
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while matplotlib || seaborn: {str(e)}\n")
    del sys

class AbInitioThermodynamics_builder(PartitionManager):
    """
    A class for performing Ab Initio Thermodynamics analysis on atomic structures.

    This class extends PartitionManager to handle composition data, energy data, and perform
    various analyses such as phase diagram generation, local linear regression, and global linear prediction.

    Attributes:
        composition_data (np.ndarray): Array containing composition data for each structure.
        energy_data (np.ndarray): Array containing energy data for each structure.
        area_data (np.ndarray): Array containing area data for each structure.
    """

    def __init__(self, file_location: str = None, name: str = None, **kwargs):
        """
        Initialize the AbInitioThermodynamics_builder.

        Args:
            file_location (str, optional): Location of input files.
            name (str, optional): Name of the analysis.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(name=name, file_location=file_location)
        
        self.composition_data = None
        self.energy_data = None 
        self.area_data = None

    def plot_phase_diagram(self, diagram_data: np.ndarray, mu_max: float, mu_min: float, 
                           output_path: str = None, window_size: Tuple[int, int] = (12, 8), 
                           save: bool = True, verbose: bool = True) -> None:
        """
        Plot a phase diagram with extrapolated lines and highlight the lower envelope.

        Args:
            diagram_data (np.ndarray): An Nx2 array with each row being [y-intercept, slope] for a line.
            mu_max (float): Maximum chemical potential value.
            mu_min (float): Minimum chemical potential value.
            output_path (str, optional): Path to save the plot image.
            window_size (Tuple[int, int]): Size of the plotting window.
            save (bool): Whether to save the plot to a file.
            verbose (bool): Whether to print additional information.
        """
        print("Generating phase diagram plot...")

        plt.figure(figsize=window_size)

        x_values = np.linspace(mu_min, mu_max, 100)
        lower_envelope = np.inf * np.ones_like(x_values)
        optimal_structures = []

        for index, (x, y) in enumerate(diagram_data):
            m = (y - x) / (1 - 0)
            b = y - m * 1
            y_values = m * x_values + b
            
            plt.plot(x_values, y_values, alpha=0.5, label=f'Structure {index}')

            # Update lower envelope
            mask = y_values < lower_envelope
            lower_envelope[mask] = y_values[mask]
            optimal_structures.append(index)

        # Plot lower envelope
        plt.plot(x_values, lower_envelope, 'k-', linewidth=2, label='Lower Envelope')

        plt.xlabel('Chemical Potential (μ)')
        plt.ylabel('Formation Energy (γ)')
        plt.title('Phase Diagram with Lower Envelope')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)

        if save:
            if not output_path:
                output_path = '.'
            plt.savefig(f'{output_path}/phase_diagram_plot.png', dpi=300, bbox_inches='tight')
            if verbose:
                print(f"Phase diagram plot saved to {output_path}/phase_diagram_plot.png")
        else:
            plt.show()

        if verbose:
            print(f"Optimal structures: {optimal_structures}")

    def plot_manifold(self, features: np.ndarray, response: np.ndarray, 
                      output_path: str = None, save: bool = True, 
                      verbose: bool = True) -> None:
        """
        Plot the manifold of the data using T-SNE and PCA, along with the response variable.

        Args:
            features (np.ndarray): Feature array (typically composition data).
            response (np.ndarray): Response array (typically energy or error data).
            output_path (str, optional): Path to save the plot.
            save (bool): Whether to save the plot to a file.
            verbose (bool): Whether to print additional information.
        """
        print("Generating manifold plots using T-SNE and PCA...")

        tsne = TSNE(n_components=2, random_state=42)
        tsne_results = tsne.fit_transform(features)

        pca = PCA(n_components=3)
        pca_results = pca.fit_transform(features)
        explained_variance = pca.explained_variance_ratio_

        fig, ax = plt.subplots(2, 2, figsize=(20, 20))

        # T-SNE plot
        sc = ax[0, 0].scatter(tsne_results[:, 0], tsne_results[:, 1], c=response, cmap='viridis')
        ax[0, 0].set_title('T-SNE Projection')
        ax[0, 0].set_xlabel('T-SNE Component 1')
        ax[0, 0].set_ylabel('T-SNE Component 2')
        plt.colorbar(sc, ax=ax[0, 0], label='Response')

        # PCA plot (2D projection)
        sc_pca = ax[0, 1].scatter(pca_results[:, 0], pca_results[:, 1], c=response, cmap='viridis')
        ax[0, 1].set_title('PCA Projection (2D)')
        ax[0, 1].set_xlabel(f'PCA Component 1 ({explained_variance[0]*100:.2f}% variance)')
        ax[0, 1].set_ylabel(f'PCA Component 2 ({explained_variance[1]*100:.2f}% variance)')
        plt.colorbar(sc_pca, ax=ax[0, 1], label='Response')

        # PCA plot (3D projection)
        ax_3d = fig.add_subplot(223, projection='3d')
        sc_pca_3d = ax_3d.scatter(pca_results[:, 0], pca_results[:, 1], pca_results[:, 2], 
                                  c=response, cmap='viridis')
        ax_3d.set_title('PCA Projection (3D)')
        ax_3d.set_xlabel(f'PC1 ({explained_variance[0]*100:.2f}%)')
        ax_3d.set_ylabel(f'PC2 ({explained_variance[1]*100:.2f}%)')
        ax_3d.set_zlabel(f'PC3 ({explained_variance[2]*100:.2f}%)')
        plt.colorbar(sc_pca_3d, ax=ax_3d, label='Response')

        # Response plot
        ax[1, 1].plot(response, 'o-', c='#1f77b4')
        RMSE = np.sqrt(np.mean(response**2))
        ax[1, 1].axhline(y=RMSE, color='r', linestyle='--', label=f'RMSE: {RMSE:.5f}')
        ax[1, 1].set_title('Response Distribution')
        ax[1, 1].set_xlabel('Index')
        ax[1, 1].set_ylabel('Response')
        ax[1, 1].legend()
        plt.tight_layout()

        if save:
            if not output_path:
                output_path = '.'
            plt.savefig(f'{output_path}/manifold_plot.png', dpi=300)
            if verbose:
                print(f"Manifold plot saved to {output_path}/manifold_plot.png")
        else:
            plt.show()

        if verbose:
            print(f"PCA explained variance ratios: {explained_variance}")

    def calculate_ensemble_properties(self, energies: np.ndarray, volumes: np.ndarray, 
                                      temperatures: np.ndarray, particles: np.ndarray,
                                      ensemble: str = 'canonical', mass: float = 1.0,
                                      output_path: str = None, save: bool = True, 
                                      verbose: bool = True) -> Dict[str, np.ndarray]:
        """
        Calculate partition function and thermodynamic parameters for different ensembles.

        Args:
            energies (np.ndarray): Energy levels of the system.
            volumes (np.ndarray): Volumes of the system.
            temperatures (np.ndarray): Array of temperatures to analyze.
            particles (np.ndarray): Array of particle numbers (for grand canonical ensemble).
            ensemble (str): Type of ensemble ('canonical', 'microcanonical', 'grand_canonical').
            mass (float): Mass of the particles (used in some calculations).
            output_path (str, optional): Path to save the plots.
            save (bool): Whether to save the plots to files.
            verbose (bool): Whether to print additional information.

        Returns:
            Dict[str, np.ndarray]: Dictionary of calculated thermodynamic properties.
        """
        print(f"Calculating ensemble properties for {ensemble} ensemble...")

        k_B = Boltzmann
        h = hbar * 2 * pi
        properties = {}

        if ensemble == 'canonical':
            # Canonical ensemble calculations
            Z = np.sum(np.exp(-energies[:, np.newaxis] / (k_B * temperatures)), axis=0)
            properties['partition_function'] = Z
            
            # Free energy
            F = -k_B * temperatures * np.log(Z)
            properties['free_energy'] = F
            
            # Internal energy
            U = np.sum(energies[:, np.newaxis] * np.exp(-energies[:, np.newaxis] / (k_B * temperatures)), axis=0) / Z
            properties['internal_energy'] = U
            
            # Entropy
            S = k_B * np.log(Z) + U / temperatures
            properties['entropy'] = S
            
            # Heat capacity
            C_V = k_B * (np.sum(energies[:, np.newaxis]**2 * np.exp(-energies[:, np.newaxis] / (k_B * temperatures)), axis=0) / Z
                         - (np.sum(energies[:, np.newaxis] * np.exp(-energies[:, np.newaxis] / (k_B * temperatures)), axis=0) / Z)**2) / temperatures**2
            properties['heat_capacity'] = C_V

        elif ensemble == 'microcanonical':
            # Microcanonical ensemble calculations
            # Assuming a simple model where Ω(E) ~ E^(3N/2-1) for an ideal gas
            N = len(particles)  # Number of particles
            Omega = energies**(3*N/2 - 1)
            properties['density_of_states'] = Omega
            
            # Entropy
            S = k_B * np.log(Omega)
            properties['entropy'] = S
            
            # Temperature (derived from entropy)
            T = 1 / (np.gradient(S, energies))
            properties['temperature'] = T
            
            # Heat capacity
            C_V = 1 / (np.gradient(1/T, energies))
            properties['heat_capacity'] = C_V

        elif ensemble == 'grand_canonical':
            # Grand Canonical ensemble calculations
            mu = np.linspace(np.min(energies), np.max(energies), 100)  # Chemical potential range
            Z_grand = np.sum(np.exp((mu[:, np.newaxis, np.newaxis] - energies[:, np.newaxis]) / (k_B * temperatures)), axis=0)
            properties['grand_partition_function'] = Z_grand
            
            # Grand potential
            Omega = -k_B * temperatures * np.log(Z_grand)
            properties['grand_potential'] = Omega
            
            # Average number of particles
            N_avg = np.sum(particles[:, np.newaxis, np.newaxis] * np.exp((mu[:, np.newaxis, np.newaxis] - energies[:, np.newaxis]) / (k_B * temperatures)), axis=0) / Z_grand
            properties['average_particles'] = N_avg
            
            # Internal energy
            U = np.sum(energies[:, np.newaxis, np.newaxis] * np.exp((mu[:, np.newaxis, np.newaxis] - energies[:, np.newaxis]) / (k_B * temperatures)), axis=0) / Z_grand
            properties['internal_energy'] = U

        # Plotting
        fig, axs = plt.subplots(2, 2, figsize=(16, 16))
        
        if ensemble == 'canonical':
            axs[0, 0].plot(temperatures, properties['free_energy'])
            axs[0, 0].set_xlabel('Temperature (K)')
            axs[0, 0].set_ylabel('Free Energy (J)')
            axs[0, 0].set_title('Free Energy vs Temperature')

            axs[0, 1].plot(temperatures, properties['internal_energy'])
            axs[0, 1].set_xlabel('Temperature (K)')
            axs[0, 1].set_ylabel('Internal Energy (J)')
            axs[0, 1].set_title('Internal Energy vs Temperature')

            axs[1, 0].plot(temperatures, properties['entropy'])
            axs[1, 0].set_xlabel('Temperature (K)')
            axs[1, 0].set_ylabel('Entropy (J/K)')
            axs[1, 0].set_title('Entropy vs Temperature')

            axs[1, 1].plot(temperatures, properties['heat_capacity'])
            axs[1, 1].set_xlabel('Temperature (K)')
            axs[1, 1].set_ylabel('Heat Capacity (J/K)')
            axs[1, 1].set_title('Heat Capacity vs Temperature')

        elif ensemble == 'microcanonical':
            axs[0, 0].plot(energies, properties['density_of_states'])
            axs[0, 0].set_xlabel('Energy (J)')
            axs[0, 0].set_ylabel('Density of States')
            axs[0, 0].set_title('Density of States vs Energy')

            axs[0, 1].plot(energies, properties['entropy'])
            axs[0, 1].set_xlabel('Energy (J)')
            axs[0, 1].set_ylabel('Entropy (J/K)')
            axs[0, 1].set_title('Entropy vs Energy')

            axs[1, 0].plot(energies, properties['temperature'])
            axs[1, 0].set_xlabel('Energy (J)')
            axs[1, 0].set_ylabel('Temperature (K)')
            axs[1, 0].set_title('Temperature vs Energy')

            axs[1, 1].plot(energies, properties['heat_capacity'])
            axs[1, 1].set_xlabel('Energy (J)')
            axs[1, 1].set_ylabel('Heat Capacity (J/K)')
            axs[1, 1].set_title('Heat Capacity vs Energy')

        elif ensemble == 'grand_canonical':
            axs[0, 0].pcolormesh(temperatures, mu, properties['grand_potential'])
            axs[0, 0].set_xlabel('Temperature (K)')
            axs[0, 0].set_ylabel('Chemical Potential (J)')
            axs[0, 0].set_title('Grand Potential')

            axs[0, 1].pcolormesh(temperatures, mu, properties['average_particles'])
            axs[0, 1].set_xlabel('Temperature (K)')
            axs[0, 1].set_ylabel('Chemical Potential (J)')
            axs[0, 1].set_title('Average Number of Particles')

            axs[1, 0].pcolormesh(temperatures, mu, properties['internal_energy'])
            axs[1, 0].set_xlabel('Temperature (K)')
            axs[1, 0].set_ylabel('Chemical Potential (J)')
            axs[1, 0].set_title('Internal Energy')

        plt.tight_layout()

        if save:
            if not output_path:
                output_path = '.'
            plt.savefig(f'{output_path}/{ensemble}_ensemble_properties.png', dpi=300)
            if verbose:
                print(f"{ensemble.capitalize()} ensemble properties plot saved to {output_path}/{ensemble}_ensemble_properties.png")
        else:
            plt.show()

        if verbose:
            print(f"Calculation of {ensemble} ensemble properties completed.")

        return properties

    def get_composition_data(self) -> Dict[str, np.ndarray]:
        """
        Extract composition, energy, and area data from containers.

        Returns:
            Dict[str, np.ndarray]: Dictionary containing composition_data, energy_data, and area_data.
        """
        print("Extracting composition, energy, and area data from containers...")
        
        composition_data = np.zeros((len(self.containers), len(self.uniqueAtomLabels)), dtype=np.float64)
        energy_data = np.zeros(len(self.containers), dtype=np.float64)
        area_data = np.zeros(len(self.containers), dtype=np.float64)
        
        for c_i, c in enumerate(self.containers):  
            comp = np.zeros_like(self.uniqueAtomLabels, dtype=np.int64)
            for ual, ac in zip(c.AtomPositionManager.uniqueAtomLabels, c.AtomPositionManager.atomCountByType):
                comp[self.uniqueAtomLabels_order[ual]] = ac 

            composition_data[c_i,:] = comp
            energy_data[c_i] = c.AtomPositionManager.E
            area_data[c_i] = c.AtomPositionManager.get_area('z')

        self.composition_data, self.energy_data, self.area_data = composition_data, energy_data, area_data

        print(f"Extracted data for {len(self.containers)} structures.")
        return {'composition_data': composition_data, 'energy_data': energy_data, 'area_data': area_data, 'uniqueAtomLabels':self.uniqueAtomLabels}

    def get_diagram_data(self, ID_reference: List[int], composition_data: np.ndarray, 
                         energy_data: np.ndarray, area_data: np.ndarray, especie: str) -> np.ndarray:
        """
        Calculate diagram data for phase diagram generation.

        Args:
            ID_reference (List[int]): List of reference structure IDs.
            composition_data (np.ndarray): Array of composition data.
            energy_data (np.ndarray): Array of energy data.
            area_data (np.ndarray): Array of area data.
            especie (str): Chemical species to focus on.

        Returns:
            np.ndarray: Array containing diagram data for phase diagram plotting.
        """
        print(f"Calculating diagram data for phase diagram generation, focusing on species: {especie}")
        
        composition_reference = composition_data[ID_reference, :] 
        energy_reference = energy_data[ID_reference] 

        reference_mu_index = next(cr_i for cr_i, cr in enumerate(composition_reference) 
                                  if np.sum(cr) == cr[self.uniqueAtomLabels_order[especie]])

        mask = np.ones(len(energy_data), dtype=bool)
        mask[ID_reference] = False

        composition_relevant = composition_data[mask,:]
        energy_relevant = energy_data[mask]
        area_relevant = area_data[mask]

        diagram_data = np.zeros((energy_relevant.shape[0], 2))

        for mu in [0, 1]:
            for i, (E, C, A) in enumerate(zip(energy_relevant, composition_relevant, area_relevant)):
                E_ref_mask = np.zeros_like(energy_reference)
                E_ref_mask[reference_mu_index] = mu

                mu_value = np.linalg.solve(composition_reference, energy_reference + E_ref_mask)
                gamma = 1/A * (E - np.sum(mu_value * C))

                diagram_data[i, mu] = gamma

        print(f"Diagram data calculated for {energy_relevant.shape[0]} structures.")
        return diagram_data

    def generate_atom_labels_and_cluster_counts(self,
        atom_clusters: Dict[str, Union[List[int], np.ndarray]],
        atom_structures: Dict[str, Union[List[Union[List[int], np.ndarray]], np.ndarray]]
    ) -> Tuple[List[np.ndarray], np.ndarray, List[str]]:
        """
        Generate atom labels for each structure, count clusters across structures, and create class labels.

        This function processes atomic clustering data and structural information to produce:
        1. A list of numpy arrays, each containing cluster labels for atoms in a structure.
        2. A matrix counting the number of atoms in each cluster for each structure.
        3. A list of class labels in the format "Element_ClusterNumber", including outliers.

        Parameters:
        atom_clusters (Dict[str, Union[List[int], np.ndarray]]): A dictionary where keys are element symbols
                                              and values are lists or arrays of cluster labels for each atom.
        atom_structures (Dict[str, Union[List[Union[List[int], np.ndarray]], np.ndarray]]): A dictionary where keys are element symbols
                                                      and values are either:
                                                      - A list of two arrays: [structure_ids, atom_ids]
                                                      - A 2D numpy array with columns [structure_id, atom_id]

        Returns:
        Tuple[List[np.ndarray], np.ndarray, List[str]]: 
            - A list of numpy arrays, each containing cluster labels for atoms in a structure.
            - A 2D numpy array where rows represent structures and columns represent clusters,
              with each cell containing the count of atoms in that cluster for that structure.
            - A list of class labels in the format "Element_ClusterNumber", including outliers.

        Note:
        - Clusters are treated independently for each species.
        - Outliers (cluster label -1) are treated as a separate class for each species.
        """
        # Determine the number of structures

        num_structures = len(self.containers)

        # Count total clusters, create a mapping for cluster indices, and generate class labels
        total_clusters = 0
        cluster_mapping = {}
        class_labels_mapping = {}
        class_labels = []
        for element in self.uniqueAtomLabels:
            #for element, clusters in atom_clusters.items():
            clusters = atom_clusters[element]
            unique_clusters = sorted(set(clusters))  # Include -1 in unique cluster count
            cluster_mapping[element] = {c: i + total_clusters for i, c in enumerate(unique_clusters)}
            class_labels.extend([f"{element}_{c}" for c in unique_clusters])
            class_labels_mapping[element] = {c: f"{element}_{c}" for i, c in enumerate(unique_clusters)}
            total_clusters += len(unique_clusters)

        # Initialize output structures
        structure_labels1 = [ np.zeros( c.AtomPositionManager.atomCount, dtype=np.int64 ) for c_i, c in enumerate(self.containers) ]
        cluster_counts1 = np.zeros((int(num_structures), int(total_clusters)), dtype=int)


        for element, clusters in atom_clusters.items():
            for i, c in enumerate(clusters):
                struct_id = int(atom_structures[element][i][0])
                atom_id = int(atom_structures[element][i][1])
                cluster = c

                clusteridx = cluster_mapping[element][cluster]

                structure_labels1[struct_id][atom_id] = clusteridx
                cluster_counts1[struct_id, clusteridx] += 1

        # Initialize output structures
        structure_labels = [ np.zeros( c.AtomPositionManager.atomCount, dtype=np.int64 ) for c_i, c in enumerate(self.containers) ]
        cluster_counts = np.zeros((int(num_structures), int(total_clusters)), dtype=int)

        # Process each element
        for element, clusters in atom_clusters.items():
            structures = atom_structures[element]
            element_mapping = cluster_mapping[element]

            if isinstance(structures, list):  # [structure_ids, atom_ids]
                struct_ids, atom_ids = structures
            else:  # 2D numpy array
                struct_ids, atom_ids = structures[:, 0], structures[:, 1]

            for struct_id, atom_id in zip(struct_ids, atom_ids):
                struct_id = int(struct_id)
                atom_id = int(atom_id)
                cluster = int(clusters[atom_id])

                # Map the cluster to its new index
                mapped_cluster = element_mapping[cluster]

                # Assign cluster label to the atom in its structure
                structure_labels[struct_id][atom_id] = mapped_cluster

                # Update cluster count for this structure
                cluster_counts[struct_id, mapped_cluster] += 1
        
        # Convert structure_labels to numpy arrays
        structure_labels = [np.array(labels) for labels in structure_labels]
        #print(structure_labels1[0], cluster_counts1, class_labels)
        #print(structure_labels[0] == structure_labels1[0], cluster_counts == cluster_counts1, class_labels)

        return structure_labels1, cluster_counts1, class_labels

    def plot_species_clusters(self, class_labels, coefficients_cluster, uniqueAtomLabels, coefficients, output_file='./species_clusters.png'):

        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        # Crear un diccionario para agrupar los clusters por especie
        species_clusters = {species: [] for species in uniqueAtomLabels}
        for label, coef in zip(class_labels, coefficients_cluster):
            species = label.split('_')[0]
            species_clusters[species].append((label, coef))
        
        # Crear un gráfico para cada especie
        for i, species in enumerate(uniqueAtomLabels):
            plt.figure(figsize=(10, 6))
            
            # Línea horizontal para el coeficiente de la especie
            plt.axhline(y=coefficients[i], color='r', linestyle='-', label=f'{species} coefficient')
            
            # Puntos para cada cluster
            clusters = species_clusters[species]
            x = np.arange(len(clusters))
            y = [coef for _, coef in clusters]
            
            plt.scatter(x, y, color='b')
            
            # Añadir etiquetas para cada cluster
            for j, (label, coef) in enumerate(clusters):
                plt.annotate(label, (x[j], y[j]), xytext=(5, 5), textcoords='offset points')
            
            plt.title(f'Comparison of {species} coefficient with its clusters')
            plt.xlabel('Clusters')
            plt.ylabel('Coefficient value')
            plt.legend()
            plt.grid(True)
            
            # Ajustar los límites del eje y para que se vean bien todos los puntos
            plt.ylim(min(min(y), coefficients[i]) - 0.1, max(max(y), coefficients[i]) + 0.1)
            
            # Quitar las etiquetas del eje x
            plt.xticks([])
            
            plt.tight_layout()
            plt.savefig(f'{output_file}_{species}.png')
            plt.close()

    def plot_RBF_cluster(self, cutoff:float=3.0, number_of_bins:int=100, output_path:str='./'):
        directory = os.path.dirname(output_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        rbf = {}
        for c_i, c in enumerate(self.containers):
            
            rbf_ci = c.AtomPositionManager.get_RBF_class(cutoff=cutoff, number_of_bins=number_of_bins, 
                bin_volume_normalize=False, number_of_atoms_normalize=False, density_normalize=False) 

            # pack all RBF from same cluster class
            for cluster_class_name, rbf_ccn in rbf_ci.items():
                if not cluster_class_name in rbf:
                    rbf[cluster_class_name] = {}

                for atomlabel_class_name, rbf_ccn_acn in rbf_ccn.items():
                    if not atomlabel_class_name in rbf[cluster_class_name]:
                        rbf[cluster_class_name][atomlabel_class_name] = np.zeros((2,number_of_bins))

                    rbf[cluster_class_name][atomlabel_class_name][0] = rbf_ccn_acn[0]
                    rbf[cluster_class_name][atomlabel_class_name][1] += rbf_ccn_acn[1]

        for cluster_class_name, rbf_ccn in rbf.items():
            fig, ax = plt.subplots()

            ax.set_xlabel('Distance (Angstrom)')
            ax.set_ylabel('g(r)')
            ax.set_title(f'Radial Distribution Function {cluster_class_name} ') 

            for atomlabel_class_name, rbf_ccn_acn in rbf_ccn.items():
                bin_centers, rbf_a = rbf_ccn_acn
                color = self.element_colors[atomlabel_class_name] 

                ax.plot(bin_centers, rbf_a, 'x-', alpha=0.8, color=color, label=f'd({cluster_class_name}-{atomlabel_class_name})' )
                ax.fill_between(bin_centers, rbf_a, alpha=0.1, color=color )  # Rellena debajo de la línea con transparencia

            ax.legend()
            if True: 
                plt.tight_layout()
                plt.savefig(f"{output_path}/RBF_{cluster_class_name}.png")  
                plt.clf()

            plt.close(fig)

    def handleABITAnalysis(self, values: Dict[str, Dict], file_location: str = None) -> None:
        """
        Handle Ab Initio Thermodynamics analysis based on specified values.

        Args:
            values (Dict[str, Dict]): Dictionary of analysis types and their parameters.
            file_location (str, optional): File location for output data.
        """
        print("Starting Ab Initio Thermodynamics analysis...")

        composition_data = self.get_composition_data()
        uniqueAtomLabels = composition_data['uniqueAtomLabels']
        compositions = composition_data['composition_data']
        energies = composition_data['energy_data']

        for abit, params in values.items():

            if abit.upper() == 'PHASE_DIAGRAM':
                print(f"Performing Phase Diagram analysis. Reference : {params.get('reference', ['GLOBAL'])[0].upper()},")

                if params.get('reference', ['GLOBAL'])[0].upper() == 'GLOBAL':

                    coefficients, predictions, residuals = self.linear_predict(
                              compositions, energies,
                              regularization = 1e-8, verbose = params.get('verbose', True), 
                              zero_intercept = True, force_negative = True)

                elif params.get('reference', ['GLOBAL'])[0].upper() == 'LOCAL':
                    if params.get('opt', True):
                        print("Optimizing k value for local linear regression...")
                        params['k'], initial_errors, refined_errors, coeffs = self.find_optimal_k(
                            composition_data=composition_data,
                            verbose=params.get('verbose', False)
                            )

                else:
                    diagram_data = self.get_diagram_data(
                        ID_reference=params.get('reference', [0]),
                        composition_data=composition_data['composition_data'],
                        energy_data=composition_data['energy_data'],
                        area_data=composition_data['area_data'],
                        especie=params.get('especie', None)
                    )

                    self.plot_phase_diagram(
                        diagram_data,
                        output_path=params.get('output_path', '.'),
                        save=True,
                        verbose=params.get('verbose', True),
                        mu_max=params.get('mu_max', 1),
                        mu_min=params.get('mu_min', 0)
                        )

            if abit.upper() == 'ENSEMBLE_ANALYSIS':
                pass 

            if abit.upper() == 'COMPOSITION_ANALYSIS':
                '''
                1linear
                    A sensibility
                2SOAP 
                    >> r_cut, n_max, l_max, sigma = 4.0, 12, 12, 0.2
                3compress
                    >> n_components = 20 
                4cluster
                    >> eps, n_sample = 0.5, 10
                5linear 
                '''
                print("Performing COMPOSITION analysis...")
                print(" >> Linear model.") 
                linear_analysis = LinearAnalysis(X=compositions, y=energies)
                coefficients, predictions, residuals = linear_analysis.linear_predict(
                                        regularization = 1e-5, verbose = params.get('verbose', True), 
                                        zero_intercept = True, force_negative = False)
                linear_analysis.save_output(output_dir='linear')
                linear_analysis.analysis(output_dir='linear')

                # =========== =========== =========== =========== #
                r_cut = params.get('r_cut', 4.0)
                n_max, l_max = params.get('n_max', 12), params.get('l_max', 12)
                sigma = params.get('sigma', 0.01)

                symbols     = [c.AtomPositionManager.atomLabelsList for c in self.containers] 
                positions   = [c.AtomPositionManager.atomPositions  for c in self.containers]
                cell        = [c.AtomPositionManager.latticeVectors for c in self.containers]

                print(" >< Making SOAP.")
                soap = SOAP_analysis(uniqueAtomLabels=self.uniqueAtomLabels,
                                     r_cut=r_cut,
                                     n_max=n_max,  
                                     l_max=l_max,
                                     sigma=sigma,
                                    )

                if params.get('cache', True):
                    soap_data = soap.verify_and_load_soap()
                    if soap_data:
                        descriptors_by_species, atom_info_by_species = soap_data
                        print("Loaded existing SOAP data.")

                    else:
                        print("Some SOAP files are missing. Recalculating...")
                        descriptors_by_species, atom_info_by_species = soap.calculate_soap_descriptors(
                                                symbols=symbols, 
                                                positions=positions, 
                                                cell=cell,)
                        soap.save_descriptors(  descriptors_by_species=descriptors_by_species, 
                                                atom_info_by_species=atom_info_by_species, 
                                                output_dir='SOAPs')
                else:
                    print("Cache disabled. Calculating SOAP descriptors...")
                    descriptors_by_species, atom_info_by_species = soap.calculate_soap_descriptors(
                                                symbols=symbols, 
                                                positions=positions, 
                                                cell=cell,)
                    soap.save_descriptors(  descriptors_by_species=descriptors_by_species, 
                                            atom_info_by_species=atom_info_by_species, 
                                            output_dir='SOAPs')

                # =========== =========== =========== =========== #
                print(" >< Compress UMAP.")
                n_components = params.get('components', 10) 
                compress_model = params.get('compress_model', 'umap') 

                compressor = Compress(unique_labels=self.uniqueAtomLabels)
                compressed_data = compressor.verify_and_load_or_compress(descriptors_by_species, method=compress_model, n_components=n_components)

                # =========== =========== =========== =========== #
                cluster_model = params.get('cluster_model', 'dbscan')
                eps, min_samples = params.get('eps', 0.7), params.get('min_samples', 2) 

                print(f" >< Cluster {cluster_model}.")
                cluster_analysis_results = {}
                for species_idx, species in enumerate(self.uniqueAtomLabels):
                    analyzer = ClusteringAnalysis()
                    cluster_analysis_results[species] = analyzer.cluster_analysis(compressed_data[species], output_dir=f'./cluster_results/{species}', use_cache=True, methods=[cluster_model])
                    print( f' Especie: {species} {cluster_model} clusters: { len(set(cluster_analysis_results[species][cluster_model]))}')

                # =========== =========== =========== =========== #
                print(" >< Linear model in cluster space.")
                structure_labels, cluster_counts, class_labels = self.generate_atom_labels_and_cluster_counts( 
                                        atom_clusters   = {key:cluster_analysis_results[key][cluster_model] for key, item in cluster_analysis_results.items()},
                                        atom_structures = {key:np.array(atom_info_by_species[key]) for key, item in atom_info_by_species.items()},
                                      )

                for specie, cluster_data in cluster_analysis_results.items():
                    for cluster_idx, (structure_idx, atom_idx) in enumerate(np.array(atom_info_by_species[specie])):
                        if type(self.containers[ structure_idx ].AtomPositionManager.class_ID) == type(None):
                            self.containers[ structure_idx ].AtomPositionManager.class_ID = np.zeros(self.containers[ structure_idx ].AtomPositionManager.atomCount)
                        self.containers[ structure_idx ].AtomPositionManager.class_ID[atom_idx] = cluster_data[cluster_model][cluster_idx]

                linear_analysis = LinearAnalysis(X=cluster_counts, y=energies)
                coefficients_cluster, predictions_cluster, residuals_cluster = linear_analysis.linear_predict(
                                        regularization = 1e-5, verbose = params.get('verbose', True), 
                                        zero_intercept = True, force_negative = False)
                linear_analysis.save_output(output_dir='linear_cluster')
                linear_analysis.analysis(output_dir='linear_cluster')

                # =========== =========== =========== =========== #
                print(" >< RBF interpretation.")
                self.plot_RBF_cluster(cutoff=r_cut, number_of_bins=100, output_path='rbf/')
                
                print(" >> Export files.")
                self.export_files(file_location=params.get('output_path', '.'), source='xyz', label='enumerate', verbose=params.get('verbose', True))

            elif abit.upper() == 'LOCAL_LINEAR':
                print("Performing Local Linear Regression analysis...")

                if params.get('opt', True):
                    print("Optimizing k value for local linear regression...")
                    params['k'], initial_errors, refined_errors, coeffs = self.find_optimal_k(
                        composition_data=composition_data,
                        verbose=params.get('verbose', False)
                    )
                    self.plot_k_convergence(
                        initial_errors,
                        refined_errors,
                        coeffs=coeffs,
                        output_path=params.get('output_path', '.')
                    )

                errors, predicted_E, composition_data, coeffs = self.n_fold_cross_validation(
                    compositions=composition_data['composition_data'],
                    energies=composition_data['energy_data'],
                    k=params['k'],
                    output_path=params.get('output_path', '.'),
                    verbose=params.get('verbose', False)
                )
                
                if params.get('output_path', False):
                    self.plot_manifold(
                        features=composition_data,
                        response=errors,
                        output_path=params.get('output_path', '.'),
                        save=True,
                        verbose=params.get('verbose', True)
                    )

            elif abit.upper() == 'GLOBAL_LINEAR':
                print("Performing Global Linear Regression analysis...")
                composition_data = self.get_composition_data()
                composition, predicted_E, coeffs = self.global_linear_predict(
                    compositions=composition_data['composition_data'],
                    energies=composition_data['energy_data'],
                    regularization=params.get('regularization', 1e-8),
                    verbose=params.get('verbose', True),
                    center=params.get('center', True)
                )
                
                if params.get('output_path', False):
                    self.plot_manifold(
                        features=composition,
                        response=composition_data['energy_data'] - predicted_E,
                        output_path=params.get('output_path', '.'),
                        save=True,
                        verbose=params.get('verbose', True)
                    )
                
                print("Global Linear Regression analysis completed.")

            elif abit.upper() == 'CLUSTER_ANALYSIS':
                print("Performing Cluster Analysis...")
                n_clusters = params.get('n_clusters', 5)
                cluster_labels, cluster_centers = self.cluster_analysis(
                    features=compositions,
                    n_clusters=n_clusters,
                    output_path=params.get('output_path', '.'),
                    save=params.get('save', True),
                    verbose=params.get('verbose', True)
                )

            elif abit.upper() == 'COMPOSITION_ENERGY_CORRELATION':
                print("Analyzing Composition-Energy Correlation...")
                correlations = self.composition_energy_correlation(
                    compositions=compositions,
                    energies=energies,
                    output_path=params.get('output_path', '.'),
                    save=params.get('save', True),
                    verbose=params.get('verbose', True)
                )

            elif abit.upper() == 'ENERGY_LANDSCAPE':
                print("Analyzing Energy Landscape...")
                self.energy_landscape_analysis(
                    compositions=compositions,
                    energies=energies,
                    output_path=params.get('output_path', '.'),
                    save=params.get('save', True),
                    verbose=params.get('verbose', True)
                )

            elif abit.upper() == 'THERMODYNAMIC_STABILITY':
                print("Predicting Thermodynamic Stability...")
                temperatures = params.get('temperatures', np.linspace(300, 1500, 50))
                stable_compositions = self.thermodynamic_stability_prediction(
                    compositions=compositions,
                    energies=energies,
                    temperatures=temperatures,
                    output_path=params.get('output_path', '.'),
                    save=params.get('save', True),
                    verbose=params.get('verbose', True)
                )

            elif abit.upper() == 'ENSEMBLE_ANALYSIS':
                print("Performing Ensemble Analysis...")
                ensemble_type = params.get('ensemble', 'canonical')
                temperatures = params.get('temperatures', np.linspace(100, 1000, 100))
                volumes = params.get('volumes', np.ones_like(energies))  # Assuming unit volume if not provided
                particles = params.get('particles', np.arange(1, len(energies) + 1))
                mass = params.get('mass', 1.0)

                ensemble_properties = self.calculate_ensemble_properties(
                    volumes=volumes,
                    temperatures=temperatures,
                    particles=particles,
                    ensemble=ensemble_type,
                    mass=mass,
                    output_path=params.get('output_path', '.'),
                    save=params.get('save', True),
                    verbose=params.get('verbose', True)
                )

        print("Ab Initio Thermodynamics analysis completed.")




