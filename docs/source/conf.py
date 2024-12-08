# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'BreakYourLLM'
copyright = '2024, ModelPulse'
author = 'ModelPulse'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
extensions = [
    'sphinx.ext.autodoc',     # Optional but not required with autoapi
    'sphinx.ext.napoleon',    # For Google/NumPy-style docstrings
    'myst_parser',            # For Markdown support
    'autoapi.extension',      # Use autoapi
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# myst_enable_extensions = [
#     "colon_fence",   # Use ::: for block directives
#     "linkify",       # Automatically detect links
#     "substitution",  # Support text substitutions
# ]

master_doc = 'index'  # If still 'index.md', no changes needed

# Point to your Python source code
autoapi_dirs = ['../../sources']

# Set the output format to MyST Markdown
autoapi_keep_files = True  # Keep generated Markdown files

myst_enable_extensions = ['amsmath', 'colon_fence']  
