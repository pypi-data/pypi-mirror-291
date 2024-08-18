# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['suricat']

package_data = \
{'': ['*'], 'suricat': ['cabs/*']}

install_requires = \
['astro-tigger-lsm',
 'astropy',
 'click',
 'matplotlib',
 'numpy',
 'scipy',
 'stimela>=2.0,<3.0',
 'suricat-beams-cabs',
 'xarray-fits']

entry_points = \
{'console_scripts': ['suricat = suricat.main:cli']}

setup_kwargs = {
    'name': 'suricat-beams',
    'version': '0.0.2',
    'description': 'MeerKAT primary beam model handling utilities',
    'long_description': '# suricat-beams\nMeerKAT primary beam model handling utilities\n\nSee https://doi.org/10.48479/wdb0-h061 for documentation on beam models. \n\nThe utilities can download the models for you automatically, see suricat.yml Stimela recipe.',
    'author': 'Oleg Smirnov',
    'author_email': 'osmirnov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
