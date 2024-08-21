# -*- coding: utf-8 -*-
"""
Setup file for hydesign
"""
import os
from setuptools import setup, find_packages

repo = os.path.dirname(__file__)



try:
    from pypandoc import convert_file

    def read_md(f): return convert_file(f, 'rst', format='md')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")



setup(name='dtu_adn',
      version= '0.0.1',
      description='A library of realistic multi-voltage distribution network dataset',
      url='https://gitlab.windenergy.dtu.dk/aeish/DTU_ADN_Base_Directory.git',
      author='Aeishwarya Baviskar',
      author_email='aeish@dtu.dk',
      license='MIT',
      packages=find_packages(),
      package_data={
          'dtu_adn': [
            '.\\data\\network_10kV_400V\\*.csv',
            '.\\data\\network_10kV_400V\\load_and_gen_type\\*.csv',
            '.\\data\\network_60kV\\*.csv',
            '.\\data\\timeseries_400V\\*.csv',
            '.\\data\\timeseries_aggregated_10kV\\*.csv',
            ],},
      install_requires=[
          'pypower',
          'numpy',
          'pandas',
          'openpyxl',
          'scipy',
          ],
      extras_require={},
      include_package_data=True,
      zip_safe=True)
