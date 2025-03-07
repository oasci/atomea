"""Processing AMBER simulations with roGFP2"""

import os
import shutil

import numpy as np
import zarr

from atomea.digesters import MDAnalysisDigester
from atomea.io.backends._zarr import ZarrManager

from .conftest import TMP_DIR


def test_digest_amber_rogfp2_serial(amber_rogfp2_sim_paths):
    """
    Test the digestion of Amber simulations using the roGFP2 ensemble.

    This test function verifies the correct digestion of Amber simulations
    using the roGFP2 ensemble. It uses the `EnsembleSchema` class to store
    the ensemble data and the `MDAnalysisDigester` class to perform the
    digestion. The digestion is performed by passing the necessary input
    files, such as the topology file and the trajectory file, to the digester.
    """
    digester = MDAnalysisDigester()
    digester_args = (
        amber_rogfp2_sim_paths["mol.prmtop"],
        amber_rogfp2_sim_paths["07_relax_npt.nc"],
    )
    digester_kwargs = {"topology_format": "PRMTOP", "format": "NC"}
    ensemble_data = digester.digest(
        digester_args=digester_args, digester_kwargs=digester_kwargs
    )
    assert ensemble_data.system.coordinates is not None
    assert ensemble_data.system.coordinates.shape[0] == 100
    assert np.allclose(ensemble_data.system.coordinates[0][0][0], 33.924496)
    assert np.allclose(ensemble_data.system.coordinates[0][32][0], 27.2496)
    assert np.allclose(ensemble_data.system.coordinates[-1][78][0], 29.406982)

    assert ensemble_data.system.atom_symbol is not None
    assert ensemble_data.system.atom_symbol[0] == "N"
    assert ensemble_data.system.atom_symbol[8324] == "H"
    assert ensemble_data.system.atom_symbol[-1] == "H"

    assert ensemble_data.topology.ff_atom_type is not None
    assert ensemble_data.topology.ff_atom_type[0] == "N3"


def test_digest_write_amber_rogfp2_serial(amber_rogfp2_sim_paths):
    digester = MDAnalysisDigester()
    digester_args = (
        amber_rogfp2_sim_paths["mol.prmtop"],
        amber_rogfp2_sim_paths["07_relax_npt.nc"],
    )
    digester_kwargs = {"topology_format": "PRMTOP", "format": "NC"}
    digest_kwargs = {"digester_args": digester_args, "digester_kwargs": digester_kwargs}
    storage_path = os.path.join(TMP_DIR, "amber_rogfp2_serial.zarr")
    if os.path.exists(storage_path):
        shutil.rmtree(storage_path)
    storage_manager = ZarrManager()

    store = storage_manager.digest_and_store(digester, digest_kwargs, storage_path)

    coordinates = zarr.open_array(store=store, path="/system/coordinates")
    assert np.allclose(coordinates.get_basic_selection((0, 0, 0)), 33.924496)
    assert np.allclose(coordinates.get_basic_selection((0, 32, 0)), 27.2496)
    assert np.allclose(coordinates.get_basic_selection((-1, 78, 0)), 29.406982)
