import json

def write_notebook(path, title, theory_md, code_content):
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {title}\n",
                    "\n",
                    theory_md
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code_content.splitlines(True)
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

# 05_phonons
write_notebook("05_phonons/quantum_oscillator.ipynb", "Quantum Oscillator", "## Theory\nQuantized energies.", "# To be filled")
write_notebook("05_phonons/bose_statistics.ipynb", "Bose Statistics", "## Theory\nPhonon occupation.", "# To be filled")
write_notebook("05_phonons/heat_capacity.ipynb", "Heat Capacity", "## Theory\nEinstein/Debye models.", "# To be filled")

# 06_defects & 07_disorder
write_notebook("05_defects/single_defect.ipynb", "Single Defect", "## Theory\nLocalized impurity mode.", "# To be filled")
write_notebook("05_defects/localized_modes.ipynb", "Localized Modes", "## Theory\nDecay length.", "# To be filled")
write_notebook("05_defects/scattering.ipynb", "Scattering", "## Theory\nTransmission/reflection.", "# To be filled")
write_notebook("06_disorder/random_chains.ipynb", "Random Chains", "## Theory\nDisordered masses.", "# To be filled")
write_notebook("06_disorder/anderson_localization.ipynb", "Anderson Localization", "## Theory\nExponential localization.", "# To be filled")

