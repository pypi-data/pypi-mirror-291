from ase.calculators.aims import Aims
import re
import numpy as np


def write_control(
    c,
    write_path,
    species_dir,
    relax=False,
    bands=False,
    bands_mulliken=False,
    dos=False,
    hse06=False,
    k_grid_density=6,
    **calc_kwargs,
):
    """
    Checks and writes control.in template.
    """
    if hse06:
        xc = {"xc": "hse06 0.11", "hse_unit": "bohr", "hybrid_xc_coeff": 0.25}
        if bands:
            xc["exx_band_structure_version"] = "1"
        calc_kwargs.update(**xc)
    elif not "xc" in calc_kwargs:
        calc_kwargs.update({"xc": "pbe"})

    if not "relativistic" in calc_kwargs:
        calc_kwargs.update({"relativistic": "atomic_zora scalar"})

    calc = Aims(species_dir=species_dir, **calc_kwargs)

    is_periodic = all(c.pbc)
    needs_spin = np.any(c.get_initial_magnetic_moments())
    c_file = write_path / "control.in"

    if c_file.exists():
        print("-- Found control.in file")
        needs_xc, needs_ks, needs_species_default = check_control(is_periodic, c_file)
        # print(needs_xc, needs_ks, needs_species_default)
        if needs_species_default:
            print("-- Found control.in, but no species: Only attaching species")
            calc.write_species(c, c_file.as_posix())
        else:
            print("-- Not attaching species_default (found some)")
        if needs_xc:
            print("-- Warning: Found control.in, but no xc flag")
        if needs_ks:
            print("-- Warning: Found control.in, but no k_grid or k_grid_density flag")
    else:
        print("-- Creating new control.in file.")
        output = []
        if is_periodic:
            r_lattice = np.linalg.norm(2.0 * np.pi * c.cell.reciprocal(), axis=1)
            if not "k_grid" in calc_kwargs or "k_grid_density" in calc_kwargs:
                k_grid = tuple(np.ceil(r_lattice * k_grid_density).astype(int))
                calc.set(k_grid=k_grid)
        if relax:
            calc.set(relax_geometry="trm 5e-3")
            if is_periodic:
                calc.set(relax_unit_cell="full")
        if dos:
            output += [
                "dos -20 10 15001 0.05",
                "species_proj_dos -20 10 15001 0.05",
            ]
            if is_periodic:
                calc.set(dos_kgrid_factors="3 3 3")
        if bands or bands_mulliken and is_periodic:
            print(f"-- Bravais Lattice: {c.cell.get_bravais_lattice().longname}")
            print(f"  {c.cell.get_bravais_lattice().description()}")
            bands = prepare_bandinput(c.get_cell(), bands_mulliken=bands_mulliken)
            output += bands
        if output:
            calc.set(output=output)
        if needs_spin:
            calc.set(spin="collinear")
        calc.write_control(c, c_file.as_posix())
        calc.write_species(c, c_file.as_posix())


def prepare_bandinput(cell, density=35, bands_mulliken=False):
    """
    Prepares the band information needed for the FHI-aims control.in file.

    Parameters:

    max_points_per_path: int
        Number of kpoints per band path
    density: int
        Number of kpoints per Angstrom. Default: 35
    """
    from ase.dft.kpoints import resolve_kpt_path_string, kpoint_convert

    bp = cell.bandpath()
    # print(cell.get_bravais_lattice())
    r_kpts = resolve_kpt_path_string(bp.path, bp.special_points)
    band_string = "band"
    if bands_mulliken:
        band_string = "band_mulliken"
    linesAndLabels = []
    for labels, coords in zip(*r_kpts):
        dists = coords[1:] - coords[:-1]
        lengths = [np.linalg.norm(d) for d in kpoint_convert(cell, skpts_kc=dists)]
        points = np.int_(np.round(np.asarray(lengths) * density))
        # I store it here for now. Might be needed to get global info.
        linesAndLabels.append([points, labels[:-1], labels[1:], coords[:-1], coords[1:]])

    bands = []
    for segs in linesAndLabels:
        for points, lstart, lend, start, end in zip(*segs):
            points = max(points, 2)
            bands.append(
                "{} {:9.5f}{:9.5f}{:9.5f} {:9.5f}{:9.5f}{:9.5f} {:4} {:3}{:3}".format(
                    band_string, *start, *end, points, lstart, lend
                )
            )

    # print(bands)
    return bands


def check_control(is_periodic, control_filename):

    with open(control_filename, "r") as fd:
        control_file = fd.read()
    needs_xc = not bool(re.search(r"\s*xc\s+.+", control_file))
    needs_ks = (
        not bool(re.search(r"\s*(k_grid|k_grid_density)\s+.+\n", control_file)) and is_periodic
    )
    needs_species_default = not bool(re.search(r"\#  FHI\-aims code project", control_file))

    return needs_xc, needs_ks, needs_species_default
