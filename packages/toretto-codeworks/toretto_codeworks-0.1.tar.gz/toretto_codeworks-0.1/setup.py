from setuptools import setup, find_packages

setup(
    name="toretto_codeworks",  # Назва вашого пакета
    version="0.1",  # Версія вашого пакета
    packages=find_packages(),  # Знайде всі пакети у вашому проекті
    install_requires=["prompt_toolkit", "wcwidth", "tabulate"],  # Список залежностей, якщо є
    entry_points={
        'console_scripts': [
            'assistant-bot = src.main:main',
        ],
    },
)

