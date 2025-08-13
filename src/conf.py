# Configuration file for the Sphinx documentation builder.

import sys
import os
import pathlib

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('../boolevard'))

# -- Project information -----------------------------------------------------
project = 'BooLEVARD'
copyright = '2025, Marco Fariñas'
author = 'Marco Fariñas, Eirini Tsirvouli, John Zobolas, Tero Aittokallio, Åsmund Flobak, Kaisa Lehti'
release = '0.1.1'
version = '0.1.1'
repository_url = 'https://github.com/farinasm/boolevard'
html_logo = 'https://raw.githubusercontent.com/farinasm/boolevard/main/src/Logo_white.png'
html_favicon = 'https://raw.githubusercontent.com/farinasm/boolevard/main/src/icon.png'
html_theme_options = {
    "logo_only": True,
    "display_version": True,
}

# Automatically generate index from README if exists
readme = pathlib.Path().absolute().parents[1].joinpath('README.rst')

if readme.exists():
    with readme.open('r') as f:
        readme_lines = f.readlines()

    with open('index.rst', 'w') as f:
        f.write('==================\n BooLEVARD \n==================\n\n')
        f.write(''.join(readme_lines))

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'nbsphinx',
    'sphinx.ext.imgconverter'
]

autosummary_generate = True
autodoc_member_order = 'groupwise'
default_role = 'literal'


templates_path = ['_templates']

source_suffix = '.rst'

# -- Autodoc configuration ---------------------------------------------------
autodoc_mock_imports = []  # Add mock imports here if needed
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "inherited-members": True,
    "private-members": True,
    "special-members": "__init__",
    "exclude-members": "__weakref__",
}

napoleon_google_docstring = True
napoleon_numpy_docstring = True  # Ensure full NumPy-style docstrings are parsed
napoleon_include_init_with_doc = True  # Ensure __init__ docstrings are included
napoleon_use_rtype = False  # Avoid redundant "Returns" section in output


# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']


master_doc = 'index'
