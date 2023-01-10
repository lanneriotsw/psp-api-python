# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os.path
import sys
from datetime import datetime
from pathlib import Path

import toml

# sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
config = toml.load(Path(__file__).parent / '..' / 'pyproject.toml')
info = config['project']
from lannerpsp import __version__
info['version'] = __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = info['name']
author = info['authors'][0]['name']
project_copyright = f'{datetime.now():%Y}, Lanner Electronics Inc'
version = info['version']
release = info['version']

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.intersphinx']

source_suffix = '.rst'
# source_encoding = 'utf-8-sig'
exclude_patterns = ['_build']
templates_path = ['_templates']
# default_role = None
# keep_warnings = False
# today_fmt = '%B %d, %Y'
highlight_language = 'python3'
pygments_style = 'sphinx'
# add_function_parentheses = True
# add_module_names = True
# show_authors = False

# -- Autodoc configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

autodoc_member_order = 'bysource'

# -- Intersphinx configuration -----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for internationalization ----------------------------------------

# language = 'zh_TW'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# html_theme_path = []
html_title = f'{info["name"]} {info["version"]} Documentation'
# html_short_title = None
html_logo = 'logo.svg'
html_favicon = 'favicon.ico'
html_static_path = ['_static']
# html_extra_path = []
# html_last_updated_fmt = '%b %d, %Y'
# html_use_smartypants = True
# html_additional_pages = {}
# html_domain_indices = True
# html_use_index = True
# html_split_index = False
# html_show_sourcelink = True
# html_use_opensearch = ''
# html_file_suffix = None
# html_show_copyright = True
# html_show_sphinx = True
