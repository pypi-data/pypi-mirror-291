from setuptools import setup, find_packages


setup(
    name="toretto_codeworks",
    version="0.7",
    package_dir={'': '.'},
    install_requires=[
        "prompt_toolkit",
        "wcwidth",
        "tabulate"
    ],
    entry_points={
        'console_scripts': [
            'assistant-bot = main:main',
        ],
    },
)
