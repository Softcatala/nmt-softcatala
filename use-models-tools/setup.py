import os
from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="use_models_tools",
    py_modules=["nmt_sc"],
    version="1.0.0",
    description="Softcatalà neuronal machine translation library",
    url="https://github.com/Softcatala/nmt-softcatala",
    author="Jordi Mas",
    author_email="jmas@softcatala.org",
    license="GPLv2+",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    packages=find_packages(exclude=["test*"]),
    install_requires=parse_requirements("requirements.txt"),
    package_data={'nmt_sc': ['segment.srx']},
    entry_points={
        "console_scripts": [
            "model_to_po=nmt_sc.model_to_po:main",
            "model_to_txt=nmt_sc.model_to_txt:main"
        ]
    },
)
