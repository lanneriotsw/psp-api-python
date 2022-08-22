"""
python setup.py sdist
twine upload dist/*
"""
from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="lannerpsp",
    install_requires=[],
    extras_require={
        "lec7242": ["portio == 0.5"],
    },
)
