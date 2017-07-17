from setuptools import setup, find_packages

setup(
    name='murpy',
    # VERSION = MAJOR.MINOR.MAINTENANCE
    version='0.1.0',
    # MAJOR version when they make incompatible API changes,
    # MINOR version when they add functionality in a backwards-compatible manner, and
    # MAINTENANCE version when they make backwards-compatible bug fixes
    description='A Brainfuck code generator from an own language',
    url='https://github.com/eisterman/MurPy',
    author='eisterman',
    author_email='federico.pasqua.96@gmail.com',
    license='GPLv3.0',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # TODO: Check the project with Python 2
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='brainfuck-transpiler brainfuck transpiler code-generator language programming-language',
    packages=find_packages(exclude=[]),
    install_requires=[],
    python_requires='>=3'
)
