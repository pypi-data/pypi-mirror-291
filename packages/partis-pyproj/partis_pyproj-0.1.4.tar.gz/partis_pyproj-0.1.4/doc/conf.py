# -*- coding: utf-8 -*-

from partis.utils.sphinx import basic_conf

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# configuration
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

globals().update( basic_conf(
  package = 'partis-pyproj',
  copyright_year = '2022' ) )

intersphinx_mapping['packaging'] = ("https://packaging.pypa.io/en/latest/", None)
