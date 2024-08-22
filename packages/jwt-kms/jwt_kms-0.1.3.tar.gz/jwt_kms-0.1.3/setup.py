# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jwt_kms']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=43.0.0,<44.0.0']

entry_points = \
{'console_scripts': ['test = scripts:test']}

setup_kwargs = {
    'name': 'jwt-kms',
    'version': '0.1.3',
    'description': 'Library to offload some JWT crypto operations to KMS',
    'long_description': "# Python `jwt_kms` library\n\nThis library is work in progress.\n\nIsolating private asymmetric keys to AWS KMS helps improve security by \nmaking it next to impossible to make copies of them. This library aims to \nprovide a simple interface to use KMS keys to sign payloads into JWS tokens \nand/or to encrypt payloads into JWE tokens.\n\nSigning with RSA and EC keys is currently supported.\n\n## Keys\n\n```\nimport boto3\nfrom jwt_kms import jwk\n\nclient = boto3.client('kms')\nkey = jwk.JWK(client, 'some-key-id')\n\npublic_key_pem = key.public_key_pem\n```\n\n## Signing\n\n```\nfrom jwt_kms import jws\n\npayload = {\n   'something': 'yes',\n   'more_something': 'abc'\n}\n\ntoken = jws.JWS(payload).add_signature(key, 'RS256').serialize(compact=True)  # or compact=False\n```\n\n## Encrypting\n\nTODO.\n",
    'author': 'Juha-Matti Tapio',
    'author_email': 'jmtapio@verkkotelakka.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jmtapio/python-jwt-kms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
