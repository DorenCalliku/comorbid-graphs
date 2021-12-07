from setuptools import setup, find_packages

setup(
    name="ontology-graphs",
    version="0.0.1",
    description="Turning to knowledge graphs ontologies for ease of use.",
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
