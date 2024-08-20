from __future__ import annotations
import copy

import pandas as pd
import typing
import numpy as np
import jax.numpy as jnp
import gemmi
import bfastor
import pathlib
import warnings

ATOMIC_MASSES = {"H": 1, "C": 12, "N": 14, "O": 16, "P": 30, "S": 32}


def read_model(
    filename,
    hetatm=False,
    water=False,
):
    structure = gemmi.read_structure(str(filename))
    structure.add_entity_types()
    if not hetatm:
        structure.remove_ligands_and_waters()
        if water:
            warnings.warn(
                f"Waters removed from model {structure.name}, to keep "
                f"waters set hetatm=True",
                category=RuntimeWarning,
                stacklevel=1,
            )
    if not water:
        structure.remove_waters()

    groups = gemmi.MmcifOutputGroups(True)
    data = structure.make_mmcif_block(groups)
    header = {}
    atom_data = {}
    for name in data.get_mmcif_category_names():
        if name == "_atom_site.":
            atom_data = data.get_mmcif_category(name, raw=True)
        else:
            header[name] = data.get_mmcif_category(name, raw=True)

    return Structure.from_dict(
        atom_data,
        filename=filename,
        header=header,
    )


class Structure:
    column_names = {
        "Cartn_x": "x",
        "Cartn_y": "y",
        "Cartn_z": "z",
        "B_iso_or_equiv": "temp_fac",
        "group_PDB": "record_name",
        "auth_asym_id": "chain",
        "auth_seq_id": "res_no",
        "label_atom_id": "atom_name",
        "type_symbol": "element",
    }
    primary_ids = {
        "label_asym_id": "chain",
        "label_seq_id": "res_no",
        "label_atom_id": "atom_name",
        "label_comp_id": "res",
    }

    def __init__(
        self,
        atoms_dataframe: pd.DataFrame,
        filename: typing.AnyStr = "",
        header: typing.Union[typing.Dict, None] = None,
    ):
        """
        Arguments:
            atoms_dataframe: pd.DataFrame containing the atom_site information. Each key should be
                a header name in mmcif format and values should be a list of a given param for
                all atoms.
            filename: The path to the file containing the model, if it was read from disk.
                Default: empty string.
            header: Dictionary containing additional information. Each key should be the name of
                a mmcif table or list of label/data pairs. Default: None
        Returns:
            A Structure object.
        """

        self.data = pd.DataFrame(atoms_dataframe).rename(columns=self.column_names)
        self.filename = filename
        self.header = header
        self.set_mass_column()
        self.data = self.data.astype(
            {
                "x": float,
                "y": float,
                "z": float,
                "temp_fac": float,
                "mass": float,
            }
        )

        self._using_primary_identifiers = False

    @classmethod
    def from_dict(
        cls,
        atom_dict: typing.Dict,
        filename: typing.AnyStr = "",
        header: typing.Dict = None,
    ) -> Structure:
        """Generate a TEMPy structure object from atom_site information in a
        dictionary

        Arguments:
            atom_dict: Dictionary containing the atom_site information. Each key should be
                a header name in mmcif format and values should be a list of a given param for
                all atoms.
            filename: The path to the file containing the model, if it was read from disk.
                Default: empty string.
            header: Dictionary containing additional information. Each key should be the name of
                a mmcif table or list of label/data pairs. Default: None

        Returns:
            A TEMPy Structure object.
        """

        df = pd.DataFrame.from_dict(atom_dict)
        df = df.rename(columns=cls.column_names)
        df = df.astype({"x": "float64", "y": "float64", "z": "float64"})

        return cls(df, filename=filename, header=header)

    @classmethod
    def from_gemmi_structure(
        cls,
        gemmi_structure: gemmi.Structure,
    ) -> Structure:
        """Generate a TEMPy structure object from a gemmi.Structure object

        Arguments:
            gemmi_structure: A gemmi.Structure object.
        Returns:
            A TEMPy Structure object
        """
        groups = gemmi.MmcifOutputGroups(True)
        data = gemmi_structure.make_mmcif_block(groups)
        header = {}
        atom_data = {}
        for name in data.get_mmcif_category_names():
            if name == "_atom_site.":
                atom_data = data.get_mmcif_category(name, raw=True)
            else:
                header[name] = data.get_mmcif_category(name, raw=True)

        return cls.from_dict(atom_data, filename="Unknown", header=header)

    @classmethod
    def from_file(
        cls,
        filename,
        hetatm=True,
        water=True,
    ):
        return read_model(filename, hetatm, water)

    @property
    def pdb_id(self):
        try:
            return self.header["_entry."]["id"][0]
        except (KeyError, TypeError):  # id not in header dict or header is None
            return "Unknown"

    @property
    def num_chains(self):
        return pd.unique(self.get_column_data("chain")).size

    @property
    def num_residues(self):
        n = 0
        for c in self.get_chain_names():
            n += pd.unique(self.get_chain(c).get_column_data("res_no")).size
        return n

    @property
    def num_atoms(self):
        return self.data.shape[0]

    def __len__(self):
        return self.num_atoms

    def __repr__(self):
        s = (
            f"{self.pdb_id} model containing {self.num_residues} residues, "
            f"in {self.num_chains} chains"
        )
        if self.filename != "":
            s = s + f" from file {self.filename}"

        return s

    def to_dict(self, use_mmcif_labels=True) -> typing.Dict:
        """ """
        if use_mmcif_labels:
            data = self.get_data_with_mmcif_labels()
        else:
            data = self.data
        d = self.header.copy()
        d["atom_site."] = data.to_dict(orient="list")

        return d

    def get_columns(
        self, column_labels: typing.Union[typing.List[str], str]
    ) -> pd.DataFrame:
        """Return a pd.DataFrame containing the specified columns from the Structure
        object.

        Arguments:
            column_labels:
        """
        return self.data.loc[:, column_labels]

    def get_column_data(
        self, column_labels: typing.Union[typing.List[str], str]
    ) -> np.ndarray:
        """Return a specified column as a np.ndarray"""
        return self.data.loc[:, column_labels].values

    def get_chain(self, chain_label: str) -> bfastor.models.Structure:
        return Structure(
            self.get_rows_by_column_values("chain", chain_label), filename=self.filename
        )

    def set_columns(
        self,
        labels: typing.Union[typing.List[str], str],
        data: typing.Union[np.ndarray, jnp.ndarray],
    ):
        """Set the values of specified columns.

        Arguments:
            labels: List of column labels
            data: 2D np.ndarray with shape (K, N) where K is len(labels)
                and N is the number of atoms in the structure
        """
        self.data[labels] = data

    def set_column_by_row_value(self, column_label, value_dict):
        """ """
        # Todo: Check this function is not setting values to a copy of dataframe
        col = self.get_column_data(column_label)
        for n in range(len(col)):
            try:
                col[n] = value_dict[col[n]]
            except KeyError:
                continue
        self.set_columns(column_label, col)

    def get_rows_by_column_values(
        self,
        column_label: typing.Union[typing.List[str], str],
        column_value: typing.Any,
    ) -> pd.DataFrame:
        """Returns a pd.Dataframe of rows that contain a specified value
        from a specified column

        Arguments:
            column_label: The label of a given column, e.g. "chain"
            column_value: The value that should be matched
        Returns:
            pd.Dataframe containing the selected rows
        """
        return self.data.loc[self.data[column_label] == column_value, :]

    def copy(self) -> Structure:
        """Return a copy of the Structure instance"""
        return copy.deepcopy(self)

    def set_mass_column(self):
        # use weird numpy indexing to quickly set masses into an array
        # taken from https://stackoverflow.com/questions/16992713
        if "mass" in self.data.columns:
            pass
        else:
            elements = self.get_columns("element")
            uniques, indices = np.unique(elements, return_inverse=True)
            masses = np.array([ATOMIC_MASSES[x] for x in uniques])[indices]

            self.data["mass"] = masses

    def get_data_with_mmcif_labels(self):
        """Sets the masses for each atom in the Structure."""
        reversed_dict = {v: k for k, v in self.column_names.items()}

        if self._using_primary_identifiers:
            reversed_primary_dict = {v: k for k, v in self.primary_ids.items()}
            data = self.data.rename(columns=reversed_primary_dict)
        else:
            data = self.data.rename(columns=reversed_dict)

        return data

    def _assign_column_at_value(
        self, column_label: str, old_value: typing.Any, new_value: typing.Any
    ):
        self.data.loc[self.data[column_label] == old_value, column_label] = new_value

    def get_gemmi_block(self) -> gemmi.cif.Block:
        """Returns a gemmi.cif.Block containing the Structures information."""
        block = gemmi.cif.Block(self.pdb_id)
        # add header info to the block
        for k, v in self.to_dict(use_mmcif_labels=True).items():
            try:
                block.set_mmcif_category(f"_{k}", v, raw=True)
            except ValueError:  # occurs due to empty header info
                continue
        return block

    def to_gemmi_structure(self) -> gemmi.Structure:
        """Returns a gemmi.Structure object"""
        block = self.get_gemmi_block()
        s = gemmi.make_structure_from_block(block)
        s.setup_entities()
        s.renumber_models()
        return s

    def write_pdb(self, filename: typing.Union[pathlib.Path, str], **kwargs):
        """Write a pdb file for the Structure instance

        Arguments:
            filename: location to save the output pdb file
        """
        s = self.to_gemmi_structure()
        s.write_pdb(str(filename), **kwargs)

    def write_mmcif(self, filename):
        """ """
        b = self.get_gemmi_block()
        b.write_file(filename, style=gemmi.cif.Style.Aligned)

    def get_chain_names(self) -> typing.List[str]:
        """Get a list of all the chain names in the Structure instance"""
        return pd.unique(self.get_column_data("chain")).tolist()


def remove_hydrogens(model: Structure):
    new_data = model.data.loc[model.data["element"] != "H", :]
    return Structure(new_data, filename=model.filename, header=model.header)
