# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certificate_cli']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=3.0.3,<4.0.0',
 'cryptography>=43.0.0,<44.0.0',
 'typer[all]>=0.12.4,<0.13.0']

entry_points = \
{'console_scripts': ['certificate_cli = certificate_cli.main:start_cli']}

setup_kwargs = {
    'name': 'certificate-cli',
    'version': '0.2.1',
    'description': '',
    'long_description': '',
    'author': 'Ben Davidson',
    'author_email': 'ben.davidson@dynatrace.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
