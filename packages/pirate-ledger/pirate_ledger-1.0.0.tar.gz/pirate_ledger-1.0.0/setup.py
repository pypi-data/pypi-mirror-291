from setuptools import setup, find_packages

setup(
    name="pirate_ledger",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "prompt-toolkit==3.0.36",
        "questionary==2.0.1",
        "wcwidth==0.2.13",
        "rapidfuzz===3.9.6",
        "colorama==0.4.6",
        "tabulate==0.9.0"
    ],
    entry_points={
        "console_scripts": [
            "pirate_ledger=pirate_ledger.main:main",
        ],
    },
    author="Grimbergen Team",
    author_email="yuriy@hubmee.com",
    description="A pirate-themed ledger for crew members and sea notes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/master-of-science-neoversity/introduction-to-computer-programming-part-1/grimbergen-team-11-project",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12.4",
)