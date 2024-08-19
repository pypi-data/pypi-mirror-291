from setuptools import setup, find_packages

setup(
    name="barwex-sshc",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "prettytable>=3.11.0",
        "pycryptodome>=3.20.0",
    ],
    entry_points={
        "console_scripts": [
            "sshc=sshc.entry_scripts:main",
        ],
    },
)
