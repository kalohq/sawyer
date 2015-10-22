import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''


def get_version():
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    with open(os.path.join('sawyer', '__init__.py'), 'rt') as f:
        matches = re.search(version_regex, f.read(), re.M)
        if matches:
            return matches.group(1)
        else:
            return RuntimeError('Cannot find version string in sawyer package')

setup(
    name='sawyer',
    version=get_version(),
    description='Sawyer changelog generator',
    packages=['sawyer'],
    long_description=README,
    author='Christoffer Torris Olsen',
    author_email='chris@lystable.com',
    url='https://github.com/lystable/sawyer',
    zip_safe=False,
    license='MIT',
    install_requires=[
        'markdown',
        'Jinja2',
        'requests',
        'python-dateutil',
        'pytz',
    ],
    entry_points={
        'console_scripts': [
            'sawyer = sawyer.console:main',
        ],
    },
)
