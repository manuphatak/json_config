# -*- coding: utf-8 -*-
import sys
from os.path import abspath, relpath

import sphinx.environment
from docutils.utils import get_source_line


def _warn_node(func):
    suppressed_urls = ['https://travis-ci.org/', 'https://pypip.in/,',
                       'https://coveralls.io/', 'https://readthedcs.org/']
    suppressed_urls = map('nonlocal image URI found: {}'.format, suppressed_urls)
    # TODO debug this.
    def wrapper(self, msg, node):
        if not msg.startswith('nonlocal image URI found:'):
            return func(self, msg, node)

    return wrapper


sphinx.environment.BuildEnvironment.warn_node = _warn_node(sphinx.environment.BuildEnvironment.warn_node)

sys.path.insert(0, abspath(relpath('../', __file__)))

import json_config

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo',
              'sphinx.ext.coverage', 'sphinx.ext.viewcode', ]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'JSON Config'
copyright = u'2015, Manu Phatak'
author = json_config.__author__
version = json_config.__version__
release = json_config.__version__
language = None

today = 'today'
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

todo_include_todos = True

viewcode_import = True
# -- Options for HTML output ----------------------------------------------

html_theme = 'sphinx_rtd_theme'
# html_theme_options = {}
# html_theme_path = []
# html_title = None
# html_logo = None
# html_short_title = None
# html_favicon = None
html_static_path = ['_static']
# html_extra_path = []
# html_last_updated_fmt = '%b %d, %Y'
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
# 'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
# 'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'JSONConfigdoc'

# -- Options for LaTeX output ---------------------------------------------

# latex_elements = {
# # The paper size ('letterpaper' or 'a4paper').
# # 'papersize': 'letterpaper',
#
# # The font size ('10pt', '11pt' or '12pt').
#     # 'pointsize': '10pt',
#
#     # Additional stuff for the LaTeX preamble.
#     # 'preamble': '',
#
#     # Latex figure (float) alignment
#     # 'figure_align': 'htbp',}
# }

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [(master_doc, 'JSONConfig.tex', u'JSON Config Documentation',
                    u'Manu Phatak', 'manual'), ]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, 'jsonconfig', u'JSON Config Documentation', [author], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [(master_doc, 'JSONConfig', u'JSON Config Documentation', author,
                      'JSONConfig', 'One line description of project.',
                      'Miscellaneous'), ]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False


