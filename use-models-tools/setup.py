import os
import pkg_resources
from setuptools import setup, find_packages

# This call to setup() does all the work
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
        'Programming Language :: Python :: 3.11',
    ],
    include_package_data=True,
    packages=find_packages(exclude=["test*"]),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    package_data={'nmt_sc': ['segment.srx']},
    entry_points={
        "console_scripts": [
            "model_to_po=nmt_sc.model_to_po:main",
            "model_to_txt=nmt_sc.model_to_txt:main"
        ]
    },
)

