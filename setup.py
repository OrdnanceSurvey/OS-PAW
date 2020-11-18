import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

CLASSIFIERS = ["Programming Language :: Python :: 3",
               "Programming Language :: Python :: 3.8",
               "License :: OSI Approved :: MIT License"]

REQUIREMENTS = ['geojson==2.5.0', 
                'requests==2.24.0',
                'pytest==6.1.2']

setup(
    name="os-paw",
    version="1.0.1",
    description="OS-PAW is the Ordnance Survey Python API Wrapper designed to make data from the OS Data Hub APIs readily accessible to python developers.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Rapid Prototyping Team",
    author_email='jacob.rainbow@os.uk',
    license="MIT",
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    packages=["os_paw"],
    include_package_data=True,
)


