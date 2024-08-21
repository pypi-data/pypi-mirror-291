# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wraiter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wraiter',
    'version': '0.0.1',
    'description': 'Wraiter.',
    'long_description': '# Wraiter',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele.dallachiesa@sigforge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/elehcimd/wraiter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10.0,<3.13.0',
}


setup(**setup_kwargs)
