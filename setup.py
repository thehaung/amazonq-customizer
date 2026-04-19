from setuptools import setup, find_packages

setup(
    name="amazonq-customizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "amazonq-customizer=amazonq_customizer.main:app",
        ],
    },
)
