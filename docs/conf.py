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
release = '0.1.0'
repository_url = 'https://github.com/farinasm/boolevard'

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
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'nbsphinx',
    'IPython.sphinxext.ipython_console_highlighting'
]

autosummary_generate = True
autodoc_member_order = 'groupwise'
default_role = 'literal'

# NumPy docstring conventions
napoleon_google_docstring = True
napoleon_numpy_docstring = True
numpydoc_show_class_members = False  # don't show class members in both class and __init__ docstrings
napoleon_include_init_with_doc = False
napoleon_use_rtype = True
napoleon_use_param = True
nbsphinx_execute = 'never'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

source_suffix = '.rst'

# -- Autodoc configuration ---------------------------------------------------
autodoc_mock_imports = []  # Add mock imports here if needed

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'

html_theme_options = dict(
    logo_only=True,
    display_version=True
)

html_context = {
    'display_github': True,  # Integrate GitHub
    'github_user': 'farinasm',  # Username
    'github_repo': project,  # Repo name
    'github_version': 'main',  # Version
    'conf_py_path': '/docs/',  # Path in the checkout to the docs root
}

html_static_path = ['_static']

