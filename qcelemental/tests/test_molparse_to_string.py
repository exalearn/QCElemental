import pytest
import qcelemental
from qcelemental.testing import compare

_results = {
"subject1": """
3 au

Co 0 0 0
H  2 0 0
h_OTher -2 0 0
""",

"ans1_au": """3 au
CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
H                     2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
""",

"ans1_ang": """3
CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
H                     1.058354421340     0.000000000000     0.000000000000
H                    -1.058354421340     0.000000000000     0.000000000000
""",

"ans1c_ang": """3
CoH2
59Co                      0.00000000         0.00000000         0.00000000
1H                        1.05835442         0.00000000         0.00000000
1H_other                 -1.05835442         0.00000000         0.00000000
""",

"ans1c_nm": """3 nm
CoH2
59Co                      0.00000000         0.00000000         0.00000000
1H                        0.10583544         0.00000000         0.00000000
1H_other                 -0.10583544         0.00000000         0.00000000
""",

"subject2": """
Co 0 0 0
no_reorient
--
@H  1.05835442134 0 0
h_OTher -1.05835442134 0 0
""",

"ans2_au": """3 au
CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
@H                    2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
""",

"ans2_ang": """3
CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
Gh(1)                 1.058354421340     0.000000000000     0.000000000000
H                    -1.058354421340     0.000000000000     0.000000000000
""",

"ans2c_ang": """2
CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
H                    -1.058354421340     0.000000000000     0.000000000000
""",

"ans2_cfour_ang": """auto-generated by QCElemental from molecule CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
GH                    1.058354421340     0.000000000000     0.000000000000
H                    -1.058354421340     0.000000000000     0.000000000000
""",

"ans2_nwchem_ang": """geometry units angstroms
Co                    0.000000000000     0.000000000000     0.000000000000
GH                    1.058354421340     0.000000000000     0.000000000000
H                    -1.058354421340     0.000000000000     0.000000000000

end
""",

"ans2_terachem_au": """3 au
CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
XH                    2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
""",

"ans2_terachem_ang": """3
CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
XH                    1.058354421340     0.000000000000     0.000000000000
H                    -1.058354421340     0.000000000000     0.000000000000
""",
}  # yapf: disable


@pytest.mark.parametrize("inp,expected", [
    (("subject1", {'dtype': 'xyz', 'units': 'Bohr'}), "ans1_au"),
    (("subject1", {'dtype': 'xyz', 'units': 'Angstrom'}), "ans1_ang"),
    (("subject1", {'dtype': 'xyz', 'prec': 8, 'atom_format': '{elea}{elem}{elbl}'}), "ans1c_ang"),
    (("subject2", {'dtype': 'xyz', 'units': 'Bohr'}), "ans2_au"),
    (("subject2", {'dtype': 'xyz', 'units': 'Angstrom', 'ghost_format': 'Gh({elez})'}), "ans2_ang"),
    (("subject2", {'dtype': 'xyz', 'units': 'angstrom', 'ghost_format': ''}), "ans2c_ang"),
    (("subject2", {'dtype': 'cfour'}), "ans2_cfour_ang"),
    (("subject2", {'dtype': 'nwchem'}), "ans2_nwchem_ang"),
    (("subject1", {'dtype': 'xyz', 'units': 'nm', 'prec': 8, 'atom_format': '{elea}{elem}{elbl}'}), "ans1c_nm"),
    (("subject2", {'dtype': 'terachem'}), "ans2_terachem_ang"),
    (("subject2", {'dtype': 'terachem', 'units': 'bohr'}), "ans2_terachem_au"),
])  # yapf: disable
def test_to_string_xyz(inp, expected):
    molrec = qcelemental.molparse.from_string(_results[inp[0]])
    smol = qcelemental.molparse.to_string(molrec['qm'], **inp[1])

    assert compare(_results[expected], smol)


@pytest.mark.parametrize("inp", [
    ("subject1", {'dtype': 'xyz', 'units': 'kg', 'prec': 8, 'atom_format': '{elea}{elem}{elbl}'}),
])  # yapf: disable
def test_to_string_error(inp):
    import pint
    molrec = qcelemental.molparse.from_string(_results[inp[0]])

    with pytest.raises(pint.errors.DimensionalityError):
        qcelemental.molparse.to_string(molrec['qm'], **inp[1])
