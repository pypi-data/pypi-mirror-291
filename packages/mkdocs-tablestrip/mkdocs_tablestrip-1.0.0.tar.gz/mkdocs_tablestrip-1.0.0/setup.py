from setuptools import setup

setup(
    entry_points={
        'mkdocs.plugins': [
            'tablestrip = src.plugin:TableStrip'
        ]
    }
)
