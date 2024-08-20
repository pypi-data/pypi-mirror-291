import click
import numpy as np
from ase.io import read
from clims.phonopy_interface import initialize_phonopy, post_process_phonopy


@click.group()
def clims_phonopy():
    """
    Simple rapper around phonopy for FHI-aims.
    """


@clims_phonopy.command()
@click.option("--displacement", default=0.01, help="Displacement of atoms (AA).")
@click.option("--supercell", help="Supercell matrix (9 elements)", nargs=9)
@click.option("--filein", help="Input geometry file", default="geometry.in")
def initialize(displacement, supercell, filein):
    """
    Generate geometries with displaced atoms needed
    for the finite difference calculation of phonons DOS.
    """
    supercell_matrix = np.array([int(x) for x in supercell]).reshape((3, 3))
    structure = read(filein)
    initialize_phonopy(structure, supercell_matrix=supercell_matrix, displacement=displacement)


@clims_phonopy.command()
@click.option(
    "--mesh", default=[20, 20, 20], help="q-point mesh for phonopy", nargs=3, type=int
)
@click.option(
    "--outfile",
    default="aims.out",
    help="FHI-aims output file. All files should have the same name in the subfolders",
)
@click.option("--show", is_flag=True, help="Show the DOS.")
def postprocess(mesh, outfile, show):
    """
    Post-processing the calculated forces to obtain the phonon DOS.
    """
    post_process_phonopy(mesh=mesh, outfile=outfile, show=show)
