from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'tablestrip = src.plugin:TableStrip'
        ]
    }
)
