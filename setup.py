import pathlib
from setuptools import setup
from grampyx.__init__  import __version__


PARENT_DIR = pathlib.Path(__file__).parent
README = (PARENT_DIR / "Examples.md").read_text()

setup(
    name="grampyx",
    version=__version__,
    description="Convert text to image",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cbattle12/grampyx",
    author="Christopher Battle",
    author_email="christopher.g.battle@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.5",
    packages=["grampyx"],
    include_package_data=True,
    install_requires=["numpy>=1.15.0"],
)
