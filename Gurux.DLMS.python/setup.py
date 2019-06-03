import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gurux_dlms",
    version="1.0.6",
    author="Gurux Ltd",
    author_email="gurux@gurux.org",
    description="Gurux DLMS library for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gurux/gurux.dlms.python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)
