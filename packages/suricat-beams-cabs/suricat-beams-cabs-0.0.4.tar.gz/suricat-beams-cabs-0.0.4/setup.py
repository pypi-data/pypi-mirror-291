# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['suricat']

package_data = \
{'': ['*'], 'suricat': ['cabs/*']}

install_requires = \
['stimela>=2.0,<3.0']

setup_kwargs = {
    'name': 'suricat-beams-cabs',
    'version': '0.0.4',
    'description': 'MeerKAT primary beam model handling utilities -- Stimela cabs',
    'long_description': '# suricat-beams-cabs\nMeerKAT primary beam model handling utilities -- Stimela cab definitions\n\nSee https://doi.org/10.48479/wdb0-h061 for documentation on beam models. \n\nThe utilities can download the models for you automatically, see suricat.yml Stimela cab.',
    'author': 'Oleg Smirnov',
    'author_email': 'osmirnov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
