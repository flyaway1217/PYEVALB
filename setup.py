from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import os

import PYEVALB


PACKAGE_NAME = 'PYEVALB'
REQUIREMENT_DIR = 'requirements'


# def get_long_description():
#     try:
#         with open('README.md', encoding='utf8') as f:
#             return f.read()
#     except IOError:
#         return ''

with open(os.path.join(REQUIREMENT_DIR, 'test-requirements.txt')) as f:
    tests_require = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, 'requirements.txt')) as f:
    install_require = [line.strip() for line in f if line.strip()]


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

setup(
    name=PACKAGE_NAME,
    version=PYEVALB.__version__,
    # version='0.1.1',
    packages=['PYEVALB', ],
    url='https://github.com/flyaway1217/PYEVALB',
    license='GNU',
    keywords='score bracket tree banks',

    author='Flyaway',
    author_email='flyaway1217@gmail.com',

    description='Scoring tools for bracket tree banks.',
    long_description=open('README.rst', encoding='utf8').read(),
    cmdclass={'test': Tox},

    include_package_data=True,
    install_requires=install_require,
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'PYEVALB = PYEVALB.__main__:main'
            ]
        },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ]
)
