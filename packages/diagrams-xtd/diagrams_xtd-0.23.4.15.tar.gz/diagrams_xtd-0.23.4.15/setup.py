# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diagrams_xtd',
 'diagrams_xtd.alibabacloud',
 'diagrams_xtd.aws',
 'diagrams_xtd.azure',
 'diagrams_xtd.base',
 'diagrams_xtd.c4',
 'diagrams_xtd.custom',
 'diagrams_xtd.digitalocean',
 'diagrams_xtd.elastic',
 'diagrams_xtd.firebase',
 'diagrams_xtd.gcp',
 'diagrams_xtd.generic',
 'diagrams_xtd.ibm',
 'diagrams_xtd.k8s',
 'diagrams_xtd.oci',
 'diagrams_xtd.onprem',
 'diagrams_xtd.openstack',
 'diagrams_xtd.outscale',
 'diagrams_xtd.programming',
 'diagrams_xtd.saas']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.13.2,<0.21.0', 'jinja2>=2.10,<4.0']

extras_require = \
{':python_version < "3.8"': ['typed-ast>=1.5.5,<2.0.0']}

entry_points = \
{'console_scripts': ['diagrams = diagrams_xtd.cli:main']}

setup_kwargs = {
    'name': 'diagrams_xtd',
    'version': '0.23.4.15',
    'description': 'Extended version of diagrams',
    'long_description': '# diagrams-xtd\nExtended version of diagrams with some PR that never get merged and I want to use.\n\nMore details in [CHANGELOG](CHANGELOG.md). \n',
    'author': 'Diagrams-web',
    'author_email': 'no_spam@nowhere.mail',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/diagrams-web/diagrams-xtd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
