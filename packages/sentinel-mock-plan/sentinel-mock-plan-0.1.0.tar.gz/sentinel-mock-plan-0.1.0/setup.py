# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentinel_mock_plan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sentinel-mock-plan',
    'version': '0.1.0',
    'description': 'Create a mock plan for Hashicorp Sentinel 0.26.2',
    'long_description': '# TODO\n\n',
    'author': 'Amine Laabi',
    'author_email': 'amine.laabi@outlook.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.12,<4.0',
}


setup(**setup_kwargs)
