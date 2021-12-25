from setuptools import setup, find_packages

setup(
    name="comorbid-graphs",
    version="0.0.1",
    description="A package for quick analysis of graphical data. Can load from ontology-json.",
    url="",
    author="DorenCalliku",
    author_email="doren.calliku01@universitadipavia.it",
    license="",  # TODO add
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "anytree",
    ],
    zip_safe=False,
)
