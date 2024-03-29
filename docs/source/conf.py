# Configuration file for the Sphinx reference builder.
#
# This file only contains a selection of the most common options. For a full
# list see the reference:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# reference root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../../"))


# -- Project information -----------------------------------------------------

project = "automatic-spike-detection"
copyright = "2024, Dominik Frey"
author = "Dominik Frey"

# The full version, including alpha/beta/rc tags
release = "1.2.6"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "numpydoc",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# master_doc = "index"

# -- numpydoc configuration --------------------------------------------------
numpydoc_show_class_members = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the reference for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_title = f"automatic-spike-detection {release}"

# html_sidebars = {"**": ["search-field.html"]}

# Configuration of sphinx.ext.coverage
coverage_show_missing_items = True

numfig = True
